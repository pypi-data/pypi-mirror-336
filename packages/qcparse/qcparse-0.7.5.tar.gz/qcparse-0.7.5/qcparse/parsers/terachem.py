"""Parsers for TeraChem output files."""

import re
from pathlib import Path
from typing import Optional, Union

from qcconst import constants
from qcio import (
    CalcType,
    OptimizationResults,
    ProgramInput,
    ProgramOutput,
    Provenance,
    SinglePointResults,
    Structure,
)

from qcparse.exceptions import MatchNotFoundError
from qcparse.models import FileType, ParsedDataCollector

from .utils import parser, regex_search

SUPPORTED_FILETYPES = {FileType.stdout}


def parse_calctype(string: str) -> CalcType:
    """Parse the calctype from TeraChem stdout."""
    calctypes = {
        r"SINGLE POINT ENERGY CALCULATIONS": CalcType.energy,
        r"SINGLE POINT GRADIENT CALCULATIONS": CalcType.gradient,
        r"FREQUENCY ANALYSIS": CalcType.hessian,
    }
    for regex, calctype in calctypes.items():
        match = re.search(regex, string)
        if match:
            return calctype
    raise MatchNotFoundError(regex, string)


@parser()
def parse_energy(string: str, data_collector: ParsedDataCollector):
    """Parse the final energy from TeraChem stdout.

    NOTE:
        - Works on frequency files containing many energy values because re.search()
            returns the first result
    """
    regex = r"FINAL ENERGY: (-?\d+(?:\.\d+)?)"
    data_collector.energy = float(regex_search(regex, string).group(1))


def parse_excited_states(string: str):
    """Parse the excited state information from a TDDFT TeraChem stdout.
    Creates a list of matches. One for each computed excited state.
    Each match is a dictionary with keys corresponding to the columns of excited state information at the end of a TDDFT TeraChem stdout.
    """
    regex = r"^\s*(?:\d+)\s+(?P<energy>-?\d+\.\d+)\s+(?P<exc_energy>-?\d+\.\d+)\s+(?P<osc_strength>-?\d+\.\d+)\s+(?P<s_squared>-?\d+\.\d+)\s+(?P<max_ci_coeff>-?\d+\.\d+)\s+(?P<excitation>\d+\s+->\s+\d+\s+:\s+\w+\s+->\s+\w+)$"
    
    matches = re.finditer(regex, string, re.MULTILINE)
    
    # Create list to add each excited state to
    excited_states = []
    for match in matches:
        # Convert the match object to a dictionary of named groups
        state_data = match.groupdict()
        
        # Convert numeric values to floats
        for key in ['energy', 'exc_energy', 'osc_strength', 's_squared', 'max_ci_coeff']:
            if key == "exc_energy":
                state_data[key] = float(state_data[key]) * constants.EV_TO_HARTREE
            else:
                state_data[key] = float(state_data[key])
        
        excited_states.append(state_data)
    
    if not excited_states:
        raise MatchNotFoundError(regex, string)
    
    return excited_states


def parse_gradients(string: str, all: bool = True) -> list[list[list[float]]]:
    """Parse gradients from TeraChem stdout.

    Args:
        string: The contents of the TeraChem stdout file.
        all: If True, return all gradients. If False, return only the first gradient.

    Returns:
        A list of gradients. Each gradient is a list of 3-element lists, where each
        3-element list is a gradient for an atom.
    """
    # This will match all floats after the dE/dX dE/dY dE/dZ header and stop at the
    # terminating -- or -= line that follows gradients or optimizations.
    regex = r"(?<=dE\/dX\s{12}dE\/dY\s{12}dE\/dZ\n)[\d\.\-\s]+(?=\n(?:--|-=))"

    if all is True:
        match: Optional[Union[list, re.Match]] = re.findall(regex, string)
    else:
        match = re.search(regex, string)

    if not match:
        raise MatchNotFoundError(regex, string)

    grad_strings: list[str] = match if all is True else [match.group()]  # type: ignore

    gradients = []

    for grad_string in grad_strings:
        # split string and cast to floats
        values = [float(val) for val in grad_string.split()]

        # arrange into N x 3 gradient
        gradient = []
        for i in range(0, len(values), 3):
            gradient.append(values[i : i + 3])

        gradients.append(gradient)

    return gradients


@parser(only=[CalcType.gradient, CalcType.hessian])
def parse_gradient(string: str, data_collector: ParsedDataCollector):
    """Parse first gradient from TeraChem stdout."""
    gradient = parse_gradients(string, all=False)[0]

    data_collector.gradient = gradient


@parser(only=[CalcType.hessian])
def parse_hessian(string: str, data_collector: ParsedDataCollector):
    """Parse Hessian Matrix from TeraChem stdout

    Notes:
        This function searches the entire document N times for all regex matches where
        N is the number of atoms. This makes the function's code easy to reason about.
        If performance becomes an issues for VERY large Hessians (unlikely) you can
        accelerate this function by parsing all Hessian floats in one pass, like the
        parse_gradient function above, and then doing the math to figure out how to
        properly sequence those values to from the Hessian matrix given TeraChem's
        six-column format for printing out Hessian matrix entries.
    """
    # requires .format(int). {{}} values are to escape {15|2} for .format()
    regex = r"(?:\s+{}\s)((?:\s-?\d\.\d{{15}}e[+-]\d{{2}})+)"
    hessian = []

    # Match all rows containing Hessian data; one set of rows at a time
    count = 1
    while matches := re.findall(regex.format(count), string):
        row = []
        for match in matches:
            row.extend([float(val) for val in match.split()])
        hessian.append(row)
        count += 1

    if not hessian:
        raise MatchNotFoundError(regex, string)

    # Assert we have created a square Hessian matrix
    for i, row in enumerate(hessian):
        assert len(row) == len(
            hessian
        ), "We must have missed some floats. Hessian should be a square matrix. Only "
        f"recovered {len(row)} of {len(hessian)} floats for row {i}."

    data_collector.hessian = hessian


@parser()
def parse_natoms(string: str, data_collector: ParsedDataCollector):
    """Parse number of atoms value from TeraChem stdout"""
    regex = r"Total atoms:\s*(\d+)"
    data_collector.calcinfo_natoms = int(regex_search(regex, string).group(1))


@parser()
def parse_nmo(string: str, data_collector: ParsedDataCollector):
    """Parse the number of molecular orbitals TeraChem stdout"""
    regex = r"Total orbitals:\s*(\d+)"
    data_collector.calcinfo_nmo = int(regex_search(regex, string).group(1))


def parse_version_control_details(string: str) -> str:
    """Parse TeraChem git commit or Hg version from TeraChem stdout."""
    regex = r"(Git|Hg) Version: (\S*)"
    return regex_search(regex, string).group(2)


def parse_terachem_version(string: str) -> str:
    """Parse TeraChem version from TeraChem stdout."""
    regex = r"TeraChem (v\S*)"
    return regex_search(regex, string).group(1)


def parse_version_string(string: str) -> str:
    """Parse version string plus git commit from TeraChem stdout.

    Matches format of 'terachem --version' on command line.
    """
    return f"{parse_terachem_version(string)} [{parse_version_control_details(string)}]"


def calculation_succeeded(string: str) -> bool:
    """Determine from TeraChem stdout if a calculation completed successfully."""
    regex = r"Job finished:"
    if re.search(regex, string):
        # If any match for a failure regex is found, the calculation failed
        return True
    return False


def parse_optimization_dir(
    directory: Union[Path, str],
    stdout: str,
    *,
    inp_obj: ProgramInput,
) -> OptimizationResults:
    """Parse the output directory of a TeraChem optimization calculation.

    Args:
        directory: Path to the directory containing the TeraChem output files.
        stdout: The contents of the TeraChem stdout file.
        inp_obj: The input object used for the calculation.

    Returns:
        OptimizationResults object
    """
    directory = Path(directory)

    # Parse the structures
    structures = Structure.open(directory / "optim.xyz")
    assert isinstance(structures, list), "Expected multiple structures in optim.xyz"

    # Parse Values
    from qcparse import parse

    # Parse all the values from the stdout file
    spr = parse(stdout, "terachem", "stdout", CalcType.energy)

    gradients = parse_gradients(stdout)
    program_version = parse_version_string(stdout)

    # Create the trajectory
    trajectory: list[ProgramOutput] = [
        ProgramOutput(
            input_data=ProgramInput(
                calctype=CalcType.gradient,
                structure=structure,
                model=inp_obj.model,
                keywords=inp_obj.keywords,
            ),
            results=SinglePointResults(
                **{
                    **spr.model_dump(),
                    # TeraChem places the energy as the first comment in the xyz file
                    "energy": structure.extras[Structure._xyz_comment_key][0],
                    # # Will be coerced by Pydantic to np.ndarray
                    "gradient": gradient,  # type: ignore
                }
            ),
            success=True,
            provenance=Provenance(
                program="terachem",
                program_version=program_version,
                scratch_dir=directory.parent,
            ),
        )
        for structure, gradient in zip(structures, gradients)
    ]

    return OptimizationResults(trajectory=trajectory)

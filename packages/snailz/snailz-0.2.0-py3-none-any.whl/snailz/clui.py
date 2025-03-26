"""Command-line interface for snailz.

Each subcommand takes options --output (output file path), --params (parameter
file), and --seed (random number seed) along with command-specific parameters.
If a parameter file is given, it is read first and additional parameters
override its values. If a parameter file is not given, all other parameters
are required.
"""

from datetime import date
import json
import random

import click

from .assays import Assay, Assays, assays_check, assays_generate, assays_to_csv
from .grid import Grid, grid_check, grid_generate, grid_to_csv
from .people import People, people_check, people_generate, people_to_csv
from .specimens import (
    Specimens,
    specimens_check,
    specimens_generate,
    specimens_to_csv,
    mutate_masses,
)
from .mangle import mangle_assays
from . import utils


@click.group()
def cli():
    """Command-line interface for snailz."""


@cli.command()
@click.option("--output", type=click.Path(), help="Path to JSON output file")
@click.option(
    "--params", type=click.Path(exists=True), help="Path to JSON parameter file"
)
@click.option("--seed", type=int, help="Random seed")
@click.option(
    "--baseline",
    type=float,
    help="Baseline reading value for non-susceptible specimens (must be > 0)",
)
@click.option("--end-date", callback=utils.validate_date, help="End date (YYYY-MM-DD)")
@click.option(
    "--mutant", type=float, help="Reading value for susceptible specimens (must be > 0)"
)
@click.option("--noise", type=float, help="Noise level for readings (must be > 0)")
@click.option("--people", type=click.Path(exists=True), help="Path to people JSON file")
@click.option("--plate-size", type=int, help="Size of assay plate (must be > 0)")
@click.option(
    "--specimens", type=click.Path(exists=True), help="Path to specimens JSON file"
)
@click.option(
    "--start-date", callback=utils.validate_date, help="Start date (YYYY-MM-DD)"
)
@click.pass_context
def assays(
    ctx,
    output=None,
    params=None,
    seed=None,
    baseline=None,
    end_date=None,
    mutant=None,
    noise=None,
    people=None,
    plate_size=None,
    specimens=None,
    start_date=None,
):
    """Generate assays for specimens within a date range."""
    try:
        # Load previously-generated data.
        people = utils.load_data("people", people, People)
        specimens = utils.load_data("specimens", specimens, Specimens)

        # Get parameters for assay generation
        supplied = (
            ("baseline", baseline),
            ("end_date", end_date),
            ("mutant", mutant),
            ("noise", noise),
            ("plate_size", plate_size),
            ("seed", seed),
            ("start_date", start_date),
        )
        parameters = _get_params(
            "assays",
            assays_check,
            supplied,
            params,
            end_date=date.fromisoformat,
            start_date=date.fromisoformat,
        )
        random.seed(parameters["seed"])

        # Generate assays with specimens and people
        result = assays_generate(parameters, specimens, people)
        utils.report_result(output, result)
    except Exception as e:
        utils.fail(f"Error generating assays: {str(e)}")


@cli.command()
@click.option(
    "--input",
    type=click.Path(exists=True),
    required=True,
    help="Path to input JSON file",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Path to output CSV file (should be a directory for assays)",
)
@click.option(
    "--kind",
    type=click.Choice(["assays", "grid", "people", "specimens"]),
    required=True,
    help="Type of data to convert",
)
def convert(input, output, kind):
    """Convert JSON data to CSV format.

    Converts grid, specimens, or assays data from JSON to CSV format.
    If output is not specified, writes to standard output.
    """
    try:
        # Load the input file based on kind
        if kind == "assays":
            # Assays need a special loading process to handle date fields
            with open(input, "r") as f:
                assay_data = json.load(f)

            # Convert items to Assay objects with proper date handling
            assay_items = []
            for item_dict in assay_data.get("items", []):
                # Convert date string to date object if needed
                if "performed" in item_dict and isinstance(item_dict["performed"], str):
                    item_dict["performed"] = date.fromisoformat(item_dict["performed"])
                # Create Assay object
                assay_items.append(Assay(**item_dict))

            # Create Assays object with items
            data = Assays(items=assay_items, params=assay_data.get("params", {}))

            # Convert assays to CSV
            assays_to_csv(data, output)
        elif kind == "grid":
            data = utils.load_data("grid", input, Grid)
            grid_to_csv(data, output)
        elif kind == "people":
            data = utils.load_data("people", input, People)
            people_to_csv(data, output)
        elif kind == "specimens":
            data = utils.load_data("specimens", input, Specimens)
            specimens_to_csv(data, output)
        else:
            raise ValueError(f"unknown kind {kind}")
    except Exception as e:
        utils.fail(f"Error converting data: {str(e)}")


@cli.command()
@click.option("--output", type=click.Path(), help="Path to JSON output file")
@click.option(
    "--params", type=click.Path(exists=True), help="Path to JSON parameter file"
)
@click.option("--seed", type=int, help="Random seed")
@click.option("--depth", type=int, help="Grid depth")
@click.option("--size", type=int, help="Grid size")
@click.pass_context
def grid(
    ctx,
    output=None,
    params=None,
    seed=None,
    depth=None,
    size=None,
):
    """Generate grid."""
    try:
        supplied = (
            ("depth", depth),
            ("seed", seed),
            ("size", size),
        )
        parameters = _get_params("grid", grid_check, supplied, params)
        random.seed(parameters["seed"])
        result = grid_generate(parameters)
        utils.report_result(output, result)
    except Exception as e:
        utils.fail(f"Error generating grid: {str(e)}")


@cli.command()
@click.option(
    "--dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="Directory containing assay CSV files",
)
@click.option(
    "--people",
    type=click.Path(exists=True),
    required=True,
    help="Path to people.csv file",
)
@click.option(
    "--seed", type=int, required=True, help="Random seed for assigning people"
)
def mangle(seed, dir, people):
    """Modify assay files by reassigning people.

    This command takes assay files in a directory and reassigns the people
    who performed the assays using the provided seed for random number generation.
    """
    try:
        random.seed(seed)
        mangle_assays(dir, people)
    except Exception as e:
        utils.fail(f"Error mangling assays: {str(e)}")


@cli.command()
@click.option("--output", type=click.Path(), help="Path to JSON output file")
@click.option(
    "--params", type=click.Path(exists=True), help="Path to JSON parameter file"
)
@click.option("--seed", type=int, help="Random seed")
@click.option("--locale", type=str, help="Locale for generating people")
@click.option("--number", type=int, help="Number of people to generate")
@click.pass_context
def people(
    ctx,
    output=None,
    params=None,
    seed=None,
    locale=None,
    number=None,
):
    """Generate people."""
    try:
        supplied = (
            ("locale", locale),
            ("number", number),
            ("seed", seed),
        )
        parameters = _get_params("people", people_check, supplied, params)
        random.seed(parameters["seed"])
        result = people_generate(parameters)
        utils.report_result(output, result)
    except Exception as e:
        utils.fail(f"Error generating people: {str(e)}")


@cli.command()
@click.option("--output", type=click.Path(), help="Path to JSON output file")
@click.option(
    "--params", type=click.Path(exists=True), help="Path to JSON parameter file"
)
@click.option("--seed", type=int, help="Random seed")
@click.option("--grid", type=str, help="Path to grid JSON file")
@click.option("--length", type=int, help="Length of each genome")
@click.option("--max-mass", type=float, help="Maximum specimen mass")
@click.option("--min-mass", type=float, help="Minimum specimen mass")
@click.option("--mutations", type=int, help="Number of possible mutation loci")
@click.option("--mut-scale", type=float, help="Mutation scaling factor")
@click.option("--number", type=int, help="Number of specimens to generate")
@click.pass_context
def specimens(
    ctx,
    output=None,
    params=None,
    seed=None,
    grid=None,
    length=None,
    max_mass=None,
    min_mass=None,
    mut_scale=None,
    mutations=None,
    number=None,
):
    """Generate specimens."""
    try:
        # Load previously-generated data.
        grid = utils.load_data("grid", grid, Grid)

        # Get parameters for specimen generation.
        supplied = (
            ("length", length),
            ("max_mass", max_mass),
            ("min_mass", min_mass),
            ("mut_scale", mut_scale),
            ("mutations", mutations),
            ("number", number),
            ("seed", seed),
        )
        parameters = _get_params("specimens", specimens_check, supplied, params)
        random.seed(parameters["seed"])
        result = specimens_generate(parameters)
        mutate_masses(grid, result, parameters["mut_scale"])
        utils.report_result(output, result)
    except Exception as e:
        utils.fail(f"Error generating specimens: {str(e)}")


def _get_params(caller, checker, supplied, params_file, **converters):
    """Get and check parameter values."""
    # Read parameter file if given.
    if params_file:
        with open(params_file, "r") as f:
            result = json.load(f)
            for name, conv in converters.items():
                result[name] = conv(result[name])
    elif any(value is None for _, value in supplied):
        names = ", ".join(f"--{name}" for name, _ in supplied)
        raise ValueError(f"Error: {names} required when not using parameter file")
    else:
        result = {}

    # Override with extra parameters and re-check.
    for name, value in supplied:
        if value is not None:
            result[name] = value
    checker(result)

    return result


if __name__ == "__main__":
    cli()

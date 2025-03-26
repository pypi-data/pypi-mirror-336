import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import random
import sys
from typing import Sequence  # Still needed for covariance

from . import utils
from .specimens import Specimens
from .people import People

# Required parameters and types.
ASSAYS_PARAMS = {
    "baseline": float,
    "end_date": date,
    "mutant": float,
    "noise": float,
    "plate_size": int,
    "seed": int,
    "start_date": date,
}

# Subdirectory for writing individual assay files.
ASSAYS_SUBDIR = "assays"


@dataclass
class Assay:
    """A single assay with date, unique identifier, specimen ID, person ID, readings and treatments."""

    performed: date
    ident: str
    specimen_id: str
    person_id: str
    readings: list[list[float]]
    treatments: list[list[str]]


@dataclass
class Assays:
    """Keep track of generated assays."""

    items: list[Assay]
    params: dict[str, object]


def assays_check(params: dict[str, object]) -> None:
    """Check parameters for assay generation.

    Parameters:
        params: Dictionary containing assay generation parameters

    Raises:
        ValueError: If parameters are missing, have wrong types, or have invalid values
    """
    utils.check_keys_and_types(ASSAYS_PARAMS, params)
    for name in ["plate_size", "noise", "baseline", "mutant"]:
        utils.require(0 < params[name], f"{name} must be positive")
    utils.require(
        params["start_date"] <= params["end_date"],
        "start date must be less than or equal to end date",
    )


def assays_generate(
    params: dict[str, object], specimens: Specimens, people: People
) -> Assays:
    """Generate an assay for each specimen.

    Parameters:
        params: Dictionary containing assay generation parameters
        specimens: Specimens object with individual specimens to generate assays for
        people: People object with staff members

    Returns:
        Assays object containing generated assays and parameters
    """
    assays_check(params)

    start = params["start_date"]
    end = params["end_date"]
    plate_size = params["plate_size"]
    noise = params["noise"]
    baseline = params["baseline"]
    mutant = params["mutant"]

    days_delta = (end - start).days + 1
    individuals = specimens.individuals
    susc_locus = specimens.susceptible_locus
    susc_base = specimens.susceptible_base
    items = []

    gen = utils.UniqueIdGenerator("assays", lambda: f"{random.randint(0, 999999):06d}")

    for individual in individuals:
        assay_date = start + timedelta(days=random.randint(0, days_delta - 1))
        assay_id = gen.next()

        # Generate treatments randomly with equal probability
        treatments = []
        for row in range(plate_size):
            treatment_row = []
            for col in range(plate_size):
                treatment_row.append(random.choice(["S", "C"]))
            treatments.append(treatment_row)

        # Generate readings based on treatments and susceptibility
        readings = []
        is_susceptible = individual.genome[susc_locus] == susc_base
        for row in range(plate_size):
            reading_row = []
            for col in range(plate_size):
                if treatments[row][col] == "C":
                    # Control cells have values uniformly distributed between 0 and noise
                    reading_row.append(random.uniform(0, noise))
                elif is_susceptible:
                    # Susceptible specimens (with susceptible base at susceptible locus)
                    # Base mutant value plus noise scaled by mutant/baseline ratio
                    scaled_noise = round(noise * mutant / baseline, utils.PRECISION)
                    reading_row.append(mutant + random.uniform(0, scaled_noise))
                else:
                    # Non-susceptible specimens
                    # Base baseline value plus uniform noise
                    reading_row.append(baseline + random.uniform(0, noise))
            # Handle limited precision.
            reading_row = [round(r, utils.PRECISION) for r in reading_row]
            readings.append(reading_row)

        # Randomly select a person to perform the assay
        person = random.choice(people.individuals)

        # Create the assay with reference to the specimen ID and person ID
        items.append(
            Assay(
                performed=assay_date,
                ident=assay_id,
                specimen_id=individual.ident,
                person_id=person.ident,
                readings=readings,
                treatments=treatments,
            )
        )

    return Assays(items=items, params=params)


def assays_to_csv(
    assays: Assays, directory: str | None, ident: str | None = None
) -> None:
    """Write assay data to CSV files.

    Args:
        assays: An Assays instance containing assay data
        directory: Directory to save output.
        ident: Optional assay ID to output only a specific assay

    If multiple files are created, writes assays.csv with fields:
    - ident: assay identifier
    - specimen_id: specimen identifier
    - performed: date the assay was performed

    For each assay (or just the specified one if ident is provided), creates:
    - assays/ID_design.csv: containing treatment data
    - assays/ID_assay.csv: containing reading data

    Each file has the format:
    id,<assay_id>
    specimen,<specimen_id>
    performed,<performed_date>
    ,A,B,C,...
    1,<data>,<data>,...
    2,<data>,<data>,...
    ...
    """
    # Filter assays if an ident is provided
    items_to_process = [
        item for item in assays.items if ident is None or item.ident == ident
    ]
    if not items_to_process and ident is not None:
        raise ValueError(f"No assay with ID {ident} found")

    # Write summary assays.csv file if multiple files are output.
    if directory is not None and ident is None:
        summary_file = Path(directory, "assays.csv")
        with open(summary_file, "w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["ident", "specimen_id", "performed", "performed_by"])
            for assay in assays.items:
                writer.writerow(
                    [
                        assay.ident,
                        assay.specimen_id,
                        assay.performed.isoformat(),
                        assay.person_id,
                    ]
                )

    # Process each assay
    for assay in items_to_process:
        # Generate column headers (A, B, C, etc.)
        plate_size = len(assay.readings)
        column_headers = [""] + [chr(65 + i) for i in range(plate_size)]

        # Write treatments to ID_design.csv
        _write_assay_csv(
            assay,
            directory,
            f"{assay.ident}_design.csv",
            assay.treatments,
            column_headers,
        )

        # Write readings to ID_assay.csv
        _write_assay_csv(
            assay, directory, f"{assay.ident}_assay.csv", assay.readings, column_headers
        )


def _write_assay_csv(
    assay: Assay,
    directory: str | None,
    filename: str,
    data: Sequence[Sequence[float | str]],
    column_headers: list[str],
) -> None:
    """Helper function to write a single assay CSV file.

    Parameters:
        assay: The Assay instance
        directory: Directory to save file (None for stdout)
        filename: Name of the file to create
        data: The data to write (treatments or readings)
        column_headers: Column headers including empty first cell

    Side effects:
        Either writes to a file in the specified directory or prints to stdout
    """
    # If directory is None, write to stdout
    if directory is None:
        print(f"--- {filename}")
        stream = sys.stdout
    else:
        Path(directory, ASSAYS_SUBDIR).mkdir(exist_ok=True)
        stream = open(Path(directory, ASSAYS_SUBDIR, filename), "w", newline="")

    writer = csv.writer(stream)

    max_columns = len(column_headers)
    padding = [""] * (max_columns - 2)
    writer.writerow(["id", assay.ident] + padding)
    writer.writerow(["specimen", assay.specimen_id] + padding)
    writer.writerow(["performed", assay.performed.isoformat()] + padding)
    writer.writerow(["performed_by", assay.person_id] + padding)

    # Write column headers, padding if necessary
    writer.writerow(column_headers)

    # Write data rows with row numbers
    for i, row in enumerate(data, 1):
        writer.writerow([i] + row)

    # Close file if we opened one
    if directory is not None:
        stream.close()

"""Generate synthetic people data."""

import csv
from dataclasses import dataclass
import random
import sys
# No typing imports needed

from faker import Faker
import faker.config

from . import utils

# Required parameters and types.
PEOPLE_PARAMS = {
    "locale": str,
    "number": int,
    "seed": int,
}


@dataclass
class Person:
    """A single person with personal and family names."""

    family: str
    ident: str
    personal: str


@dataclass
class People:
    """Keep track of generated people."""

    individuals: list[Person]
    params: dict[str, object]


def people_check(params: dict[str, object]) -> None:
    """Check people generation parameters.

    Parameters:
        params: Dictionary containing people generation parameters

    Raises:
        ValueError: If parameters are missing, have wrong types, or have invalid values
    """
    utils.check_keys_and_types(PEOPLE_PARAMS, params)
    utils.require(0 < params["number"], "number must be positive")
    utils.require(
        params["locale"] in faker.config.AVAILABLE_LOCALES,
        f"unknown locale {params['locale']}",
    )


def people_generate(params: dict[str, object]) -> People:
    """Generate synthetic people data.

    Parameters:
        params: Dictionary containing people generation parameters

    Returns:
        People object containing generated individuals and parameters
    """
    people_check(params)
    fake = Faker(params["locale"])
    fake.seed_instance(params["seed"])

    gen = utils.UniqueIdGenerator(
        "people",
        lambda p, f: f"{f[0].lower()}{p[0].lower()}{random.randint(0, 9999):04d}",
    )

    individuals = []
    for _ in range(params["number"]):
        personal = fake.first_name()
        family = fake.last_name()
        ident = gen.next(personal, family)
        individuals.append(Person(personal=personal, family=family, ident=ident))

    return People(individuals=individuals, params=params)


def people_to_csv(people: People, filename: str | None) -> None:
    """Write people data as CSV with columns for ident, personal, and family.

    Parameters:
        people: A People object containing the data to write
        filename: Path to output file, or None to write to standard output

    Side effects:
        Either writes to the specified output file or prints to stdout
    """
    stream = sys.stdout if filename is None else open(filename, "w", newline="")
    writer = csv.writer(stream)
    writer.writerow(["ident", "personal", "family"])
    for person in people.individuals:
        writer.writerow([person.ident, person.personal, person.family])
    if stream is not sys.stdout:
        stream.close()

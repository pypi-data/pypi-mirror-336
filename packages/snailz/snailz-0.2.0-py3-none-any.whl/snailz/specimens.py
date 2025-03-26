"""Generate snail specimens."""

import csv
from dataclasses import dataclass
import random
import string
import sys
# No typing imports needed

from . import utils
from .grid import Grid

# Required parameters and types.
SPECIMENS_PARAMS = {
    "length": int,
    "max_mass": float,
    "min_mass": float,
    "mut_scale": float,
    "mutations": int,
    "number": int,
    "seed": int,
}

# Bases.
BASES = "ACGT"


@dataclass
class Point:
    """A 2D point with x and y coordinates."""

    x: int | None = None
    y: int | None = None


@dataclass
class Individual:
    """A single specimen with genome, mass, site location and unique identifier."""

    genome: str
    ident: str
    mass: float
    site: Point


@dataclass
class Specimens:
    """Keep track of generated specimens."""

    individuals: list[Individual]
    loci: list[int]
    params: dict[str, object]
    reference: str
    susceptible_base: str
    susceptible_locus: int


def specimens_check(params: dict[str, object]) -> None:
    """Check specimen generation parameters.

    Parameters:
        params: Dictionary containing specimen generation parameters

    Raises:
        ValueError: If parameters are missing, have wrong types, or have invalid values
    """
    utils.check_keys_and_types(SPECIMENS_PARAMS, params)

    for name in ["length", "min_mass", "mutations", "number"]:
        utils.require(0 < params[name], f"{name} must be positive")
    utils.require(
        0 <= params["mutations"] <= params["length"],
        "mutations must be between 0 and length",
    )
    utils.require(
        params["min_mass"] < params["max_mass"],
        "max_mass must be greater than min_mass",
    )


def specimens_generate(params: dict[str, object]) -> Specimens:
    """Generate specimens with random genomes and masses.

    Each genome is a string of bases of the same length. One locus
    is randomly chosen as "significant", and a specific mutation there
    predisposes the snail to mass changes. Other mutations are added
    randomly at other loci.

    Parameters:
        params: Dictionary containing specimen generation parameters

    Returns:
        Specimens object containing the generated specimens and parameters
    """
    specimens_check(params)
    loci = _make_loci(params)
    reference = _make_reference_genome(params)
    susc_loc = _choose_one(loci)
    susc_base = reference[susc_loc]
    genomes = [_make_genome(reference, loci) for i in range(params["number"])]
    masses = _make_masses(params, genomes, susc_loc, susc_base)

    # Generate unique identifiers
    identifiers = _make_idents(params["number"])

    individuals = [
        Individual(genome=g, mass=m, site=Point(), ident=i)
        for g, m, i in zip(genomes, masses, identifiers)
    ]

    return Specimens(
        individuals=individuals,
        loci=loci,
        params=params,
        reference=reference,
        susceptible_base=susc_base,
        susceptible_locus=susc_loc,
    )


def specimens_to_csv(specimens: Specimens, filename: str | None) -> None:
    """Write specimens data as CSV.

    Parameters:
        specimens: A Specimens object containing specimen data
        filename: Path to output file, or None to write to standard output

    Side effects:
        Either writes to the specified output file or prints to stdout
    """
    stream = sys.stdout if filename is None else open(filename, "w", newline="")
    writer = csv.writer(stream)
    writer.writerow(["ident", "x", "y", "genome", "mass"])
    for indiv in specimens.individuals:
        writer.writerow(
            [indiv.ident, indiv.site.x, indiv.site.y, indiv.genome, indiv.mass]
        )
    if stream is not sys.stdout:
        stream.close()


def mutate_masses(
    grid: Grid,
    specimens: Specimens,
    mut_scale: float,
    specific_index: int | None = None,
) -> None:
    """Mutate mass based on grid values and genetic susceptibility.

    For each specimen, choose a random cell from the grid and modify
    the mass if the cell's value is non-zero and the genome is
    susceptible. Records the chosen site coordinates for each specimen
    regardless of whether mutation occurs.

    Parameters:
        grid: A Grid object containing pollution values
        specimens: A Specimens object with individuals to potentially mutate
        mut_scale: Scaling factor for mutation effect
        specific_index: Optional index to mutate only a specific specimen

    Side effects:
        Modifies specimen masses in-place for susceptible individuals
        Updates site coordinates for all individuals
    """
    grid_size = len(grid.grid)
    susc_locus = specimens.susceptible_locus
    susc_base = specimens.susceptible_base

    if specific_index is not None:
        indices = [specific_index]
    else:
        indices = range(len(specimens.individuals))

    for i in indices:
        individual = specimens.individuals[i]
        x = random.randrange(grid_size)
        y = random.randrange(grid_size)

        individual.site.x = x
        individual.site.y = y

        if grid.grid[x][y] > 0 and individual.genome[susc_locus] == susc_base:
            individual.mass = mutate_mass(individual.mass, mut_scale, grid.grid[x][y])


def mutate_mass(original: float, mut_scale: float, cell_value: int) -> float:
    """Mutate a single mass.

    Parameters:
        original: The original mass value
        mut_scale: Scaling factor for mutation effect
        cell_value: The grid cell value affecting the mutation

    Returns:
        The mutated mass value, rounded to PRECISION decimal places
    """
    return round(original * (1 + (mut_scale * cell_value)), utils.PRECISION)


def _choose_one(values: list[int]) -> int:
    """Choose a single random item from a collection.

    Parameters:
        values: A sequence to choose from

    Returns:
        A randomly selected item from the values sequence
    """
    return random.choices(values, k=1)[0]


def _choose_other(values: str, exclude: str) -> str:
    """Choose a value at random except for the excluded values.

    Parameters:
        values: A collection to choose from
        exclude: Value or collection of values to exclude from the choice

    Returns:
        A randomly selected item from values that isn't in exclude
    """
    candidates = list(sorted(set(values) - set(exclude)))
    return candidates[random.randrange(len(candidates))]


def _make_genome(reference: str, loci: list[int]) -> str:
    """Make an individual genome by mutating the reference genome.

    Parameters:
        reference: Reference genome string to base the new genome on
        loci: List of positions that can be mutated

    Returns:
        A new genome string with random mutations at some loci
    """
    result = list(reference)
    num_mutations = random.randint(1, len(loci))
    for loc in random.sample(range(len(loci)), num_mutations):
        result[loc] = _choose_other(BASES, reference[loc])
    return "".join(result)


def _make_idents(count: int) -> list[str]:
    """Create unique specimen identifiers.

    Each identifier is a 6-character string where:
    - First two chars are the same uppercase letters for all specimens
    - Remaining four chars are random uppercase letters and digits, unique for each specimen

    Parameters:
        count: Number of identifiers to generate

    Returns:
        List of unique specimen identifiers
    """
    prefix = "".join(random.choices(string.ascii_uppercase, k=2))
    chars = string.ascii_uppercase + string.digits
    gen = utils.UniqueIdGenerator(
        "specimens", lambda: f"{prefix}{''.join(random.choices(chars, k=4))}"
    )
    return [gen.next() for _ in range(count)]


def _make_loci(params: dict[str, object]) -> list[int]:
    """Make a list of mutable loci positions.

    Parameters:
        params: Dictionary with 'length' (genome length) and 'mutations' (number of mutable positions)

    Returns:
        A list of randomly selected positions that can be mutated
    """
    return random.sample(list(range(params["length"])), params["mutations"])


def _make_masses(
    params: dict[str, object],
    genomes: list[str],
    susceptible_locus: int,
    susceptible_base: str,
) -> list[float]:
    """Generate random masses for specimens.

    Parameters:
        params: Dictionary with 'min_mass' and 'max_mass' parameters
        genomes: List of genome strings
        susceptible_locus: Position that determines susceptibility
        susceptible_base: Base that makes a specimen susceptible

    Returns:
        List of randomly generated mass values between min_mass and max_mass,
        rounded to PRECISION decimal places
    """
    min_mass = params["min_mass"]
    max_mass = params["max_mass"]
    return [round(random.uniform(min_mass, max_mass), utils.PRECISION) for _ in genomes]


def _make_reference_genome(params: dict[str, object]) -> str:
    """Make a random reference genome.

    Parameters:
        params: Dictionary with 'length' parameter for the genome length

    Returns:
        A randomly generated genome string of the specified length
    """
    return "".join(random.choices(BASES, k=params["length"]))

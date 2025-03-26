"""Test specimen generation."""

import csv
import io
import pytest
import random

from snailz import specimens_generate
from snailz.specimens import BASES, specimens_to_csv, Point, Individual, Specimens

from utils import SPECIMEN_PARAMS, check_params_stored


@pytest.mark.parametrize(
    "name, value",
    [
        ("length", 0),
        ("max_mass", 0.5 * SPECIMEN_PARAMS["min_mass"]),
        ("min_mass", -1.0),
        ("mutations", SPECIMEN_PARAMS["length"] * 2),
        ("number", 0),
    ],
)
def test_specimens_fail_bad_parameter_value(name, value):
    params = {**SPECIMEN_PARAMS, name: value}
    with pytest.raises(ValueError):
        specimens_generate(params)


def test_specimens_fail_missing_parameter():
    params = {k: v for k, v in SPECIMEN_PARAMS.items() if k != "length"}
    with pytest.raises(ValueError):
        specimens_generate(params)


def test_specimens_fail_extra_parameter():
    params = {**SPECIMEN_PARAMS, "extra": 1.0}
    with pytest.raises(ValueError):
        specimens_generate(params)


@pytest.mark.parametrize("seed", [127893, 47129, 990124, 512741, 44109318])
def test_specimens_valid_result(seed):
    random.seed(seed)
    result = specimens_generate(SPECIMEN_PARAMS)
    check_params_stored(SPECIMEN_PARAMS, result)

    # Check specimens have correct structure
    assert len(result.reference) == result.params["length"]
    assert len(result.individuals) == result.params["number"]
    assert all(len(ind.genome) == result.params["length"] for ind in result.individuals)
    assert 0 <= result.susceptible_locus < result.params["length"]
    assert result.susceptible_base in BASES
    assert all(
        result.params["min_mass"] <= ind.mass <= result.params["max_mass"]
        for ind in result.individuals
    )

    # Check identifiers
    identifiers = [ind.ident for ind in result.individuals]
    assert all(len(ident) == 6 for ident in identifiers)
    assert all(ident[:2] == identifiers[0][:2] for ident in identifiers)
    assert identifiers[0][:2].isalpha() and identifiers[0][:2].isupper()
    assert len(set(identifiers)) == len(identifiers)
    for ident in identifiers:
        suffix = ident[2:]
        assert len(suffix) == 4
        assert all(c.isupper() or c.isdigit() for c in suffix)


@pytest.fixture
def output_specimens():
    """Create a small test specimen dataset."""
    individuals = [
        Individual(genome="ACGT", ident="AB1234", mass=1.5, site=Point(x=1, y=2)),
        Individual(genome="TGCA", ident="AB5678", mass=1.8, site=Point(x=3, y=4)),
    ]
    return Specimens(
        individuals=individuals,
        loci=[0, 1, 2],
        params={"length": 4, "seed": 12345},
        reference="ACGT",
        susceptible_base="A",
        susceptible_locus=0,
    )


def test_specimens_to_csv_stdout(fs, capsys, output_specimens):
    """Test exporting specimens to CSV on stdout."""
    # Run the function with None as filename (stdout)
    specimens_to_csv(output_specimens, None)

    # Parse the CSV output
    captured = capsys.readouterr()
    rows = list(csv.reader(io.StringIO(captured.out)))

    # Check the output
    assert len(rows) == 3
    assert rows[0] == ["ident", "x", "y", "genome", "mass"]
    assert rows[1] == ["AB1234", "1", "2", "ACGT", "1.5"]
    assert rows[2] == ["AB5678", "3", "4", "TGCA", "1.8"]


def test_specimens_to_csv_file(fs, output_specimens):
    """Test exporting specimens to CSV file."""
    test_file = "/output.csv"
    specimens_to_csv(output_specimens, test_file)
    assert fs.exists(test_file)

    with open(test_file, "r", newline="") as stream:
        rows = list(csv.reader(stream))
    assert len(rows) == 3
    assert rows[0] == ["ident", "x", "y", "genome", "mass"]
    assert rows[1] == ["AB1234", "1", "2", "ACGT", "1.5"]
    assert rows[2] == ["AB5678", "3", "4", "TGCA", "1.8"]

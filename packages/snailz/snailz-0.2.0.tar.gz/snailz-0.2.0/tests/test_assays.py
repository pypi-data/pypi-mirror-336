"""Test assay generation."""

import csv
import pytest
import random
from datetime import date

from snailz import assays_generate, specimens_generate, people_generate
from snailz.assays import ASSAYS_SUBDIR, assays_check, assays_to_csv, Assay, Assays
from snailz.specimens import BASES, Specimens, Individual, Point

from utils import (
    ASSAY_PARAMS,
    SPECIMEN_PARAMS,
    PEOPLE_PARAMS,
    check_params_stored,
    convert_assay_dates,
)


@pytest.mark.parametrize(
    "name, value",
    [
        ("baseline", 0),
        ("baseline", -1.5),
        ("mutant", 0),
        ("mutant", -2.0),
        ("noise", 0),
        ("noise", -0.1),
        ("plate_size", 0),
        ("plate_size", -3),
    ],
)
def test_assays_fail_bad_parameter_value(name, value):
    """Test assay generation fails with invalid parameter values."""
    params = {**ASSAY_PARAMS, name: value}
    convert_assay_dates(params)
    with pytest.raises(ValueError):
        assays_check(params)


def test_assays_fail_date_order():
    """Test assay generation fails when end date is before start date."""
    params = {**ASSAY_PARAMS, "start_date": "2025-01-01", "end_date": "2024-01-01"}
    convert_assay_dates(params)
    with pytest.raises(ValueError):
        assays_check(params)


def test_assays_fail_missing_parameter():
    """Test assay generation fails with missing parameters."""
    for key in ASSAY_PARAMS:
        params = {k: v for k, v in ASSAY_PARAMS.items() if k != key}
        with pytest.raises(ValueError):
            assays_check(params)


def test_assays_fail_extra_parameter():
    """Test assay generation fails with extra parameters."""
    params = {**ASSAY_PARAMS, "extra": 1.0}
    convert_assay_dates(params)
    with pytest.raises(ValueError):
        assays_check(params)


@pytest.mark.parametrize("seed", [127893, 47129, 990124])
def test_assays_valid_result(seed):
    """Test that assay generation returns the expected structure."""
    random.seed(seed)

    # Prepare parameters
    params = {**ASSAY_PARAMS, "seed": seed}
    convert_assay_dates(params)

    # Generate specimens and people for assays
    specimens = specimens_generate(SPECIMEN_PARAMS)
    people = people_generate(PEOPLE_PARAMS)

    # Generate assays
    result = assays_generate(params, specimens, people)
    check_params_stored(params, result)

    # Check result has correct structure
    assert hasattr(result, "items")
    assert isinstance(result.items, list)

    # Check number of assays matches number of specimens
    assert len(result.items) == len(specimens.individuals)

    # Check each assay
    for assay in result.items:
        # Check date is within range
        assert params["start_date"] <= assay.performed <= params["end_date"]

        # Check identifier format
        assert len(assay.ident) == len(result.items[0].ident)
        assert assay.ident.isdigit()

        # Check plate structure
        assert len(assay.treatments) == params["plate_size"]
        assert len(assay.readings) == params["plate_size"]
        for row in range(params["plate_size"]):
            assert len(assay.treatments[row]) == params["plate_size"]
            assert len(assay.readings[row]) == params["plate_size"]
            for treatment in assay.treatments[row]:
                assert treatment in ["S", "C"]


def test_assay_reading_values():
    """Test that assay readings follow the specified distributions."""
    random.seed(ASSAY_PARAMS["seed"])

    # Prepare parameters with controlled values for easier testing
    params = {**ASSAY_PARAMS}
    params["baseline"] = 5.0
    params["mutant"] = 20.0
    params["noise"] = 1.0
    convert_assay_dates(params)

    # Create a controlled specimen with known susceptibility
    susc_locus = 3
    reference = "ACGTACGTACGTACG"
    susc_base = reference[susc_locus]

    # Create two specimens: one susceptible, one not
    susceptible_individual = Individual(
        genome=reference,  # Has the susceptible base at the susceptible locus
        ident="AB1234",
        mass=1.0,
        site=Point(),
    )

    # Modify a copy of the reference genome to not have the susceptible base
    non_susceptible_genome = list(reference)
    non_susceptible_genome[susc_locus] = next(b for b in BASES if b != susc_base)
    non_susceptible_individual = Individual(
        genome="".join(non_susceptible_genome), ident="AB5678", mass=1.0, site=Point()
    )

    specimens = Specimens(
        individuals=[susceptible_individual, non_susceptible_individual],
        loci=[susc_locus],
        params=SPECIMEN_PARAMS,
        reference=reference,
        susceptible_base=susc_base,
        susceptible_locus=susc_locus,
    )

    # Create mock people data
    people = people_generate(PEOPLE_PARAMS)

    # Generate assays with fixed random seed for reproducibility
    result = assays_generate(params, specimens, people)

    # Test reading values for susceptible specimen
    susceptible_assay = result.items[0]
    for row in range(params["plate_size"]):
        for col in range(params["plate_size"]):
            if susceptible_assay.treatments[row][col] == "C":
                # Control cells should have values between 0 and noise
                assert 0 <= susceptible_assay.readings[row][col] <= params["noise"]
            else:
                # Susceptible cells should have mutant value plus scaled noise
                reading = susceptible_assay.readings[row][col]
                scaled_noise = params["noise"] * params["mutant"] / params["baseline"]
                assert params["mutant"] <= reading <= params["mutant"] + scaled_noise

    # Test reading values for non-susceptible specimen
    non_susceptible_assay = result.items[1]
    for row in range(params["plate_size"]):
        for col in range(params["plate_size"]):
            if non_susceptible_assay.treatments[row][col] == "C":
                # Control cells should have values between 0 and noise
                assert 0 <= non_susceptible_assay.readings[row][col] <= params["noise"]
            else:
                # Non-susceptible cells should have baseline value plus noise
                reading = non_susceptible_assay.readings[row][col]
                assert (
                    params["baseline"]
                    <= reading
                    <= params["baseline"] + params["noise"]
                )


@pytest.fixture
def sample_assay():
    """Create a sample assay for testing CSV output."""
    return Assay(
        performed=date(2023, 1, 15),
        ident="123456",
        specimen_id="AB1234",
        person_id="ab0123",
        readings=[
            [1.5, 2.5, 3.5],
            [4.5, 5.5, 6.5],
            [7.5, 8.5, 9.5],
        ],
        treatments=[
            ["S", "C", "S"],
            ["C", "S", "C"],
            ["S", "C", "S"],
        ],
    )


@pytest.fixture
def sample_assays(sample_assay):
    """Create a sample Assays instance with multiple assays."""
    # Create a second assay with different values
    second_assay = Assay(
        performed=date(2023, 2, 20),
        ident="789012",
        specimen_id="AB5678",
        person_id="cd4567",
        readings=[
            [0.5, 1.0, 1.5],
            [2.0, 2.5, 3.0],
            [3.5, 4.0, 4.5],
        ],
        treatments=[
            ["C", "S", "C"],
            ["S", "C", "S"],
            ["C", "S", "C"],
        ],
    )

    return Assays(
        items=[sample_assay, second_assay],
        params={"plate_size": 3, "seed": 12345},
    )


def test_assays_to_csv_stdout(capsys, sample_assays):
    """Test writing assays to CSV on stdout."""
    # Select just the first assay by its ID
    assays_to_csv(sample_assays, None, sample_assays.items[0].ident)

    # Capture stdout
    captured = capsys.readouterr()
    stdout = captured.out

    # Verify that the stdout contains the expected data
    # We should find the assay ID in the output
    assert sample_assays.items[0].ident in stdout

    # We should find the specimen ID in the output
    assert sample_assays.items[0].specimen_id in stdout

    # We should find the date in the output
    assert "2023-01-15" in stdout

    # We should find the person ID in the output
    assert sample_assays.items[0].person_id in stdout

    # Check for column headers
    assert ",A,B,C" in stdout

    # Check for row numbers and data
    assert "1,S,C,S" in stdout  # treatments
    assert "1,1.5,2.5,3.5" in stdout  # readings

    # Ensure we have both files in the output
    assert f"{sample_assays.items[0].ident}_design.csv" in stdout
    assert f"{sample_assays.items[0].ident}_assay.csv" in stdout

    # When a specific ID is provided, the summary file should not be in the output
    assert "assays.csv" not in stdout


def test_assays_to_csv_files(fs, sample_assays):
    """Test writing assays to CSV files."""
    # Create test directory
    test_dir = "/test_output"
    fs.create_dir(test_dir)

    # Write all assays to files
    assays_to_csv(sample_assays, test_dir)

    # Check if summary file was created
    summary_file = f"{test_dir}/assays.csv"
    assert fs.exists(summary_file)

    # Check summary file contents
    with open(summary_file, "r", newline="") as f:
        summary_rows = list(csv.reader(f))
        assert summary_rows[0] == ["ident", "specimen_id", "performed", "performed_by"]
        assert (
            len(summary_rows) == len(sample_assays.items) + 1
        )  # header row + one row per assay

        # Check each assay entry in the summary
        for i, assay in enumerate(sample_assays.items, 1):
            assert summary_rows[i][0] == assay.ident
            assert summary_rows[i][1] == assay.specimen_id
            assert summary_rows[i][2] == assay.performed.isoformat()
            assert summary_rows[i][3] == assay.person_id

    # Check if assays subdirectory was created
    assays_subdir = f"{test_dir}/{ASSAYS_SUBDIR}"
    assert fs.exists(assays_subdir)

    # Check files were created for both assays in the assays subdirectory
    for assay in sample_assays.items:
        design_file = f"{test_dir}/{ASSAYS_SUBDIR}/{assay.ident}_design.csv"
        assay_file = f"{test_dir}/{ASSAYS_SUBDIR}/{assay.ident}_assay.csv"

        assert fs.exists(design_file)
        assert fs.exists(assay_file)

        # Check design file
        with open(design_file, "r", newline="") as f:
            design_rows = list(csv.reader(f))

            # Check the first elements (the rest will be padding)
            assert design_rows[0][:2] == ["id", assay.ident]
            assert design_rows[1][:2] == ["specimen", assay.specimen_id]
            assert design_rows[2][:2] == ["performed", assay.performed.isoformat()]
            assert design_rows[3][:2] == ["performed_by", assay.person_id]
            # Column headers (may have padding)
            assert design_rows[4][:4] == ["", "A", "B", "C"]

            # Check data rows
            for i, row in enumerate(
                assay.treatments, 5
            ):  # Starting at 5 because of additional header line
                assert design_rows[i][0] == str(i - 4)  # Row number
                assert (
                    design_rows[i][1 : len(row) + 1] == row
                )  # Check just the data part, not padding

        # Check assay file
        with open(assay_file, "r", newline="") as f:
            reading_rows = list(csv.reader(f))

            # Check the first elements (the rest will be padding)
            assert reading_rows[0][:2] == ["id", assay.ident]
            assert reading_rows[1][:2] == ["specimen", assay.specimen_id]
            assert reading_rows[2][:2] == ["performed", assay.performed.isoformat()]
            assert reading_rows[3][:2] == ["performed_by", assay.person_id]
            # Column headers (may have padding)
            assert reading_rows[4][:4] == ["", "A", "B", "C"]

            # Check data rows
            for i, row in enumerate(
                assay.readings, 5
            ):  # Starting at 5 because of additional header line
                assert reading_rows[i][0] == str(i - 4)  # Row number
                data_vals = [float(val) for val in reading_rows[i][1 : len(row) + 1]]
                assert data_vals == row


def test_assays_to_csv_specific_ident(fs, sample_assays):
    """Test writing only a specific assay to CSV."""
    # Create test directory
    test_dir = "/test_output"
    fs.create_dir(test_dir)

    # Get the ID of the second assay
    second_assay_id = sample_assays.items[1].ident

    # Write only the second assay to files
    assays_to_csv(sample_assays, test_dir, second_assay_id)

    # Check if assays subdirectory exists
    assays_subdir = f"{test_dir}/{ASSAYS_SUBDIR}"
    assert fs.exists(assays_subdir)

    # First assay's files should not exist
    first_assay_design = (
        f"{test_dir}/{ASSAYS_SUBDIR}/{sample_assays.items[0].ident}_design.csv"
    )
    assert not fs.exists(first_assay_design)

    # Second assay's files should exist
    second_assay_design = f"{test_dir}/{ASSAYS_SUBDIR}/{second_assay_id}_design.csv"
    second_assay_assay = f"{test_dir}/{ASSAYS_SUBDIR}/{second_assay_id}_assay.csv"
    assert fs.exists(second_assay_design)
    assert fs.exists(second_assay_assay)

    # Summary file should not exist when specific ident is provided
    summary_file = f"{test_dir}/assays.csv"
    assert not fs.exists(summary_file)


def test_assays_to_csv_invalid_ident(sample_assays):
    """Test error is raised when an invalid assay ID is provided."""
    with pytest.raises(ValueError, match="No assay with ID"):
        assays_to_csv(sample_assays, None, "non_existent_id")

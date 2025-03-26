"""Test people generation."""

import pytest
import random

from snailz.people import people_generate, people_check

from utils import PEOPLE_PARAMS, check_params_stored


@pytest.mark.parametrize(
    "name, value",
    [
        ("number", 0),
        ("number", -5),
        ("locale", ""),
    ],
)
def test_people_fail_bad_parameter_value(name, value):
    """Test people generation fails with invalid parameter values."""
    params = {**PEOPLE_PARAMS, name: value}
    with pytest.raises(ValueError):
        people_check(params)


def test_people_fail_missing_parameter():
    """Test people generation fails with missing parameters."""
    params = {k: v for k, v in PEOPLE_PARAMS.items() if k != "locale"}
    with pytest.raises(ValueError):
        people_check(params)


def test_people_fail_extra_parameter():
    """Test people generation fails with extra parameters."""
    params = {**PEOPLE_PARAMS, "extra": 1.0}
    with pytest.raises(ValueError):
        people_check(params)


@pytest.mark.parametrize("seed", [127893, 47129, 990124, 512741, 44109318])
def test_people_valid_result(seed):
    """Test that people generation returns the expected structure."""
    random.seed(seed)
    params = {**PEOPLE_PARAMS, "seed": seed}
    result = people_generate(params)
    check_params_stored(params, result)

    # Check result has correct structure
    assert hasattr(result, "individuals")
    assert isinstance(result.individuals, list)

    # Check that the individuals list has the right number of people
    assert len(result.individuals) == PEOPLE_PARAMS["number"]

    # Check that all individuals have personal and family names
    for person in result.individuals:
        assert person.personal
        assert person.family
        assert isinstance(person.personal, str)
        assert isinstance(person.family, str)

        # Check that the ident has the correct format
        assert len(person.ident) == 6
        assert person.ident[:2] == (person.family[0] + person.personal[0]).lower()
        assert person.ident[2:].isdigit()
        assert len(person.ident[2:]) == 4

    # Check that all identifiers are unique
    identifiers = [person.ident for person in result.individuals]
    assert len(set(identifiers)) == len(identifiers)

    # Check that new seed is stored
    assert result.params["seed"] == seed

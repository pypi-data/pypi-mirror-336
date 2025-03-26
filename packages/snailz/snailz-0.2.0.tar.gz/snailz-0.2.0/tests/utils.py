"""Test utilities."""

from datetime import date

ASSAY_PARAMS = {
    "baseline": 1.0,
    "end_date": "2023-12-31",
    "mutant": 10.0,
    "noise": 0.1,
    "plate_size": 4,
    "seed": 4712389,
    "start_date": "2023-01-01",
}

GRID_PARAMS = {
    "depth": 8,
    "seed": 7421398,
    "size": 15,
}

PEOPLE_PARAMS = {
    "locale": "et_EE",
    "number": 15,
    "seed": 9812374,
}

SPECIMEN_PARAMS = {
    "length": 15,
    "max_mass": 33.0,
    "min_mass": 15.0,
    "mut_scale": 0.5,
    "mutations": 3,
    "number": 20,
    "seed": 4712389,
}


def check_params_stored(params, result):
    """Check that params are properly stored."""
    for key, value in params.items():
        assert key in result.params, f"key {key} missing"
        assert result.params[key] == value, (
            f"result.params[{key}] is {result.params[key]} not {value}"
        )


def convert_assay_dates(params):
    """Make sure start_date and end_date are date objects."""
    for name in ("start_date", "end_date"):
        if name in params:
            params[name] = date.fromisoformat(params[name])

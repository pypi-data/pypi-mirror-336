"""Utilities."""

from dataclasses import asdict
from datetime import date
import json
import sys

from dacite import from_dict


# Decimal places in floating-point values.
PRECISION = 2


class UniqueIdGenerator:
    """Generate unique IDs using provided function."""

    def __init__(self, name: str, func: callable, limit: int = 10000) -> None:
        """Initialize the UniqueIdGenerator.

        Parameters:
            name: A name for this generator (used in error messages)
            func: Function that creates IDs when called
            limit: Maximum number of attempts to find a unique ID
        """
        self._name = name
        self._func = func
        self._seen = set()
        self._limit = limit

    def next(self, *args: object) -> str:
        """Get next unique ID.

        Parameters:
            *args: Arguments to pass to the ID-generating function

        Returns:
            A unique identifier that hasn't been returned before

        Raises:
            RuntimeError: If unable to generate a unique ID within limit attempts
        """
        for i in range(self._limit):
            ident = self._func(*args)
            if ident in self._seen:
                continue
            self._seen.add(ident)
            return ident
        raise RuntimeError(f"failed to find unique ID for {self._name}")


def check_keys_and_types(spec: dict[str, type], actual: dict[str, object]) -> None:
    """Check that parameters have all and only required keys with correct types.

    Parameters:
        spec: Dictionary with parameter names as keys and expected types as values
        actual: Dictionary with parameter names and their actual values

    Raises:
        ValueError: If any parameters are missing, extra parameters are present,
                   or parameters have the wrong type
    """

    missing = set(spec.keys()) - set(actual.keys())
    require(not missing, f"Missing parameter(s): {list(sorted(missing))}")

    extra = set(actual.keys()) - set(spec.keys())
    require(not extra, f"Extra parameter(s): {list(sorted(extra))}")

    for key, required_type in spec.items():
        require(
            isinstance(actual[key], required_type),
            f"Parameter {key} has wrong type: got {type(actual[key])} expected {required_type}",
        )


def fail(msg: str) -> None:
    """Print message to standard error and exit with status 1.

    Parameters:
        msg: The error message to display

    Note: This function does not return as it exits the program
    """
    print(msg, file=sys.stderr)
    sys.exit(1)


def load_data[T](parameter_name: str, filename: str | None, cls: type[T]) -> T:
    """Construct a dataclass from serialized JSON.

    Parameters:
        parameter_name: Name of the parameter requiring this file (for error messages)
        filename: Path to the JSON file to load
        cls: The dataclass to instantiate with the loaded data

    Returns:
        An instance of cls constructed from the JSON data

    Raises:
        ValueError: If filename is None or empty
        IOError: If the file cannot be read
    """
    require(bool(filename), f"--{parameter_name} is required")
    with open(filename, "r") as reader:
        return from_dict(data_class=cls, data=json.load(reader))


def report_result(output: str | None, result: object) -> None:
    """Save or display result as JSON.

    Parameters:
        output: Path to output file, or None to print to stdout
        result: The dataclass object to serialize as JSON

    Side effects:
        Either writes to the specified output file or prints to stdout
    """
    result_json = json.dumps(asdict(result), default=serialize_values)
    if output:
        with open(output, "w") as writer:
            writer.write(result_json)
    else:
        print(result_json)


def require(cond: bool, msg: str, cls: type = ValueError) -> None:
    """Raise exception if condition not satisfied.

    Parameters:
        cond: The condition to check
        msg: The error message to use if condition is not met
        cls: The exception class to raise (default: ValueError)

    Raises:
        cls: If cond is False or evaluates to a falsy value
    """
    if not cond:
        raise cls(msg)


def serialize_values(obj: object) -> str:
    """Custom JSON serializer for dates.

    Parameters:
        obj: The object to serialize

    Returns:
        String representation of date objects

    Raises:
        TypeError: If the object type is not supported for serialization
    """
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def validate_date(ctx: object, param: object, value: str | None) -> date | None:
    """Validate and convert date string to date object.

    Parameters:
        ctx: Click context object
        param: Click parameter being processed
        value: The value to validate

    Returns:
        None if value is None, otherwise a date object
    """
    return None if value is None else date.fromisoformat(value)

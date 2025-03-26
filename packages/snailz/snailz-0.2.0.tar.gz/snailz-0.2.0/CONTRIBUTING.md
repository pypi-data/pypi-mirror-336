# Contributing

Contributions are very welcome.  Please file issues or submit pull
requests in our GitHub repository.  All contributors will be
acknowledged, but must abide by our Code of Conduct.

## Please

-   Use [Conventional Commits][conventional].
-   [Open an issue][repo] *before* creating a pull request.

## Setup

1.  Fork or clone [the repository][repo].
1.  `uv venv -p 3.12` in the root directory of the project
    to create a virtual environment with Python 3.12.
1.  `source .venv/bin/activate` to activate that virtual environment.
1.  `uv pip install -e ".[dev]" to install an editable version of this
    package along with all its dependencies (including developer
    dependencies).

## Running

1.  `doit list` prints a list of available commands.

[conventional]: https://www.conventionalcommits.org/
[repo]: https://github.com/gvwilson/snailz

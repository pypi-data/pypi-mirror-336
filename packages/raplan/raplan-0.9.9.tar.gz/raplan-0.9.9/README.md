# RaPlan

Ratio maintenance planning and scheduling in Python.

## Quickstart

### Installation

RaPlan can be installed from PyPI using `pip install raplan[all]` for any Python version \>=3.11.
For managed projects, use:

- uv: `uv add raplan[all]`
- Poetry: `poetry add raplan -E all`

### User documentation

The further user documentation is available on
[https://raplan.ratio-case.nl](https://raplan.ratio-case.nl)!

## Development installation

This project is packaged using [uv](https://docs.astral.sh/uv/) as the environment manager and build
frontend. Packaging information as well as dependencies are stored in
[pyproject.toml](./pyproject.toml).

For ease of use, this project uses the [just](https://github.com/casey/just) command runner to
simplify common tasks. Installing the project and its development dependencies can be done by
running `just install` in the cloned repository directory or manually by running `uv sync --all-extras`.

Please consult the [justfile](./justfile) for the underlying commands or run `just` to display a
list of all available commands.

### Tests

Tests can be run using `just test` and subsequent arguments will be passed to pytest.

### Linting

Linting the project can be done using `just lint`, automatic fixes can be applied using `just fix`.
Linting config is included in [pyproject.toml](./pyproject.toml) for Ruff.

### Documentation

Documentation can be built using `just docs` or served continuously using `just serve-docs` with
the help of [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Contributions and license

To get contributing, feel free to fork, pick up an issue or file your own and get going for your
first merge! We'll be more than happy to help.

For contribution instructions, head over to [CONTRIBUTING.md](./CONTRIBUTING.md).

RaPlan is licensed following a dual licensing model. In short, we want to provide anyone that
wishes to use our published software under the GNU GPLv3 to do so freely and without any further
limitation. The GNU GPLv3 is a strong copyleft license that promotes the distribution of free,
open-source software. In that spirit, it requires dependent pieces of software to follow the same
route. This might be too restrictive for some. To accommodate users with specific requirements
regarding licenses, we offer a proprietary license. The terms can be discussed by reaching out to
Ratio.

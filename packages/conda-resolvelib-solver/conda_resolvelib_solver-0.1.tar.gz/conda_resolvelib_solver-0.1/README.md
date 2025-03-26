# conda-resolvelib-solver

[Resolvelib](https://github.com/sarugaku/resolvelib) based conda solver. A pure python conda solver!


## What is this?

Conda-resolvelib-solver is a demostration solver for the
[conda package manager](https://docs.conda.io/) which uses the
[resolvelib](https://github.com/sarugaku/resolvelib) library,
a pure python dependency resolver that is used by
[pip](https://pip.pypa.io/en/stable/).


## Installation

To install `conda-resolvelib-solver` use:

```
conda install --name base --channel conda-forge conda-resolvelib-solver
```

Or with the `base` environment activated install using pip:

```
python -m pip install conda-resolvelib-solver
```


## Usage

Once installed the solver can be used by adding `--solver resolvelib` to a `conda create` command.

Note that the solver may fail for complex dependencies, commands other than `create` and does not
implement many configuration values of conda like channel priority.

Use as a general solver in conda is not recommended.


## Development workflow

To setup a development environment use:

```
conda create --prefix ./env --file dev/conda-requirements.txt
conda activate ./env
python -m pip install -e .
```

Conda commands can now be run from this environment using:

```
python -m conda <command>
```

Tests can be run using

```
python -m pytest tests
```

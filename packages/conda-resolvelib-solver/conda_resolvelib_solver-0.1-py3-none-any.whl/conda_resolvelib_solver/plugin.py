# Copyright (C) 2025 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""
Entry points for the conda plugin system
"""

from conda import plugins

from .solver import ResolveLibSolver


@plugins.hookimpl
def conda_solvers():
    """The conda plugin hook implementation to load the solver into conda."""
    yield plugins.CondaSolver(
        name="resolvelib",
        backend=ResolveLibSolver,
    )

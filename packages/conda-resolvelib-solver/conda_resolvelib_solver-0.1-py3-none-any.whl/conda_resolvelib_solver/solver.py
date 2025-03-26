# Copyright (C) 2025 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""
Define the conda.core.solve.Solver interface and solver implementation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from boltons.setutils import IndexedSet
from conda.common.constants import NULL
from conda.core.index import Index
from conda.core.solve import Solver
from conda.models.match_spec import MatchSpec
from conda.models.prefix_graph import PrefixGraph
from conda.models.version import VersionOrder
from resolvelib import AbstractProvider, BaseReporter, Resolver

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping
    from typing import Any

    from conda.auxlib import _Null
    from conda.base.constants import DepsModifier, UpdateModifier
    from conda.models.records import PackageRecord


class ResolveLibSolver(Solver):
    MAX_ROUNDS = 1_000

    def solve_final_state(
        self,
        update_modifier: UpdateModifier | _Null = NULL,
        deps_modifier: DepsModifier | _Null = NULL,
        prune: bool | _Null = NULL,
        ignore_pinned: bool | _Null = NULL,
        force_remove: bool | _Null = NULL,
        should_retry_solve: bool = False,
    ) -> IndexedSet[PackageRecord]:
        # This skips a lot of checks and behaviors that a proper solver should implement.
        if self._command != "create":
            raise ValueError("resolvelib solver only supports the 'create' command")
        index = Index(
            channels=self.channels,
            subdirs=self.subdirs,
            repodata_fn="repodata.json",
            use_system=True,
        )
        provider = CondaProvider(index)
        reporter = BaseReporter()
        resolver = Resolver(provider, reporter)
        requirements = self.specs_to_add
        solution = resolver.resolve(requirements, max_rounds=self.MAX_ROUNDS)
        return IndexedSet(PrefixGraph(solution.mapping.values()).graph)


class CondaProvider(AbstractProvider):
    def __init__(self, index: Index) -> None:
        self.index = index

    def identify(self, requirement_or_candidate: MatchSpec | PackageRecord) -> str:
        return requirement_or_candidate.name

    def get_preference(
        self,
        identifier: str,
        resolutions: Mapping[str, PackageRecord],
        candidates: Mapping[str, Iterator[PackageRecord]],
        information: Any,
        backtrack_causes: Any,
    ) -> int:
        return 1

    def find_matches(
        self,
        identifier: str,
        requirements: Mapping[str, Iterator[MatchSpec]],
        incompatibilities: Mapping[str, Iterator[PackageRecord]],
    ) -> Iterable[PackageRecord]:
        candidates = self.index._retrieve_all_from_channels(MatchSpec(identifier))
        for mspec in requirements[identifier]:
            candidates = [prec for prec in candidates if mspec.match(prec)]
        incompatible_precs = set(incompatibilities[identifier])
        candidates = [prec for prec in candidates if prec not in incompatible_precs]
        candidates.sort(key=lambda rec: (VersionOrder(rec.version), rec.build))
        candidates.reverse()
        return candidates

    def is_satisfied_by(self, requirement: MatchSpec, candidate: PackageRecord) -> bool:
        return requirement.match(candidate)

    def get_dependencies(self, candidate: PackageRecord) -> Iterable[MatchSpec]:
        return [MatchSpec(dep) for dep in candidate.depends]

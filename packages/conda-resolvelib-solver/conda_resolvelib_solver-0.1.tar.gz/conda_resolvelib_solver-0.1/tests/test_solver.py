from pathlib import Path

from conda.base.context import context
from conda.models.match_spec import MatchSpec

from conda_resolvelib_solver.solver import ResolveLibSolver

TEST_CHANNEL = str(Path(__file__).parent / "repo")


def solve_for_matchspec(matchspec: MatchSpec):
    context.__init__()
    solver = ResolveLibSolver(
        prefix="/fake/fake/fake",
        channels=(TEST_CHANNEL,),
        specs_to_add=(matchspec,),
        command="create",
    )
    solution = solver.solve_final_state()
    return solution


def test_solve_select_highest_version():
    solution = solve_for_matchspec(MatchSpec("bar"))
    assert len(solution) == 1
    assert solution[0].name == "bar"
    assert solution[0].version == "3.0.0"


def test_solve_select_highest_version_with_constraint():
    solution = solve_for_matchspec(MatchSpec("bar<3"))
    assert len(solution) == 1
    assert solution[0].name == "bar"
    assert solution[0].version == "2.0.0"


def test_solve_depends():
    solution = solve_for_matchspec(MatchSpec("foo"))
    assert len(solution) == 2
    assert solution[0].name == "bar"
    assert solution[0].version == "2.0.0"
    assert solution[1].name == "foo"
    assert solution[1].version == "2.1.0"


def test_solve_depends_with_constraints():
    solution = solve_for_matchspec(MatchSpec("foo<2"))
    assert len(solution) == 2
    assert solution[0].name == "bar"
    assert solution[0].version == "1.0.0"
    assert solution[1].name == "foo"
    assert solution[1].version == "1.1.0"

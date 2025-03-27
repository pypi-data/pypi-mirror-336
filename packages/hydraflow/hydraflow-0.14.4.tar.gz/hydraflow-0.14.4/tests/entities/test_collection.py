from pathlib import Path

import mlflow
import pytest
from mlflow.entities import Experiment, Run, RunStatus

from hydraflow.core.mlflow import list_runs
from hydraflow.entities.run_collection import RunCollection, filter_runs

pytestmark = pytest.mark.xdist_group(name="group3")


@pytest.fixture(scope="module")
def experiment(experiment_name: str):
    experiment = mlflow.set_experiment(experiment_name)

    for x in range(6):
        with mlflow.start_run(run_name=f"{x}"):
            mlflow.log_param("p", x)
            mlflow.log_param("q", 0 if x < 5 else None)
            mlflow.log_param("r", x % 3)
            mlflow.log_text(f"{x}", "abc.txt")

    return experiment


@pytest.fixture
def runs(experiment: Experiment):
    runs = mlflow.search_runs([experiment.experiment_id], output_format="list")
    return list(reversed(runs))


def test_start_time(runs: list[Run]):
    start_times = [run.info.start_time for run in runs]
    assert start_times == sorted(start_times)


@pytest.fixture
def rc(runs: list[Run]):
    return RunCollection(runs)


def test_bool_false():
    assert not RunCollection([])
    assert bool(RunCollection([])) is False


def test_bool_true(rc: RunCollection):
    assert rc
    assert bool(rc) is True


def test_len(rc: RunCollection):
    assert len(rc) == 6


def test_from_list(runs: list[Run]):
    rc = RunCollection(runs)
    assert len(rc) == len(runs)
    assert all(run in rc for run in runs)


def test_add(runs: list[Run]):
    rc1 = RunCollection(runs[:3])
    rc2 = RunCollection(runs[3:])
    rc = rc1 + rc2
    assert rc._runs == runs


def test_sub(runs: list[Run]):
    rc1 = RunCollection(runs)
    rc2 = RunCollection(runs[3:])
    rc = rc1 - rc2
    assert rc._runs == runs[:3]


def test_search_runs_sorted(runs: list[Run]):
    assert [run.data.params["p"] for run in runs] == ["0", "1", "2", "3", "4", "5"]


def test_filter_none(runs: list[Run]):
    assert runs == filter_runs(runs)


def test_filter_dict_one(runs: list[Run]):
    assert len(filter_runs(runs, {"p": 1})) == 1


def test_filter_kwarg_one(runs: list[Run]):
    assert len(filter_runs(runs, p=1)) == 1


def test_filter_list_one(runs: list[Run]):
    assert len(filter_runs(runs, ["p=1"])) == 1


def test_filter_dict_rest(runs: list[Run]):
    assert len(filter_runs(runs, {"q": 0})) == 5


def test_filter_kwarg_rest(runs: list[Run]):
    assert len(filter_runs(runs, q=0)) == 5


def test_filter_list_rest(runs: list[Run]):
    assert len(filter_runs(runs, ["q=0"])) == 5


def test_filter_list(runs: list[Run]):
    assert len(filter_runs(runs, p=[0, 4, 5])) == 3


def test_filter_tuple(runs: list[Run]):
    assert len(filter_runs(runs, p=(1, 3))) == 3


def test_filter_kwarg_none(runs: list[Run]):
    assert not filter_runs(runs, {"invalid": 0})


def test_filter_list_none(runs: list[Run]):
    assert not filter_runs(runs, ["invalid=0"])


def test_filter_callable(runs: list[Run]):
    runs = filter_runs(runs, lambda run: run.data.params["r"] == "0")
    assert len(runs) == 2
    assert all(run.data.params["q"] == "0" for run in runs)


@pytest.mark.parametrize(
    ("status", "n"),
    [
        ("RUNNING", 0),
        ("finished", 6),
        (["finished", "running"], 6),
        ("!RUNNING", 6),
        ("!finished", 0),
        (RunStatus.RUNNING, 0),
        (RunStatus.FINISHED, 6),
        ([RunStatus.FINISHED, RunStatus.RUNNING], 6),
    ],
)
def test_filter_status(runs: list[Run], status, n):
    assert len(filter_runs(runs, status=status)) == n


@pytest.mark.parametrize(
    ("select", "n"),
    [(None, 0), (["p"], 3), (["q"], 0), (["r"], 0)],
)
def test_filter_select(runs: list[Run], select, n):
    cfg = {"p": [0, 4, 5], "q": -1}
    assert len(filter_runs(runs, cfg, select=select)) == n


@pytest.mark.parametrize(
    ("overrides", "n"),
    [(["p=4"], 3), (["q=1000"], 5), (["r=1"], 0)],
)
def test_filter_overrides(runs: list[Run], overrides, n):
    cfg = {"p": [0, 4, 5], "q": 0}
    assert len(filter_runs(runs, cfg, overrides=overrides)) == n


def test_get_params(runs: list[Run]):
    from hydraflow.core.param import get_params

    assert get_params(runs[1], "p") == ("1",)
    assert get_params(runs[2], "p", "q") == ("2", "0")
    assert get_params(runs[3], ["p", "q"]) == ("3", "0")
    assert get_params(runs[4], "p", ["q", "r"]) == ("4", "0", "1")
    assert get_params(runs[5], ["a", "q"], "r") == (None, "None", "2")


def test_get_values(runs: list[Run]):
    from hydraflow.core.param import get_values

    assert get_values(runs[3], ["p", "q"], [int, int]) == (3, 0)


@pytest.mark.parametrize("i", range(6))
def test_chdir_artifact_list(runs: list[Run], i):
    from hydraflow.core.context import chdir_artifact

    with chdir_artifact(runs[i]):
        assert Path("abc.txt").read_text() == f"{i}"

    assert not Path("abc.txt").exists()


def test_repr(rc: RunCollection):
    assert repr(rc) == "RunCollection(6)"


def test_first(rc: RunCollection):
    run = rc.first()
    assert isinstance(run, Run)
    assert run.data.params["p"] == "0"


def test_first_empty():
    with pytest.raises(ValueError):
        RunCollection([]).first()


def test_try_first_empty():
    assert RunCollection([]).try_first() is None


def test_last(rc: RunCollection):
    run = rc.last()
    assert isinstance(run, Run)
    assert run.data.params["p"] == "5"


def test_last_empty():
    with pytest.raises(ValueError):
        RunCollection([]).last()


def test_try_last_empty():
    assert RunCollection([]).try_last() is None


def test_rc_filter_empty(rc: RunCollection):
    assert len(rc.filter()) == 6
    assert len(rc.filter({})) == 6
    assert len(rc.filter([])) == 6


def test_rc_filter_one(rc: RunCollection):
    assert len(rc.filter({"p": 1})) == 1
    assert len(rc.filter(["p=1"])) == 1
    assert len(rc.filter(p=5)) == 1


def test_rc_filter_rest(rc: RunCollection):
    assert len(rc.filter({"q": 0})) == 5
    assert len(rc.filter(["q=0"])) == 5
    assert len(rc.filter(q=0)) == 5


def test_rc_filter_none(rc: RunCollection):
    assert not rc.filter({"q": -1})
    assert not rc.filter(["q=-1"])
    assert not rc.filter(q=-1)


@pytest.mark.parametrize("r", [0, 1, 2])
def test_rc_filter_two(rc: RunCollection, r):
    assert len(rc.filter({"r": r})) == 2
    assert len(rc.filter([f"r={r}"])) == 2
    assert len(rc.filter(r=r)) == 2


def test_get_dict(rc: RunCollection):
    assert isinstance(rc.get({"p": 4}), Run)


def test_get_kwarg(rc: RunCollection):
    assert isinstance(rc.get(p=2), Run)


def test_get_list(rc: RunCollection):
    assert isinstance(rc.get(["p=3"]), Run)


def test_get_error(rc: RunCollection):
    with pytest.raises(ValueError):
        rc.get({"p": 10})


def test_get_run_multiple_params(rc: RunCollection):
    run = rc.get({"p": 4, "q": 0})
    assert run.data.params["p"] == "4"
    assert run.data.params["q"] == "0"


def test_try_get_dict(rc: RunCollection):
    assert isinstance(rc.try_get({"p": 5}), Run)


def test_try_get_kwarg(rc: RunCollection):
    assert isinstance(rc.try_get(p=1), Run)


def test_try_get_list(rc: RunCollection):
    assert isinstance(rc.try_get(["p=2"]), Run)


def test_try_get_dict_none(rc: RunCollection):
    assert rc.try_get({"p": -1}) is None


def test_try_get_kwarg_none(rc: RunCollection):
    assert rc.try_get(p=-1) is None


def test_try_get_list_none(rc: RunCollection):
    assert rc.try_get(["p=-2"]) is None


def test_try_get_run_multiple_params(rc: RunCollection):
    run = rc.try_get({"p": 4, "q": 0})
    assert isinstance(run, Run)
    assert run.data.params["p"] == "4"
    assert run.data.params["q"] == "0"


@pytest.mark.parametrize("name", ["p", "q", "r"])
def test_get_param_names(rc: RunCollection, name: str):
    assert name in rc.get_param_names()


@pytest.mark.parametrize(
    ("name", "values"),
    [
        ("p", ["0", "1", "2", "3", "4", "5"]),
        ("q", ["0", "None"]),
        ("r", ["0", "1", "2"]),
    ],
)
def test_get_param_dict(rc: RunCollection, name: str, values: list[str]):
    params = rc.get_param_dict()
    assert params[name] == values


def test_get_param_dict_drop_const(rc: RunCollection):
    params = rc.filter(q=0).get_param_dict(drop_const=True)
    assert len(params) == 2
    assert "p" in params
    assert "q" not in params
    assert "r" in params


@pytest.mark.parametrize("n_jobs", [0, 1, 2])
def test_list_runs(rc: RunCollection, n_jobs: int):
    assert len(list_runs(n_jobs=n_jobs)) == 6


@pytest.mark.parametrize("n_jobs", [0, 1, 2])
def test_list_runs_empty_list(rc: RunCollection, n_jobs: int):
    assert len(list_runs(None, n_jobs=n_jobs)) == 6


@pytest.mark.parametrize("n_jobs", [0, 1, 2])
def test_list_runs_none(rc: RunCollection, n_jobs: int):
    assert not list_runs(["non_existent_experiment"], n_jobs=n_jobs)


def test_iter(rc: RunCollection):
    assert list(rc) == rc._runs


@pytest.mark.parametrize("i", range(6))
def test_run_collection_getitem(rc: RunCollection, i: int):
    assert rc[i] == rc._runs[i]


@pytest.mark.parametrize("i", range(6))
def test_getitem_slice(rc: RunCollection, i: int):
    assert rc[i : i + 2]._runs == rc._runs[i : i + 2]


@pytest.mark.parametrize("i", range(6))
def test_getitem_slice_step(rc: RunCollection, i: int):
    assert rc[i::2]._runs == rc._runs[i::2]


@pytest.mark.parametrize("i", range(6))
def test_getitem_slice_step_neg(rc: RunCollection, i: int):
    assert rc[i::-2]._runs == rc._runs[i::-2]


@pytest.mark.parametrize("i", range(6))
def test_contains(rc: RunCollection, i: int):
    assert rc[i] in rc


@pytest.mark.parametrize(("name", "n"), [("p", 6), ("q", 2), ("r", 3)])
def test_groupby_len(rc: RunCollection, name: str, n: int):
    assert len(rc.groupby(name)) == n


def test_groupby(rc: RunCollection):
    grouped = rc.groupby(["p"])
    assert all(isinstance(group, RunCollection) for group in grouped.values())
    assert all(len(group) == 1 for group in grouped.values())
    assert grouped[("0",)][0] == rc[0]
    assert grouped[("1",)][0] == rc[1]


def test_sort(rc: RunCollection):
    rc.sort(key=lambda x: x.data.params["p"])
    assert [run.data.params["p"] for run in rc] == ["0", "1", "2", "3", "4", "5"]


def test_sort_reverse(rc: RunCollection):
    rc.sort(reverse=True)
    assert [run.data.params["p"] for run in rc] == ["5", "4", "3", "2", "1", "0"]


def test_filter_runs_empty_list():
    assert not filter_runs([], p=[0, 1, 2])


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("p", ["0", "1", "2", "3", "4", "5"]),
        ("q", ["0", "0", "0", "0", "0", "None"]),
        ("r", ["0", "1", "2", "0", "1", "2"]),
    ],
)
def test_data(rc: RunCollection, name, value):
    assert rc.data.params[name] == value

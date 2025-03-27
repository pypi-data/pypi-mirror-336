from pathlib import Path

import pytest
from mlflow.entities import Run

from hydraflow.entities.run_collection import RunCollection

pytestmark = pytest.mark.xdist_group(name="group1")


@pytest.fixture(scope="module")
def rc(collect):
    file = Path(__file__).parent / "params.py"
    return collect(file, ["host=a", "data.y=[10,20,30]"])


@pytest.fixture(scope="module")
def run(rc: RunCollection):
    return rc.one()


def test_get_params_str(run: Run):
    from hydraflow.core.param import get_params

    assert get_params(run, "host") == ("a",)


def test_get_params_dot(run: Run):
    from hydraflow.core.param import get_params

    assert get_params(run, "data.x") == ("[1, 2, 3]",)


def test_get_params_dot_overrides(run: Run):
    from hydraflow.core.param import get_params

    assert get_params(run, "data.y") == ("[10, 20, 30]",)


def test_get_params_list(run: Run):
    from hydraflow.core.param import get_params

    assert get_params(run, ["host"], ["port"]) == ("a", "3306")


def test_get_values(run: Run):
    from hydraflow.core.param import get_values

    assert get_values(run, ["host", "port"], [str, int]) == ("a", 3306)

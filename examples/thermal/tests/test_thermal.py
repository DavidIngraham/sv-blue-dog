"""Application tests for the independently generated SysML calculation."""
import importlib
from pathlib import Path

import numpy as np
import pytest
from sysml_python import Project


@pytest.fixture(scope="module")
def heat():
    Project(Path(__file__).parents[1]/"pyproject.toml").prepare()
    return importlib.import_module("generated").joule_heat


def test_model_default_and_explicit_override(heat):
    assert heat(current=2).power == 40
    assert heat(current=2, resistance=5).power == 20


def test_shared_resistance_and_per_case_current(heat):
    result = heat.batch(shared={"resistance": 5}, cases={"current": [0, 1, 2, 3]})
    np.testing.assert_array_equal(result.values[:, 0], [0, 5, 20, 45])
    assert result.errors == (None,)*4


def test_invalid_inputs_are_rejected(heat):
    with pytest.raises(ValueError, match="finite"):
        heat(current=float("nan"))


def test_model_physical_check_applies_to_overrides(heat):
    with pytest.raises(ValueError, match="positiveResistance"):
        heat(current=2, resistance=-1)

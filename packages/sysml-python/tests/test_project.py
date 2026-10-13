import importlib.util
import os
from pathlib import Path

import numpy as np
import pytest
from sysml_python import Project


@pytest.fixture
def prepared(tmp_path):
    executable = os.environ.get('OPENSYSML_BINARY')
    if not executable:
        pytest.skip('Set OPENSYSML_BINARY to the pinned test compiler')
    source = tmp_path/'example.sysml'
    source.write_text("package Example { private import ScalarValues::*; calc def Heat { in current : Real; in resistance : Real; return power : Real = current * current * resistance; } }")
    config = tmp_path/'pyproject.toml'
    config.write_text('''[tool.sysml_python]
models = ["*.sysml"]
generated_package = "generated"
[tool.sysml_python.exports.heat]
definition = "Example::Heat"
''')
    project = Project(config, executable=executable)
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('generated_test', package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return project, source, module


def test_typed_scalar_batch_and_no_implicit_broadcast(prepared):
    _, _, module = prepared
    assert module.heat(current=2, resistance=10).power == 40
    result = module.heat.batch(shared={'resistance':10},cases={'current':[1,2,3]})
    np.testing.assert_array_equal(result.values, [[10],[40],[90]])
    assert result.errors == (None,)*3
    with pytest.raises(ValueError, match='exactly once'):
        module.heat.batch(shared={'resistance':10}, cases={'resistance':[10], 'current':[2]})


def test_stale_source_rejected_and_reprepare_reloads(prepared):
    project, source, module = prepared
    assert module.heat(current=2,resistance=10).power == 40
    source.write_text(source.read_text().replace('current * current * resistance', '2 * current * current * resistance'))
    with pytest.raises(ValueError, match='Stale SysML source'):
        module.heat(current=2,resistance=10)
    project.prepare()
    assert module.heat(current=2,resistance=10).power == 80


def test_model_default_is_bound_before_native_execution(prepared):
    project, source, _ = prepared
    source.write_text(source.read_text().replace('in resistance : Real;', 'in resistance : Real default 10;'))
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('default_test', package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.heat(current=2).power == 40
    assert module.heat(current=2,resistance=5).power == 20
    np.testing.assert_array_equal(module.heat.batch(shared={},cases={'current':[1,2]}).values, [[10],[40]])
    assert 'default 10' in source.read_text()

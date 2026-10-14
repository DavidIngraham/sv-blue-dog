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


def test_source_hash_cache_detects_same_size_rewrite(tmp_path, monkeypatch):
    from sysml_python import execution
    source = tmp_path/'source.sysml'
    source.write_text('first')
    calls = []
    original = execution.digest
    def counted(path):
        calls.append(path)
        return original(path)
    monkeypatch.setattr(execution, 'digest', counted)
    first = execution.checked_digest(source)
    assert execution.checked_digest(source) == first
    assert len(calls) == 1
    previous = source.stat()
    source.write_text('other')
    os.utime(source, ns=(previous.st_atime_ns, previous.st_mtime_ns + 1_000_000_000))
    assert execution.checked_digest(source) != first
    assert len(calls) == 2


def test_independent_records_checks_and_batches(tmp_path):
    executable = os.environ.get('OPENSYSML_BINARY')
    if not executable:
        pytest.skip('Set OPENSYSML_BINARY to the pinned test compiler')
    (tmp_path/'plate.sysml').write_text("""package Plate {
        private import ScalarValues::*;
        attribute def Dimensions { attribute width : Real; attribute height : Real; }
        calc def Area {
            in size : Real [2] ordered nonunique;
            return area : Real = size#(1)*size#(2);
        }
        calc def Valid {
            in size : Real [2] ordered nonunique;
            attribute positiveWidth : Real = if size#(1)>0 ? 1.0 else 0.0;
            attribute positiveHeight : Real = if size#(2)>0 ? 1.0 else 0.0;
            return result : Real [2] ordered nonunique;
            (positiveWidth,positiveHeight)
        }
    }""")
    config = tmp_path/'pyproject.toml'
    config.write_text('''[tool.sysml_python]
models = ["*.sysml"]
generated_package = "generated"
[tool.sysml_python.exports.area]
definition = "Plate::Area"
checks = "Plate::Valid"
[tool.sysml_python.exports.area.aliases]
size = "dimensions"
[tool.sysml_python.exports.area.records]
dimensions = "Plate::Dimensions"
''')
    package = Project(config, executable=executable).prepare()
    spec = importlib.util.spec_from_file_location('plate_test', package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    first = module.Dimensions(width=2, height=3)
    assert module.area(dimensions=first).area == 6
    assert module.area(dimensions={'height':3, 'width':2}).area == 6
    packed = module.area.prepare_inputs(dimensions=first)
    np.testing.assert_array_equal(packed['dimensions'], [2,3])
    batch = module.area.batch(shared={}, cases={'dimensions':[first,module.Dimensions(width=4,height=5)]})
    np.testing.assert_array_equal(batch.values, [[6],[20]])
    with pytest.raises(ValueError, match='positiveWidth'):
        module.area(dimensions=module.Dimensions(width=-1,height=3))
    with pytest.raises(ValueError, match='case 1.*positiveHeight'):
        module.area.batch(shared={}, cases={'dimensions':[first,module.Dimensions(width=4,height=0)]})


def test_single_named_vector_return_and_array_copy(prepared):
    project, source, _ = prepared
    source.write_text(source.read_text().replace(
        'return power : Real = current * current * resistance;',
        'attribute power : Real = current * current * resistance; return result : Real [1] ordered nonunique; (power)'))
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('single_vector_test', package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.heat(current=2,resistance=10)
    vector = result.as_array()
    np.testing.assert_array_equal(vector,[40])
    vector[0] = 0
    assert result.power == 40


def test_execution_session_checks_before_use_and_after_nested_work(prepared):
    from sysml_python import execution_session
    _, source, module = prepared
    with pytest.raises(ValueError, match='Stale SysML source'):
        with execution_session():
            assert module.heat(current=2,resistance=10).power == 40
            with execution_session():
                assert module.heat(current=3,resistance=10).power == 90
            source.write_text(source.read_text().replace('current * current * resistance', '2 * current * current * resistance'))
            # Native code remains the pinned snapshot; the enclosing operation
            # must fail its exit check before the result can be accepted.
            assert module.heat(current=2,resistance=10).power == 40
    with pytest.raises(ValueError, match='Stale SysML source'):
        with execution_session():
            module.heat(current=2,resistance=10)


def test_execution_session_decorator_and_exception_cleanup(prepared):
    from sysml_python import execution_session
    _, source, module = prepared
    @execution_session()
    def calculate():
        return module.heat(current=2,resistance=10).power
    assert calculate() == calculate() == 40
    with pytest.raises(RuntimeError, match='abort'):
        with execution_session():
            module.heat(current=2,resistance=10)
            raise RuntimeError('abort')
    source.write_text(source.read_text()+'\n// changed\n')
    with pytest.raises(ValueError, match='Stale SysML source'):
        module.heat(current=2,resistance=10)


def test_prepared_project_is_relocatable(prepared):
    import shutil
    project, source, _ = prepared
    moved = project.root.parent / (project.root.name + '-moved')
    shutil.copytree(project.root, moved)
    source.write_text('changed original location')
    spec = importlib.util.spec_from_file_location('moved_test', moved/'generated/__init__.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.heat(current=2, resistance=10).power == 40
    assert set(module.heat.provenance()['sourceHashes']) == {'example.sysml'}


def test_configuration_and_source_discovery_are_checked(prepared):
    project, source, module = prepared
    project.path.write_text(project.path.read_text()+'\n# changed configuration\n')
    with pytest.raises(ValueError, match='Stale project configuration'):
        module.heat(current=2, resistance=10)
    project.prepare()
    assert module.heat(current=2, resistance=10).power == 40
    extra = source.with_name('added.sysml')
    extra.write_text('package Added {}')
    with pytest.raises(ValueError, match='source set changed'):
        module.heat(current=2, resistance=10)
    project.prepare()
    assert module.heat(current=2, resistance=10).power == 40
    assert set(module.heat.provenance()['sourceHashes']) == {'example.sysml', 'added.sysml'}


def test_execution_report_records_actual_build_and_failed_session(prepared):
    from sysml_python import execution_session
    _, source, module = prepared
    with execution_session() as report:
        module.heat(current=2, resistance=10)
        module.heat.batch(shared={'resistance':10}, cases={'current':[1,2,3]})
        with execution_session() as nested:
            assert nested is report
            module.heat(current=3, resistance=10)
        assert report.status == 'running'
    evidence = report.to_mapping()
    assert evidence['status'] == 'complete'
    scalar, batch = evidence['operations']
    assert (scalar['calls'],scalar['rows'],batch['rows']) == (2,2,3)
    assert len(scalar['provenance']['nativeBuild']['librarySha256']) == 64
    assert scalar['provenance']['sysmlCompiler']['sha256']
    assert scalar['provenance']['runtime']['sourceHashes']
    assert module.heat.provenance()['definition'] == 'Example::Heat'
    detached = module.heat.provenance()
    detached['sourceHashes'].clear()
    assert module.heat.provenance()['sourceHashes']
    assert module.heat(current=2,resistance=10).power == 40
    with pytest.raises(ValueError, match='Stale SysML source'):
        with execution_session() as failed:
            module.heat(current=2, resistance=10)
            source.write_text(source.read_text()+'\n// changed\n')
    assert failed.to_mapping()['status'] == 'failed'


def test_generated_batch_signature_is_statically_named(prepared):
    from typing import get_type_hints
    _, _, module = prepared
    hints = get_type_hints(type(module.heat).batch)
    assert set(hints['shared'].__annotations__) == {'current','resistance'}
    assert set(hints['cases'].__annotations__) == {'current','resistance'}
    result = module.heat(current=2,resistance=10)
    from dataclasses import replace
    with pytest.raises(ValueError, match='finite Real'):
        replace(result,power=float('nan'))
    with pytest.raises(TypeError, match='Real number'):
        replace(result,power=True)


@pytest.mark.parametrize('declaration,field,match', [
    ('attribute def Dimensions { attribute values : Real; }','values','conflicts'),
    ('attribute def Parent { attribute x : Real; } attribute def Dimensions :> Parent { attribute y : Real; }','y','inheritance'),
])
def test_unsupported_record_schemas_fail_explicitly(prepared, declaration, field, match):
    project, source, _ = prepared
    source.write_text('package Example { private import ScalarValues::*; '+declaration+
        ' calc def Heat { in size : Real [1] ordered nonunique; return area : Real = size#(1); } }')
    project.path.write_text(project.path.read_text()+'\n[tool.sysml_python.exports.heat.records]\nsize = "Example::Dimensions"\n')
    with pytest.raises(ValueError, match=match):
        project.prepare()


def test_source_aliases_preserve_resolved_discovery_semantics(prepared):
    project, source, module = prepared
    alias = source.with_name('alias.sysml')
    alias.symlink_to(source)
    assert module.heat(current=2,resistance=10).power == 40
    project.prepare()
    assert module.heat(current=2,resistance=10).power == 40

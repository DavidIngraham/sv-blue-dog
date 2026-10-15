import importlib.util
import sys
from sysml_python.records import as_array
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
    sys.modules[spec.name] = module
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
    sys.modules[spec.name] = module
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
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    first = module.Dimensions(width=2, height=3)
    from dataclasses import fields
    from sysml_python.records import Record
    assert not isinstance(first, Record)
    assert [f.metadata['sysml_name'] for f in fields(first)] == ['width', 'height']
    assert module.Dimensions(width=np.float32(2), height=np.int64(3)).to_mapping() == first.to_mapping()
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
    sys.modules[spec.name] = module
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
    sys.modules[spec.name] = module
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
    ('part def Nested {} part def Dimensions { attribute x : Real; part nested : Nested; }','x','nested'),
    ('attribute def Dimensions { attribute x : Real = 2; }','x','bound record'),
    ('attribute def Parent { attribute x : Real; } attribute def Dimensions :> Parent { attribute y : Real; }','y','inheritance'),
])
def test_unsupported_record_schemas_fail_explicitly(prepared, declaration, field, match):
    project, source, _ = prepared
    source.write_text('package Example { private import ScalarValues::*; '+declaration+
        ' calc def Heat { in size : Real [1] ordered nonunique; return area : Real = size#(1); } }')
    project.path.write_text(project.path.read_text()+'\n[tool.sysml_python.exports.heat.records]\nsize = "Example::Dimensions"\n')
    with pytest.raises(ValueError, match=match):
        project.prepare()


def test_snapshot_field_can_use_mapping_method_name(prepared):
    project, source, _ = prepared
    source.write_text('package Example { private import ScalarValues::*; '
        'attribute def Dimensions { attribute values : Real; attribute scale : Real; } '
        'calc def Heat { in size : Real [2] ordered nonunique; return area : Real = size#(1)*size#(2); } }')
    project.path.write_text(project.path.read_text()+'\n[tool.sysml_python.exports.heat.records]\nsize = "Example::Dimensions"\n')
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('mapping_name_test', package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.Dimensions(values=3, scale=2)
    assert record.values == 3
    assert record.to_mapping() == {'values': 3, 'scale': 2}
    assert module.heat(size=record).area == 6


def test_source_aliases_preserve_resolved_discovery_semantics(prepared):
    project, source, module = prepared
    alias = source.with_name('alias.sysml')
    alias.symlink_to(source)
    assert module.heat(current=2,resistance=10).power == 40
    project.prepare()
    assert module.heat(current=2,resistance=10).power == 40


@pytest.mark.parametrize('expression,expected', [('if current > 0 ? 1 else 0',[0,1]),('if current > 0 ? 1.5 else 0',[0,1.5])])
def test_real_scalar_with_compiler_numeric_union(prepared, expression, expected):
    project, source, _ = prepared
    source.write_text(source.read_text().replace('current * current * resistance',expression))
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('numeric_union_test',package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert module.heat(current=2,resistance=10).power == expected[1]
    result = module.heat.batch(shared={'resistance':10},cases={'current':[-1,2]})
    np.testing.assert_array_equal(result.values[:,0],expected)


def test_existing_user_package_is_not_overwritten(prepared):
    project, _, _ = prepared
    output = project.root/'generated/__init__.py'
    output.write_text('# application code\n')
    with pytest.raises(ValueError,match='non-generated'):
        project.prepare()
    assert output.read_text() == '# application code\n'


def test_constant_calculation_without_inputs(prepared):
    project, source, _ = prepared
    source.write_text('package Example { private import ScalarValues::*; calc def Heat { return power : Real = 42.0; } }')
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('constant_test',package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert module.heat().power == 42
    with pytest.raises(ValueError, match='exactly once'):
        module.heat.batch(shared={},cases={})


def test_record_defaults_preserve_model_order_and_named_overrides(prepared):
    project, source, _ = prepared
    source.write_text('package Example { private import ScalarValues::*;\n        part def Dimensions { attribute width : Real default 2; attribute height : Real; }\n        calc def Heat { in size : Real [2] ordered nonunique; return power : Real = size#(1)*size#(2); }\n    }')
    project.path.write_text(project.path.read_text()+'\n[tool.sysml_python.exports.heat.records]\nsize = "Example::Dimensions"\n')
    package = project.prepare()
    spec = importlib.util.spec_from_file_location('record_defaults_test',package/'__init__.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    record = module.Dimensions(height=3, width=2)
    with pytest.raises(TypeError):
        module.Dimensions(height=3)
    np.testing.assert_array_equal(as_array(record),[2,3])
    assert module.heat(size=record).power == 6
    assert module.heat(size={'height':3}).power == 6
    assert module.heat(size=module.Dimensions(height=3,width=4)).power == 12
    np.testing.assert_array_equal(module.heat.batch(shared={},cases={'size':[{'height':3},{'height':4,'width':5}]}).values,[[6],[20]])

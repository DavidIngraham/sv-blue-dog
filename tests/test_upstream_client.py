"""Native typed execution must preserve values, failure verdicts and source edits."""
from fractions import Fraction
import os

import pytest

from tools.boat_analysis.model.runtime import analysis_values, load_model, numerical_value, record_analyses


def test_typed_analysis_preserves_strings_and_reloads_edits(tmp_path):
    source = tmp_path / 'typed.sysml'
    text = '''package Typed {
        analysis sample {
            out text : ScalarValues::String = "1/3 is a label";
            out value : ScalarValues::Real = 2.5;
        }
    }'''
    source.write_text(text)
    assert analysis_values('Typed::sample', (source,)) == {'text': '1/3 is a label', 'value': 2.5}
    before = source.stat()
    assert load_model((source,)) is load_model((source,))
    source.write_text(text.replace('2.5', '4.5'))
    os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert analysis_values('Typed::sample', (source,))['value'] == 4.5


def test_failed_analysis_is_not_accepted_as_input(tmp_path):
    source = tmp_path / 'failed.sysml'
    source.write_text('package Failed { analysis sample { out value : ScalarValues::Real = 2; assert constraint { value < 0 } } }')
    with pytest.raises(ValueError, match='did not satisfy'):
        analysis_values('Failed::sample', (source,))


def test_numerical_boundary_converts_rationals_without_rewriting_text():
    assert numerical_value({'ratio': Fraction(1, 3), 'text': '1/3'}) == {'ratio': 1/3, 'text': '1/3'}
    with pytest.raises(TypeError):
        numerical_value(object())


def test_mission_classifier_accepts_numpy_booleans_and_rejects_truthy_strings():
    import numpy as np
    from tools.boat_analysis.mission.engine import evaluate_outcome
    facts = [False] * 8
    assert evaluate_outcome(*map(np.bool_, facts)) == evaluate_outcome(*facts)
    with pytest.raises(TypeError, match='Boolean'):
        evaluate_outcome('false', *facts[1:])


def test_native_analysis_records_reload_with_case_and_output(tmp_path):
    source = tmp_path / 'record.sysml'
    dependency = tmp_path / 'values.sysml'
    dependency.write_text('package Values { attribute answer : ScalarValues::Real = 42; }')
    text = 'package Recorded { analysis sample { out result : ScalarValues::Real = Values::answer; } }'
    source.write_text(text)
    output = record_analyses(['Recorded::sample'], tmp_path/'evidence.sysml', (source, dependency))
    assert source.read_text() == text
    model = load_model((output,))
    record = model.instantiate('BlueDogRecordedEvidence::sample_run1')
    assert record.caseName == 'Recorded::sample'
    assert record.result == 42
    import json, hashlib
    from tools.boat_analysis.model.install import REVISION, binary_path
    provenance = json.loads(output.with_suffix('.sysml.provenance.json').read_text())
    assert provenance['runtimeRevision'] == REVISION
    assert provenance['recordedModelSha256'] == hashlib.sha256(output.read_bytes()).hexdigest()
    assert provenance['sourceHashes'][str(source)] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert provenance['executableSha256'] == hashlib.sha256(binary_path().read_bytes()).hexdigest()
    assert provenance['modelHash'] == load_model((source, dependency)).hash
    with pytest.raises(ValueError, match='overwrite'):
        record_analyses(['Recorded::sample'], source, (source,))


def test_missing_record_does_not_replace_existing_evidence(tmp_path):
    source = tmp_path / 'input.sysml'
    source.write_text('package Sample { analysis valid { out x : ScalarValues::Real = 1; } }')
    output = tmp_path / 'evidence.sysml'
    output.write_text('previous evidence')
    with pytest.raises(RuntimeError, match='did not record'):
        record_analyses(['Sample::missing'], output, (source,))
    assert output.read_text() == 'previous evidence'


def test_native_records_distinguish_runs_from_nested_verdicts_and_unrelated_parts(tmp_path):
    source = tmp_path/'subject.sysml'
    source.write_text('''package SubjectCases {
        part vessel { attribute capacity : ScalarValues::Real = 42; }
        analysis passing {
            subject candidate = vessel;
            out result : ScalarValues::Real = candidate.capacity;
            assert constraint positive { result > 0 }
        }
        analysis failing {
            subject candidate = vessel;
            out result : ScalarValues::Real = candidate.capacity;
            assert constraint insufficient { result < 0 }
        }
    }
    package BlueDogRecordedEvidence {
        part unrelated { attribute caseName : ScalarValues::String = "NotAnAnalysis::case"; }
    }''')
    output = record_analyses(['SubjectCases::passing', 'SubjectCases::failing'],
                            tmp_path/'evidence.sysml', (source,))
    model = load_model((output,))
    passing = model.instantiate('BlueDogRecordedEvidence::passing_run1')
    failing = model.instantiate('BlueDogRecordedEvidence::failing_run1')
    assert passing.caseName == 'SubjectCases::passing'
    assert failing.caseName == 'SubjectCases::failing'
    assert passing.subjectName == failing.subjectName == 'SubjectCases::vessel'
    assert model.instantiate('BlueDogRecordedEvidence::passing_run1::verdict1').status == 'satisfied'
    assert model.instantiate('BlueDogRecordedEvidence::failing_run1::verdict1').status == 'not satisfied'
    assert model.instantiate('BlueDogRecordedEvidence::unrelated').caseName == 'NotAnAnalysis::case'

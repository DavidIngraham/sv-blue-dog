"""Native typed execution must preserve values, failure verdicts and source edits."""
from fractions import Fraction

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
    source.write_text(text.replace('2.5', '4.5'))
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

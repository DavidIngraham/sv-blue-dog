import pytest
from tools.publishing.risk_cube import coordinate, render, render_all, read_rows, LIKELIHOOD, CONSEQUENCE


def test_ordinal_classes_do_not_accept_numeric_probabilities():
    assert coordinate('', LIKELIHOOD) is None
    assert coordinate('Remote', LIKELIHOOD) == 0
    assert coordinate('Demonstrated', LIKELIHOOD) == 4
    assert coordinate('Critical', CONSEQUENCE) == 4
    for value in ('0', '0.8', 'NaN', 'Very likely'):
        with pytest.raises(ValueError): coordinate(value, LIKELIHOOD)


def test_native_risks_have_explicit_qualitative_assessments():
    rows = read_rows()
    assert len(rows) == 6
    assert {r["kind"] for r in rows} == {"technical"}
    assert all(r['status'].split('::')[-1] == 'open' for r in rows)
    assert all(r['statement'] and r['basis'] and r['reductionAction'] and r['evidence'] for r in rows)
    assert all(r['likelihood'] in LIKELIHOOD and r['consequence'] in CONSEQUENCE for r in rows)
    assert next(r for r in rows if r['identifier']=='R-006')['likelihood']=='Demonstrated'


def test_render_places_assessed_and_retains_unknown(tmp_path):
    rows = [dict(kind="technical",identifier='TEST-A',area='Test',likelihood='Likely',consequence='Critical'),
            dict(kind="technical",identifier='TEST-B',area='Unknown',likelihood='',consequence='Major')]
    text = render(tmp_path, rows).read_text(encoding='utf-8')
    assert 'TEST-A' in text and 'TEST-B' in text
    assert '1 assessed' in text and 'Unassessed: TEST-B' in text
    assert 'Not probabilities of accidents.' in text
    assert '0–.2' not in text


def test_risk_kinds_have_separate_cubes(tmp_path):
    rows = [dict(kind='technical', identifier='TECH', area='Design', likelihood='Likely', consequence='Critical'),
            dict(kind='schedule', identifier='SCHED', area='Lead time', likelihood='Possible', consequence='Minor')]
    paths = render_all(tmp_path, rows)
    assert set(paths) == {'technical', 'schedule'}
    assert 'TECH' in paths['technical'].read_text() and 'SCHED' not in paths['technical'].read_text()
    assert 'SCHED' in paths['schedule'].read_text() and 'TECH' not in paths['schedule'].read_text()
    assert 'SCHED' not in (tmp_path / 'cube.svg').read_text()

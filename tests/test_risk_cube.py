import pytest
from tools.publishing.risk_cube import coordinate, render, read_rows, LIKELIHOOD, CONSEQUENCE


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
    assert all(r['likelihood'] in LIKELIHOOD and r['consequence'] in CONSEQUENCE for r in rows)
    assert next(r for r in rows if r['identifier']=='R-006')['likelihood']=='Demonstrated'


def test_render_places_assessed_and_retains_unknown(tmp_path):
    rows = [dict(identifier='TEST-A',area='Test',likelihood='Likely',consequence='Critical'),
            dict(identifier='TEST-B',area='Unknown',likelihood='',consequence='Major')]
    text = render(tmp_path, rows).read_text(encoding='utf-8')
    assert 'TEST-A' in text and 'TEST-B' in text
    assert '1 assessed' in text and 'Unassessed: TEST-B' in text
    assert 'Not probabilities of accidents.' in text
    assert '0–.2' not in text

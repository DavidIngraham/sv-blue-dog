import pytest
from tools.publishing.risk_cube import coordinate, cell, render, read_rows


def test_missing_is_not_zero_and_bins_include_endpoints():
    assert coordinate('') is None
    assert coordinate('0') == 0
    assert coordinate('1/2') == .5
    assert [cell(v) for v in (0,.2,.2001,1)] == [0,0,1,4]
    for value in ('-0.1','1.1','NaN'):
        with pytest.raises(ValueError): coordinate(value)


def test_native_risks_remain_unassessed():
    rows = read_rows()
    assert len(rows) == 6
    assert all(r['probability'] is None and r['impact'] is None for r in rows)


def test_render_places_assessed_and_retains_unknown(tmp_path):
    rows = [dict(identifier='TEST-A',area='Test',probability=1,impact=0),
            dict(identifier='TEST-B',area='Unknown',probability=None,impact=.8)]
    text = render(tmp_path, rows).read_text(encoding='utf-8')
    assert 'TEST-A' in text and 'TEST-B' in text
    assert '1 assessed' in text and 'Unassessed' in text

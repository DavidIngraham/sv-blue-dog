"""Provenance and publication checks for preliminary wing evidence."""
import hashlib,json,math
from pathlib import Path
from scripts.publish_wing_analysis import publication
ROOT=Path(__file__).resolve().parents[1]


def test_wing_geometry_preserves_missing_data_and_source_identity():
    r=json.loads((ROOT/'docs/analysis/wing-geometry.json').read_text())
    assert hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['sha256']
    assert r['units']=='mm'
    for p in r['profiles']:
        assert len(p['x_mm'])==len(p['upper_mm'])==len(p['lower_mm'])
        assert all(b>a for a,b in zip(p['x_mm'],p['x_mm'][1:]))
        missing=sum(u is None or l is None for u,l in zip(p['upper_mm'],p['lower_mm']))
        assert p['incomplete_samples']==missing
        assert (p['enclosed_area_mm2'] is None)==bool(missing)
        assert all(u>=l for u,l in zip(p['upper_mm'],p['lower_mm']) if u is not None and l is not None)


def test_reference_runs_are_finite_consistent_and_not_qualified():
    source=hashlib.sha256((ROOT/'analysis/wing/reference_vsp.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for mesh in [16,32,64]:
        r=json.loads((ROOT/f'docs/analysis/wing-vsp-reference-{mesh}.json').read_text())
        assert r['driverSha256']==source
        assert r['validated'] is False
        assert r['mesh']==mesh
        assert math.isclose(r['span_m']*r['chord_m'],r['area_m2'])
        assert math.isclose(r['span_m']/r['chord_m'],r['aspectRatio'])
        for key in ['CLtot','CDi','CMytot']:
            assert len(r['results'][key])==len(r['results']['Alpha'])
            assert all(math.isfinite(x) for x in r['results'][key])


def test_wing_report_is_generated_from_current_results():
    assert (ROOT/'docs/wing-analysis-results.md').read_text(encoding='utf-8')==publication()

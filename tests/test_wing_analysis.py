"""Provenance and publication checks for preliminary wing evidence."""
import hashlib,json,math
from pathlib import Path
from tools.boat_analysis.evidence.records import baseline_record
import subprocess
ROOT=Path(__file__).resolve().parents[1]


def test_wing_geometry_preserves_missing_data_and_source_identity():
    r=baseline_record('wing-geometry.json')
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
    manifest=json.loads((ROOT/'evidence/runs/2026-10-10-coupled/manifest.json').read_text())
    driver=subprocess.check_output(['git','show',manifest['sourceRevision']+':analysis/wing/reference_vsp.py'],cwd=ROOT)
    source=hashlib.sha256(driver.replace(b'\r\n',b'\n')).hexdigest()
    for mesh in [16,32,64]:
        r=baseline_record(f'wing-vsp-reference-{mesh}.json')
        assert r['driverSha256']==source
        assert r['validated'] is False
        assert r['mesh']==mesh
        assert math.isclose(r['span_m']*r['chord_m'],r['area_m2'])
        assert math.isclose(r['span_m']/r['chord_m'],r['aspectRatio'])
        for key in ['CLtot','CDi','CMytot']:
            assert len(r['results'][key])==len(r['results']['Alpha'])
            assert all(math.isfinite(x) for x in r['results'][key])

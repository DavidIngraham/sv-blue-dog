"""Published experiment figures must all be reproducible from archived evidence."""
import json
import re
from tools.boat_analysis.evidence.aerodynamics import render
from tools.boat_analysis.model.runtime import ROOT


def test_gallery_assets_and_sample_provenance(tmp_path):
    out=render(tmp_path)
    page=(ROOT/'docs/sail-trade.md').read_text(encoding='utf-8')
    assets=re.findall(r'https://davidingraham.github.io/sv-blue-dog/assets/vsp/([^\s)]+)',page)
    assert len(assets)==14
    assert all((out/name).stat().st_size>1000 for name in assets)
    provenance=json.loads((out/'provenance.json').read_text())
    assert provenance['gridCases']==25
    assert provenance['gridSamples']==200
    assert provenance['validated'] is False

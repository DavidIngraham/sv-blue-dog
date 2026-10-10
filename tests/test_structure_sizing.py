"""Independent formula, regression, trace and native route checks."""
import json
import math
from pathlib import Path
import numpy as np
import pytest
from scripts.study_open_sizing import ROOT, STRUCTURE, ROUTE, MODEL, read_report
from scripts.prepare_design_search import native_value


def model_source():
    return '\n'.join(p.read_text(encoding='utf-8') for p in (STRUCTURE, ROUTE, MODEL))


def values(report):
    return {v['name']:native_value(v['value']) for v in report['checks'][0]['values'] if v['value'] not in ('satisfied','violated')}


def test_mass_and_finite_thickness_inertia_against_hand_calculation(run_model):
    source=model_source()+'''\npackage HandCheck {
        analysis def Evaluate {
            out attribute shell : ScalarValues::Real = BlueDogStructure::HullArealMass(0.6, BlueDogOpenSizing::sizingSettings.parameterValues, 0.06);
            out attribute laminate : ScalarValues::Real = BlueDogStructure::LaminateThickness(0.6, BlueDogOpenSizing::sizingSettings.parameterValues);
            out attribute inertia : ScalarValues::Real = BlueDogStructure::ShellInertia(0.1, 0.012, 0.002);
        }
    }'''
    code,r=run_model(source,'-analysis','HandCheck::Evaluate');assert code==0
    v=values(r)
    assert v['shell']==pytest.approx(1270*(.0008+2*.0008*.01/.06)+.6*2+.1+2*.03/.23*.2*2)
    assert v['laminate']==pytest.approx(.6/2550+.6/1180)
    assert v['inertia']==pytest.approx(2*.1*(.002**3/12+.002*(.012/2-.002/2)**2))


def test_signed_time_weighting_preserves_negative_progress(run_model):
    source=model_source()+'''\npackage RouteCheck {
        analysis def Evaluate {
            out attribute average : ScalarValues::Real = BlueDogSizingRoute::MeanProgress((1.0,3.0),(-1.5,-1.5),(0.5,0.5),1.0);
        }
    }'''
    code,r=run_model(source,'-analysis','RouteCheck::Evaluate');assert code==0
    assert values(r)['average']==pytest.approx(.5) # -0.5 is retained, not discarded.


def test_long_keel_and_low_freeboard_are_rejected_by_native_physics(run_model):
    # Earlier free-sizing solution, with candidate composite layup appended.
    d=[4.664,.1094,5.258,8.44,.0966,11.86,.09099,1.137,1.202,-.5,230.7,.2695,2.744,.0025,.2869,.6,.4,.8,.8,.05]
    source=model_source()+'''\npackage OldCandidate {
        part boat : BlueDogOpenSizing::Candidate {
            attribute :>> design = ('''+','.join(map(str,d))+''');
            attribute :>> scenario = (5,1,1,2,45,8,3,-2,8);
        }
        analysis assessment : BlueDogOpenSizing::Audit { subject :>> trial = boat; }
    }'''
    code,r=run_model(source,'-analysis','OldCandidate::assessment');assert code==0
    c=read_report()['contract'];v=dict(zip(c['outputNames'],values(r)['rows']))
    assert v['keel_bending']<0 and v['keel_deflection']<0
    assert v['deck_freeboard']<0 and v['launch_clearance']<0
    assert v['eq_heel']==pytest.approx((v['rightingMoment']-v['heelingMoment'])/20)


def test_selected_results_mass_moments_and_integer_layups():
    report=read_report()
    for study in report['studies'].values():
        d=study['best']['design']
        for key,count in zip(report['contract']['designNames'][15:19],study['plyCounts']):
            assert d[key]==pytest.approx(.2*count)
        for row in study['best']['results']:
            assert row['bodyMass']+row['keelAssembly']==pytest.approx(row['totalMass'])
            assert row['keelAssembly']==pytest.approx(d['ballast_kg']+row['keelStructuralMass'])
            assert row['eq_heel']==pytest.approx((row['rightingMoment']-row['heelingMoment'])/20,abs=1e-9)
            assert row['deckEdgeFreeboard']>=.05-1e-5
            assert row['reserveDisplacementFraction']>=1-1e-5
            assert row['immersedDepth']<=1.2+1e-5


def test_structure_trace_is_native_and_evidence_remains_open():
    source=STRUCTURE.read_text(encoding='utf-8')
    assert 'source ::> structuralIntegrity' in source
    assert 'to BlueDogRequirements::desktopManufacture' in source
    assert 'to BlueDogRequirements::soloLaunch' in source
    report=json.loads((ROOT/'docs/analysis/sizing-route-audit.json').read_text(encoding='utf-8'))
    assert values(report)['missionSupported'] is False
    assert values(report)['evidenceReady'] is False


def test_generated_trace_contains_derivation_edges_and_design_bases():
    text=(ROOT/'docs/structure-requirements.md').read_text(encoding='utf-8')
    assert text.count('|"derive"|')>=6
    assert 'Design basis' in text and 'desktopManufacture' in text and 'soloLaunch' in text

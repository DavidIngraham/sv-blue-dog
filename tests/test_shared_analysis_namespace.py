"""Shared calculation ownership and reusable native execution are real model structure."""
import math
import pytest
from tools.boat_analysis.model.runtime import ROOT,connection,load_model,model_files
from tests.native_edits import edit_sources


def test_only_calculation_libraries_share_analysis_and_mixed_roots_stay_separate():
    model=load_model()
    roots={r.id for r in model.query(select=['owner'],where={
        '@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['Package']}) if not r.get('owner')}
    assert roots=={'Analysis','BlueDog','GorgeChallenge','MarineDesign','MarineEnergy','InlandExtended',
                   'InlandNavigationExperiment','EngineeringDecisions'}
    assert len(model_files())==8
    assert model.get('MarineSailing') is None
    assert model.get('MarineMass') is None
    for identity in ('MarineDesign::Design','MarineEnergy::Battery',
                     'InlandExtended::Truth','InlandNavigationExperiment::VesselKind',
                     'EngineeringDecisions::DecisionRecord','BlueDog::Analyses::SailTrade'):
        assert model.get(identity).id==identity


def test_shared_analysis_document_is_standalone_and_executes_native_calculations():
    path=ROOT/'models/libraries/analysis.sysml'
    model=connection().parse_sources(((str(path),path.read_text()),),strict=True)
    assert model.calc('Analysis::Reliability::ConstantHazardSurvival',arguments=[0.1,2.0]).value==pytest.approx(math.exp(-0.2),rel=1e-14,abs=1e-15)
    rows=model.query(scope=['Analysis'],select=[],where={
        '@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['CalculationDefinition']})
    assert len(rows)==44
    assert all(row.id.startswith('Analysis::') for row in rows)


def test_new_domain_calculation_is_discovered_and_runs_without_python_dispatch_edits():
    primary=ROOT/'models/libraries/analysis.sysml'
    # Native edits target the primary document; calculation ownership is explicit.
    paths=(primary,*(p for p in model_files() if p!=primary))
    sources=tuple((str(p),p.read_text()) for p in paths)
    owner='Analysis::Mechanics::ScaleFixture'
    def extend(editor):
        editor.add_member('Analysis::Mechanics','calc def','ScaleFixture')
        editor.add_member(owner,'attribute','inputN',type='ScalarValues::Real',direction='in')
        editor.add_member(owner,'attribute','scale',type='ScalarValues::Real',direction='in')
        editor.add_member(owner,'return','forceN',type='ScalarValues::Real',value='inputN * scale')
    model=connection().parse_sources(edit_sources(sources,extend),strict=True)
    rows=model.query(scope=['Analysis::Mechanics'],select=[],where={
        '@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['CalculationDefinition']})
    assert owner in {row.id for row in rows}
    assert model.calc(owner,arguments=[5.0,2.0]).value==10.0

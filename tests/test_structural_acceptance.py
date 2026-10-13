"""Production acceptance constraints distinguish evidence from sizing assumptions."""
import pytest


def evaluate(run_model, definition, **inputs):
    bindings=' '.join(f'attribute :>> {name} = {str(value).lower()};' for name,value in inputs.items())
    code,report=run_model('package Check { requirement sample : BlueDogStructure::'+definition+' { '+bindings+' } }', '-requirement','Check::sample')
    return code,report['status']


@pytest.mark.parametrize('definition,credit,bound,value', [
    ('WetCouponStiffness','creditedModulusPa','qualifiedModulusPa',5e9),
    ('WetCouponStrength','creditedAllowablePa','qualifiedAllowablePa',25e6),
])
def test_lower_material_properties_are_allowed_but_overcredit_is_not(run_model,definition,credit,bound,value):
    data={credit:value,bound:value,'evidenceAccepted':True}
    assert evaluate(run_model,definition,**data)==(0,'holds')
    assert evaluate(run_model,definition,**(data|{credit:value*1.01}))==(1,'fails')
    assert evaluate(run_model,definition,**(data|{'evidenceAccepted':False}))==(1,'fails')
    assert evaluate(run_model,definition)[1]!='holds'


@pytest.mark.parametrize('definition',['AppendageDeflection','HullDeflection','PanelDeflection'])
def test_functional_limit_replaces_assumed_screen(run_model,definition):
    data=dict(fraction=.025,validatedMaximumFraction=.03,limitEvidenceAccepted=True)
    assert evaluate(run_model,definition,**data)==(0,'holds')
    assert evaluate(run_model,definition,**(data|{'fraction':.031}))==(1,'fails')
    assert evaluate(run_model,definition,**(data|{'limitEvidenceAccepted':False}))==(1,'fails')


@pytest.mark.parametrize('definition,inputs,change', [
    ('PrintTileEnvelope',dict(jobXM=.24,jobYM=.25,jobZM=.2,slicerEvidenceAccepted=True),dict(jobYM=.2501)),
    ('PrintTileEnvelope',dict(jobXM=.24,jobYM=.25,jobZM=.2,slicerEvidenceAccepted=True),dict(jobZM=-.1)),
    ('LaunchClearance',dict(availableDepthM=.9,immersedDepthM=.4,requiredClearanceM=.2,siteEvidenceAccepted=True),dict(availableDepthM=.5)),
    ('ReserveBuoyancy',dict(availableBuoyancyN=120,loadedWeightN=100,caseCoverageAccepted=True),dict(availableBuoyancyN=99)),
    ('LoadedFreeboard',dict(minimumOpeningClearanceM=.01,caseCoverageAccepted=True),dict(minimumOpeningClearanceM=0)),
    ('BendingStrength',dict(stressPa=20e6,qualifiedAllowablePa=25e6,evidenceAccepted=True),dict(stressPa=26e6)),
    ('PanelStrength',dict(stressPa=20e6,qualifiedAllowablePa=25e6,evidenceAccepted=True),dict(stressPa=-26e6)),
])
def test_design_specific_acceptance(run_model,definition,inputs,change):
    assert evaluate(run_model,definition,**inputs)==(0,'holds')
    assert evaluate(run_model,definition,**(inputs|change))==(1,'fails')
    assert evaluate(run_model,definition)[1]!='holds'


def test_aged_capacity_is_compared_with_design_credit(run_model):
    for capacity,accepted,expected in [(60,True,'holds'),(49,True,'fails'),(60,False,'fails')]:
        source=('package Aging { requirement sample : BlueDogRequirements::PrintedMaterialAging { '
                'attribute :>> creditedLoadCapacityN = 50; '
                f'attribute :>> qualifiedAgedCapacityN = {capacity}; '
                f'attribute :>> exposureEvidenceAccepted = {str(accepted).lower()};'+' } }')
        _,report=run_model(source,'-requirement','Aging::sample')
        assert report['status']==expected

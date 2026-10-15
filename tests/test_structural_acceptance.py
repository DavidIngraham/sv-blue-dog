"""Production acceptance constraints distinguish evidence from sizing assumptions."""
import pytest


@pytest.mark.parametrize('definition,credit,bound,value', [
    ('WetCouponStiffness','creditedModulusPa','qualifiedModulusPa',5e9),
    ('WetCouponStrength','creditedAllowablePa','qualifiedAllowablePa',25e6),
])
def test_lower_material_properties_are_allowed_but_overcredit_is_not(acceptance,definition,credit,bound,value):
    data={credit:value,bound:value,'evidenceAccepted':True}
    assert acceptance(definition,**data)==(0,'holds')
    assert acceptance(definition,**(data|{credit:value*1.01}))==(1,'fails')
    assert acceptance(definition,**(data|{'evidenceAccepted':False}))==(1,'fails')
    assert acceptance(definition)[1]!='holds'


@pytest.mark.parametrize('definition',['AppendageDeflection','HullDeflection','PanelDeflection'])
def test_functional_limit_replaces_assumed_screen(acceptance,definition):
    data=dict(fraction=.025,validatedMaximumFraction=.03,limitEvidenceAccepted=True)
    assert acceptance(definition,**data)==(0,'holds')
    assert acceptance(definition,**(data|{'fraction':.031}))==(1,'fails')
    assert acceptance(definition,**(data|{'limitEvidenceAccepted':False}))==(1,'fails')


@pytest.mark.parametrize('definition,inputs,change', [
    ('PrintTileEnvelope',dict(jobXM=.24,jobYM=.25,jobZM=.2,slicerEvidenceAccepted=True),dict(jobYM=.2501)),
    ('PrintTileEnvelope',dict(jobXM=.24,jobYM=.25,jobZM=.2,slicerEvidenceAccepted=True),dict(jobZM=-.1)),
    ('LaunchClearance',dict(availableDepthM=.9,immersedDepthM=.4,requiredClearanceM=.2,siteEvidenceAccepted=True),dict(availableDepthM=.5)),
    ('ReserveBuoyancy',dict(availableBuoyancyN=120,loadedWeightN=100,caseCoverageAccepted=True),dict(availableBuoyancyN=99)),
    ('LoadedFreeboard',dict(minimumOpeningClearanceM=.01,caseCoverageAccepted=True),dict(minimumOpeningClearanceM=0)),
    ('BendingStrength',dict(stressPa=20e6,qualifiedAllowablePa=25e6,evidenceAccepted=True),dict(stressPa=26e6)),
    ('PanelStrength',dict(stressPa=20e6,qualifiedAllowablePa=25e6,evidenceAccepted=True),dict(stressPa=-26e6)),
])
def test_design_specific_acceptance(acceptance,definition,inputs,change):
    assert acceptance(definition,**inputs)==(0,'holds')
    assert acceptance(definition,**(inputs|change))==(1,'fails')
    assert acceptance(definition)[1]!='holds'


def test_aged_capacity_is_compared_with_design_credit(acceptance):
    for capacity,accepted,expected in [(60,True,'holds'),(49,True,'fails'),(60,False,'fails')]:
        _, status = acceptance('PrintedMaterialAging', creditedLoadCapacityN=50,
                               qualifiedAgedCapacityN=capacity, exposureEvidenceAccepted=accepted)
        assert status == expected


def test_shared_inputs_do_not_leak(acceptance):
    good = dict(creditedAllowablePa=20e6, qualifiedAllowablePa=25e6, evidenceAccepted=True)
    assert acceptance('WetCouponStrength', **good) == (0, 'holds')
    assert acceptance('WetCouponStrength') == (2, 'unevaluated')
    assert acceptance('WetCouponStrength', **(good | {'evidenceAccepted': False})) == (1, 'fails')
    assert acceptance('WetCouponStrength', **good) == (0, 'holds')


@pytest.mark.parametrize('accepted,expected', [(True, 'holds'), (False, 'fails')])
def test_shared_evaluation_matches_cli(acceptance, run_model, accepted, expected):
    inputs = dict(creditedAllowablePa=20e6, qualifiedAllowablePa=25e6, evidenceAccepted=accepted)
    bindings = ' '.join(f'attribute :>> {key} = {str(value).lower()};' for key,value in inputs.items())
    code, report = run_model('package Parity { requirement sample : BlueDogStructure::WetCouponStrength { '
                             + bindings + ' } }', '-requirement', 'Parity::sample')
    assert report['status'] == expected
    assert acceptance('WetCouponStrength', **inputs) == (code, report['status'])

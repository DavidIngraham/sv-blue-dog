"""Native configuration applicability, accounting boundaries and meaningful negative controls."""
import pytest
from tools.boat_analysis.model.runtime import ROOT,connection,load_model,model_files
from tools.boat_analysis.model.configuration_audit import native_configuration_audit
from tests.native_edits import set_values

@pytest.fixture(scope='module')
def sources():return tuple((str(p),p.read_text()) for p in model_files())

@pytest.fixture(scope='module')
def report(sources):return native_configuration_audit(sources)


def test_all_top_level_design_parameter_parts_have_context_and_no_acceptance(report):
    assert not report['errors'] and not report['diagnostics']
    assert report['summary']==dict(configurationContexts=12,accountingScopes=7,topLevelDesignParameterParts=9)
    assert report['review']==dict(scopeCount=7,allScopesSameConfiguration=True,installationReconciled=False,
        resourceEvidenceReady=False,ready=False)
    assert len(report['openRequiredQuantities'])==3
    assert len(report['missingInstallationRecords'])==5
    assert len(report['unboundedPowerPeaks'])==2 and all(r['missingPeak'] for r in report['unboundedPowerPeaks'])


def test_historical_bingen_and_440wh_replay_are_different_subjects(report):
    rows={r['element']['id'].rsplit('::',1)[-1]:r for r in report['tables']['Contexts']['rows']}
    assert rows['retainedSizing']['cells'][2][0]['id']=='BlueDog::Evidence::SRRCurrent::candidate'
    assert rows['bingenProjection']['cells'][2][0]['id']=='BlueDog::Evidence::CurrentSizing::candidate'
    assert load_model().eval('BlueDog::Evidence::CurrentSizing::candidate.battery_Wh')!=440
    assert load_model().eval('BlueDog::Evidence::SRRCurrent::candidate.batteryWh')==440


@pytest.mark.parametrize('target,value,error',[
    ('retainedSizing::representedSubject','BlueDog::Evidence::CurrentSizing::candidate','C02 Wrong represented subject'),
    ('ic01Installation::design','BlueDog::Evidence::CurrentSizing::candidate','C04 Wrong planned installation reference'),
    ('ResourceScope::configuration','BlueDog::Evidence::CurrentSizing::candidate','C07 Wrong accounting configuration'),
    ('ic01::fixedEquipment::massAllocation',
     '(BlueDog::Configurations::IC01::integration.fixedEquipmentKg + BlueDog::Configurations::IC01::integration.recoveryBatteryWh/BlueDog::Configurations::IC01::integration.batteryWhKg) * 1 [kg]',
     'C10 Accounting binding differs'),
    ('ic01::sailingElectronics::averagePowerAllocation',
     '(BlueDog::Configurations::IC01::integration.electronicsW + BlueDog::Configurations::IC01::integration.additionalBusW) * 1 [W]',
     'C10 Accounting binding differs'),
    ('ic01::recoveryEssentials::averagePowerAllocation','-1 [W]','C07 Invalid allocated quantity'),
])
def test_substitution_double_counting_and_invalid_demand_are_detected(sources,target,value,error):
    mutant=set_values(sources, {'BlueDog::Configurations::Management::'+target:value})
    assert any(error in e for e in native_configuration_audit(mutant)['errors'])


def test_new_unclassified_top_level_design_is_detected(sources):
    extra='package ConfigurationTest { part candidate : MarineDesign::Design; }'
    assert 'C02 Unclassified top-level design/parameter part: ConfigurationTest::candidate' in native_configuration_audit((*sources,(str(ROOT/'reviews/unclassified-test.sysml'),extra)))['errors']


def test_new_unclassified_design_in_deep_namespace_is_detected(sources):
    extra='package ConfigurationTest { package Nested { package Further { part candidate : MarineDesign::Design; } } }'
    error='C02 Unclassified top-level design/parameter part: ConfigurationTest::Nested::Further::candidate'
    assert error in native_configuration_audit((*sources, (str(ROOT/'reviews/deep-configuration.sysml'),extra)))['errors']


@pytest.mark.parametrize('missing',['articleId','hardwareRevision','softwareDataRevision','procedureRevision','reconciliationRecord'])
def test_missing_installation_identity_cannot_be_reconciled(sources,missing):
    values={k:'"synthetic-test-only"' for k in ('articleId','hardwareRevision','softwareDataRevision','procedureRevision','reconciliationRecord')}
    values.pop(missing)
    body=' '.join('attribute :>> '+k+' = '+v+';' for k,v in values.items())
    extra='''package InstallationTest { part example : BlueDog::Configurations::Management::PlannedInstallation {
        ref part :>> design = BlueDog::Configurations::IC01::design; ref part :>> assembly = BlueDog::Architecture::Physical::ic01;
        attribute :>> reconciled = true;'''+body+'} }'
    m=connection().parse_sources((*sources,(str(ROOT/'reviews/installation.sysml'),extra)),strict=True)
    assert m.eval('InstallationTest::example.configurationReconciled') is False


def test_empty_peak_is_not_zero_or_ready_even_with_synthetic_review_flags(sources):
    # Change only resource-accounting defaults; unrelated evidence stays untouched.
    prefix='BlueDog::Configurations::Management::ResourceScope::'
    mutant=set_values(sources, {
        prefix+'coverageReviewed':'true',
        prefix+'measurementsAccepted':'true',
        prefix+'accountingReconciled':'true',
        prefix+'evidenceRecord':'"synthetic-test-only"',
    })
    m=connection().parse_sources(mutant,strict=True)
    assert m.eval('BlueDog::Configurations::Management::ic01.sailingElectronics.ready') is False
    assert m.eval('BlueDog::Configurations::Management::ic01.recoveryEssentials.ready') is False
    assert m.eval('BlueDog::Configurations::Management::ic01.wholeVesselMass.ready') is False
    assert m.eval('BlueDog::Configurations::Management::ic01.fixedEquipment.ready') is True


@pytest.mark.parametrize('bank',['main','recovery'])
def test_changed_bank_owner_updates_only_its_own_accounts(sources,bank):
    target,value=('integration::recoveryBatteryWh','10') if bank=='recovery' else ('design::battery_Wh','900')
    mutant=set_values(sources, {'BlueDog::Configurations::IC01::'+target:value})
    before=load_model();after=connection().parse_sources(mutant,strict=True)
    features=[('fixedEquipment.massAllocation','kg','recovery'),('recoveryStorage.nameplateEnergy','J','recovery'),
        ('recoveryStorage.departureEnergy','J','recovery'),('mainStorage.nameplateEnergy','J','main'),('mainStorage.departureEnergy','J','main')]
    for feature,unit,owner in features:
        expression='BlueDog::Configurations::Management::ic01.'+feature+' / (1 ['+unit+'])'
        a=after.eval(expression,context_symbol_id='BlueDog::Configurations::Management')
        b=before.eval(expression,context_symbol_id='BlueDog::Configurations::Management')
        assert (a<b) if owner==bank else (a==b)
    assert not native_configuration_audit(mutant)['errors']

def test_rendered_configuration_budget_scopes_preserve_unknowns(rendered_site):
    architecture=(rendered_site/'imports/docs/architecture.md').read_text()
    energy=(rendered_site/'imports/docs/energy.md').read_text()
    assert 'Bingen Projection' in architecture and '| Actual article |' in architecture
    assert '| Peak bound |' in energy and 'not additive capacity' in energy

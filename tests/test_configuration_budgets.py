"""Native configuration applicability, accounting boundaries and meaningful negative controls."""
import pytest
from tools.boat_analysis.model.runtime import ROOT,connection,load_model,model_files
from tools.boat_analysis.model.configuration_audit import native_configuration_audit

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
    assert rows['retainedSizing']['cells'][2][0]['id']=='BlueDogSRRCurrent::candidate'
    assert rows['bingenProjection']['cells'][2][0]['id']=='BlueDogCurrentSizing::candidate'
    assert load_model().eval('BlueDogCurrentSizing::candidate.battery_Wh')!=440
    assert load_model().eval('BlueDogSRRCurrent::candidate.batteryWh')==440


@pytest.mark.parametrize('old,new,error',[
    ('ref part :>> representedSubject = BlueDogSRRCurrent::candidate;',
     'ref part :>> representedSubject = BlueDogCurrentSizing::candidate;','C02 Wrong represented subject'),
    ('ref part :>> design = BlueDogIC01::design;',
     'ref part :>> design = BlueDogCurrentSizing::candidate;','C04 Wrong planned installation reference'),
    ('ref part configuration : MarineDesign::Design [1] = BlueDogIC01::design;',
     'ref part configuration : MarineDesign::Design [1] = BlueDogCurrentSizing::candidate;','C07 Wrong accounting configuration'),
    ('BlueDogIC01::integration.fixedEquipmentKg * 1 [kg]',
     '(BlueDogIC01::integration.fixedEquipmentKg + BlueDogIC01::integration.recoveryBatteryWh/BlueDogIC01::integration.batteryWhKg) * 1 [kg]',
     'C10 Accounting binding differs'),
    ('BlueDogIC01::integration.electronicsW * 1 [W]',
     '(BlueDogIC01::integration.electronicsW + BlueDogIC01::integration.additionalBusW) * 1 [W]',
     'C10 Accounting binding differs'),
    ('BlueDogIC01::integration.recoveryEssentialW * 1 [W]',
     '-1 [W]','C07 Invalid allocated quantity'),
])
def test_substitution_double_counting_and_invalid_demand_are_detected(sources,old,new,error):
    mutant=tuple((p,t.replace(old,new)) if p.endswith('/management.sysml') else (p,t) for p,t in sources)
    assert mutant!=sources
    assert any(error in e for e in native_configuration_audit(mutant)['errors'])


def test_new_unclassified_top_level_design_is_detected(sources):
    extra='package ConfigurationTest { part candidate : MarineDesign::Design; }'
    assert 'C02 Unclassified top-level design/parameter part: ConfigurationTest::candidate' in native_configuration_audit((*sources,(str(ROOT/'reviews/unclassified-test.sysml'),extra)))['errors']


@pytest.mark.parametrize('missing',['articleId','hardwareRevision','softwareDataRevision','procedureRevision','reconciliationRecord'])
def test_missing_installation_identity_cannot_be_reconciled(sources,missing):
    values={k:'"synthetic-test-only"' for k in ('articleId','hardwareRevision','softwareDataRevision','procedureRevision','reconciliationRecord')}
    values.pop(missing)
    body=' '.join('attribute :>> '+k+' = '+v+';' for k,v in values.items())
    extra='''package InstallationTest { part example : BlueDogConfigurationManagement::PlannedInstallation {
        ref part :>> design = BlueDogIC01::design; ref part :>> assembly = BlueDogPhysicalArchitecture::ic01;
        attribute :>> reconciled = true;'''+body+'} }'
    m=connection().parse_sources((*sources,('installation.sysml',extra)),strict=True)
    assert m.eval('InstallationTest::example.configurationReconciled') is False


def test_empty_peak_is_not_zero_or_ready_even_with_synthetic_review_flags(sources):
    # Redefine the default review assertions in an isolated source mutation; preserve all equations.
    mutant=tuple((p,t.replace('attribute coverageReviewed : Boolean default = false;','attribute coverageReviewed : Boolean default = true;')
        .replace('attribute measurementsAccepted : Boolean default = false;','attribute measurementsAccepted : Boolean default = true;')
        .replace('attribute accountingReconciled : Boolean default = false;','attribute accountingReconciled : Boolean default = true;')
        .replace('attribute evidenceRecord : String [0..1];','attribute evidenceRecord : String [0..1] = "synthetic-test-only";'))
        if p.endswith('/management.sysml') else (p,t) for p,t in sources)
    m=connection().parse_sources(mutant,strict=True)
    assert m.eval('BlueDogConfigurationManagement::ic01.sailingElectronics.ready') is False
    assert m.eval('BlueDogConfigurationManagement::ic01.recoveryEssentials.ready') is False
    assert m.eval('BlueDogConfigurationManagement::ic01.wholeVesselMass.ready') is False
    assert m.eval('BlueDogConfigurationManagement::ic01.fixedEquipment.ready') is True


@pytest.mark.parametrize('bank',['main','recovery'])
def test_changed_bank_owner_updates_only_its_own_accounts(sources,bank):
    old,new=('attribute recoveryBatteryWh : Real = 60;','attribute recoveryBatteryWh : Real = 10;') if bank=='recovery' else (
        'attribute :>> battery_Wh = 1300;','attribute :>> battery_Wh = 900;')
    mutant=tuple((p,t.replace(old,new)) for p,t in sources)
    assert mutant!=sources
    before=load_model();after=connection().parse_sources(mutant,strict=True)
    features=[('fixedEquipment.massAllocation','kg','recovery'),('recoveryStorage.nameplateEnergy','J','recovery'),
        ('recoveryStorage.departureEnergy','J','recovery'),('mainStorage.nameplateEnergy','J','main'),('mainStorage.departureEnergy','J','main')]
    for feature,unit,owner in features:
        expression='BlueDogConfigurationManagement::ic01.'+feature+' / (1 ['+unit+'])'
        a=after.eval(expression,context_symbol_id='BlueDogConfigurationManagement')
        b=before.eval(expression,context_symbol_id='BlueDogConfigurationManagement')
        assert (a<b) if owner==bank else (a==b)
    assert not native_configuration_audit(mutant)['errors']

def test_rendered_configuration_budget_scopes_preserve_unknowns(rendered_site):
    architecture=(rendered_site/'imports/docs/architecture.md').read_text()
    energy=(rendered_site/'imports/docs/energy.md').read_text()
    assert 'Bingen Projection' in architecture and '| Actual article |' in architecture
    assert '| Peak bound |' in energy and 'not additive capacity' in energy

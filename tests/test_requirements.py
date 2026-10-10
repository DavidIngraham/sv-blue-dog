"""Integration checks for the native publishing outputs, not a second SysML parser."""
from types import SimpleNamespace
import json
from pathlib import Path
import re
import pytest
from scripts.render_requirements import native, native_graph, native_register, MODELS


ENERGY_LINKS = [('repeatedOperation', 'sustainedEnergyFeasibility'), ('hawaiiVoyage', 'sustainedEnergyFeasibility'), ('sustainedEnergyFeasibility', 'sustainedReserveProtection'), ('sustainedEnergyFeasibility', 'repeatableCycleBalance'), ('sustainedEnergyFeasibility', 'peakSupplyCapability'), ('sustainedEnergyFeasibility', 'energyEvidenceReadiness'), ('multiDayEndurance', 'sustainedReserveProtection'), ('multiDayEndurance', 'peakSupplyCapability'), ('multiDayEndurance', 'harvestCampaignCoverage'), ('multiDayEndurance', 'energyEvidenceReadiness'), ('recoveryEnergy', 'sustainedReserveProtection')]
ENERGY_IDS = {f'E-{i}' for i in range(200, 206)}
ATOMIC = json.loads(Path(__file__).with_name('atomic_requirements.json').read_text())

@pytest.fixture(scope="module")
def published_model():
    model = SimpleNamespace()
    model.dot = native_graph()
    model.markdown = native_register()
    model.nodes = dict(re.findall(r'"(n[0-9]+)" \[.*?<b>([A-Za-z0-9_:]+) :', model.dot))
    model.nodes = {key: name.rsplit("::", 1)[-1] for key, name in model.nodes.items()}
    links = re.findall(r'"(n[0-9]+)" -> "(n[0-9]+)" \[label="derive"', model.dot)
    model.edges = [(model.nodes[b], model.nodes[a]) for a, b in links]
    return model


def test_native_validation():
    native("-validate")

def test_challenge_is_standalone():
    native("-validate", models=MODELS[:1])

def test_diagram_preserves_expected_derivations(published_model):
    expected = {
        *(("transGorgeChallenge", target) for target in ["courseCompletion", "repeatedOperation", "unassistedAttempt", "sailingPropulsion", "liveObservation", "emergencyIntervention"]),
        *(("hawaiiVoyage", target) for target in ["multiDayEndurance", "navigationAndControl", "communications", "resetRecovery", "missionEvidence"]),
        ("courseCompletion", "roundTrip"), ("repeatedOperation", "multiDayEndurance"),
        ("unassistedAttempt", "navigationAndControl"), ("sailingPropulsion", "roundTrip"),
        ("liveObservation", "communications"), ("emergencyIntervention", "communications"),
        ("roundTrip", "navigationAndControl"), ("roundTrip", "resetRecovery"),
        ("roundTrip", "communications"), ("roundTrip", "ingressResponse"),
        ("roundTrip", "missionEvidence"), ("multiDayEndurance", "energyAwareness"),
        ("multiDayEndurance", "lowEnergyRecovery"), ("energyAwareness", "lowEnergyRecovery"),
    }
    expected.update([('roundTrip', 'transportability'), ('transportability', 'desktopManufacture'), ('desktopManufacture', 'serviceability'), ('navigationAndControl', 'trafficSafety'), ('roundTrip', 'operatingBoundary'), ('transportability', 'safeRecovery'), ('trafficSafety', 'navigationConspicuity'), ('roundTrip', 'regulatoryClassification'), ('roundTrip', 'environmentalEnvelope'), ('environmentalEnvelope', 'marineDurability'), ('environmentalEnvelope', 'stabilityAndFouling'), ('safeRecovery', 'recoveryPropulsion'), ('recoveryPropulsion', 'recoveryEnergy'), ('communications', 'telemetryEquipment'), ('communications', 'commandIntegrity'), ('hawaiiVoyage', 'environmentalEnvelope')])
    expected.update([('environmentalEnvelope', 'gorgeEnvironment'), ('environmentalEnvelope', 'oceanEnvironment'), ('gorgeEnvironment', 'gorgeWind'), ('gorgeEnvironment', 'gorgeWaves'), ('gorgeEnvironment', 'gorgeCurrent'), ('gorgeEnvironment', 'gorgeSurvivalWind'), ('gorgeEnvironment', 'gorgeSurvivalWaves'), ('oceanEnvironment', 'oceanWind'), ('oceanEnvironment', 'oceanWaves'), ('oceanEnvironment', 'oceanCurrent'), ('oceanEnvironment', 'oceanSurvivalWind'), ('oceanEnvironment', 'oceanSurvivalWaves'), ('environmentalEnvelope', 'airTemperature'), ('environmentalEnvelope', 'waterTemperature'), ('environmentalEnvelope', 'humidity'), ('environmentalEnvelope', 'visibility'), ('environmentalEnvelope', 'calmOperation'), ('environmentalEnvelope', 'envelopeTransition'), ('marineDurability', 'freshwaterExposure'), ('marineDurability', 'saltwaterExposure'), ('marineDurability', 'enclosureSealing'), ('marineDurability', 'wetMechanicalIntegrity'), ('marineDurability', 'wetElectricalIntegrity'), ('marineDurability', 'solarHeating'), ('marineDurability', 'printedMaterialAging'), ('stabilityAndFouling', 'selfRighting'), ('stabilityAndFouling', 'capsizeControlRecovery'), ('stabilityAndFouling', 'submergedWeedPassage'), ('stabilityAndFouling', 'weedSnagShedding'), ('stabilityAndFouling', 'weedBlockageResponse'), ('stabilityAndFouling', 'recoveryPropulsorWeeds'), ('recoveryPropulsion', 'recoveryPropulsorWeeds')])
    expected.difference_update([('transportability', 'desktopManufacture'), ('desktopManufacture', 'serviceability'), ('transportability', 'safeRecovery'), ('environmentalEnvelope', 'gorgeEnvironment'), ('environmentalEnvelope', 'oceanEnvironment')])
    expected.update([('roundTrip', 'desktopManufacture'), ('repeatedOperation', 'serviceability'), ('emergencyIntervention', 'safeRecovery'), ('roundTrip', 'gorgeEnvironment'), ('hawaiiVoyage', 'oceanEnvironment'), ('navigationAndControl', 'navigationAvailability'), ('recoveryEnergy', 'launchEnergyAdmission'), ('sailingPropulsion', 'challengeMotorInhibition'), ('unassistedAttempt', 'challengeMotorInhibition'), ('unassistedAttempt', 'commandIntegrity'), ('emergencyIntervention', 'commandIntegrity'), ('hawaiiVoyage', 'operatingBoundary'), ('hawaiiVoyage', 'regulatoryClassification'), ('hawaiiVoyage', 'serviceability'), ('gorgeEnvironment', 'freshwaterExposure'), ('oceanEnvironment', 'saltwaterExposure'), ('gorgeEnvironment', 'submergedWeedPassage'), ('gorgeEnvironment', 'weedSnagShedding')])
    expected.update((r['parent'], r['usage']) for r in ATOMIC['leaves'])
    expected.update(tuple(edge) for edge in ATOMIC['shared_links'])
    expected.update(ENERGY_LINKS)
    assert set(published_model.edges) == expected
    assert len(published_model.edges) == len(expected)
    assert len({name for edge in published_model.edges for name in edge}) == 66 + len(ATOMIC['leaves']) + len(ENERGY_IDS)

def test_use_case_and_satisfaction_traceability():
    text = native("-render-document", "BlueDogDocuments::Traceability")
    for case, requirement in [('prepare', 'transportability'), ('sailGorge', 'roundTrip'),
                              ('sailOcean', 'hawaiiVoyage'), ('monitor', 'telemetryEquipment'),
                              ('recover', 'safeRecovery'), ('maintain', 'serviceability'),
                              ('avoidTraffic', 'trafficSafety'), ('presentNavigationSignals', 'navigationConspicuity')]:
        assert re.search(f'\\| {case} \\|[^\\n]+\\| {requirement} \\|', text)
    assert '| recoveryPropulsion | boat |' in text
    assert '| commandIntegrity | commandGateway |' in text
    assert '| regulatoryClassification |  |' in text
    diagram = native('-render', 'BlueDogUseCaseViews::operations', '-render-form', 'dot')
    assert '// kind: case' in diagram
    assert 'P-001 Transportability' in diagram
    assert 'OtherVessel' in diagram
    context = native('-render', 'BlueDogArchitectureViews::context', '-render-form', 'dot')
    assert 'OtherVessel' in context

def test_exactly_two_top_level_drivers(published_model):
    roots = {source for source, _ in published_model.edges} - {target for _, target in published_model.edges}
    assert roots == {'transGorgeChallenge', 'hawaiiVoyage'}

def test_register_preserves_ids_status_and_relationships(published_model):
    ids = re.findall(r"^\| ([CHEMPNSR]-[0-9]+) \|", published_model.markdown, re.MULTILINE)
    expected = {"H-001", "M-001", "M-002",
                *(f"C-00{i}" for i in range(7)), *(f"E-00{i}" for i in range(1, 8))}
    expected.update(['P-001', 'P-002', 'P-003', 'S-001', 'S-002', 'S-003', 'S-004', 'S-005', 'N-001', 'N-002', 'N-003', 'R-001', 'R-002', 'C-101', 'C-102'])
    expected.update(['N-010', 'N-020', 'N-011', 'N-012', 'N-013', 'N-014', 'N-015', 'N-021', 'N-022', 'N-023', 'N-024', 'N-025', 'N-030', 'N-031', 'N-032', 'N-033', 'N-034', 'N-035', 'N-041', 'N-042', 'N-043', 'N-044', 'N-045', 'N-046', 'N-047', 'N-051', 'N-052', 'N-053', 'N-054', 'N-055', 'N-056'])
    expected.update(['E-008', 'R-003', 'R-004'])
    expected.update(r['id'] for r in ATOMIC['leaves'])
    expected.update(ENERGY_IDS)
    assert set(ids) == expected
    assert len(ids) == len(expected)
    for source, target in published_model.edges:
        assert f'| {source} | {target} | open |' in published_model.markdown
    rows = [line for line in published_model.markdown.splitlines() if line.startswith('| ')]
    assert len(rows) == len(expected) + len(published_model.edges) + 4
    data = [line for line in rows if line not in (
        '| ID | Requirement | Status | Statement |',
        '| Original | Derived | Status | Rationale |', '| --- | --- | --- | --- |')]
    assert all((' | open | ' in line for line in data))

"""Integration checks for the native publishing outputs, not a second SysML parser."""
from types import SimpleNamespace
import json
from pathlib import Path
import re
import pytest
from scripts.render_requirements import native, native_graph, native_register, MODELS


RELIABILITY_IDS = {'L-101', 'Q-101', 'Q-102', 'L-103', 'L-001', 'Q-001', 'L-104', 'Q-103', 'L-102'}
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
    assert not json.loads(native("-validate", "-json"))["diagnostics"]

def test_challenge_is_standalone():
    native("-validate", models=MODELS[:1])

def test_diagram_preserves_expected_derivations(published_model):
    expected = {
        ('cruisePerformance', 'cruiseEvidence'),
        ('cruisePerformance', 'legProgress'),
        ('cruisePerformance', 'passageDuration'),
        ('environmentalEnvelope', 'airTemperature'),
        ('environmentalEnvelope', 'calmOperation'),
        ('environmentalEnvelope', 'envelopeTransition'),
        ('environmentalEnvelope', 'humidity'),
        ('environmentalEnvelope', 'visibility'),
        ('environmentalEnvelope', 'waterTemperature'),
        ('gorgeEnvironment', 'freshwaterExposure'),
        ('gorgeEnvironment', 'gorgeCurrent'),
        ('gorgeEnvironment', 'gorgeSurvivalWaves'),
        ('gorgeEnvironment', 'gorgeSurvivalWind'),
        ('gorgeEnvironment', 'gorgeWaves'),
        ('gorgeEnvironment', 'gorgeWind'),
        ('gorgeEnvironment', 'submergedWeedPassage'),
        ('gorgeEnvironment', 'weedSnagShedding'),
        ('marineDurability', 'enclosureSealing'),
        ('marineDurability', 'freshwaterExposure'),
        ('marineDurability', 'printedMaterialAging'),
        ('marineDurability', 'saltwaterExposure'),
        ('marineDurability', 'solarHeating'),
        ('marineDurability', 'wetElectricalIntegrity'),
        ('marineDurability', 'wetMechanicalIntegrity'),
        ('missionReliability', 'criticalFailureDisposition'),
        ('missionReliability', 'failureRateBudget'),
        ('missionReliability', 'missionSuccessProbability'),
        ('missionReliability', 'reliabilityEvidence'),
        ('multiDayEndurance', 'energyEvidenceReadiness'),
        ('multiDayEndurance', 'harvestCampaignCoverage'),
        ('multiDayEndurance', 'peakSupplyCapability'),
        ('multiDayEndurance', 'sustainedReserveProtection'),
        ('navigationAndControl', 'navigationAvailability'),
        ('oceanEnvironment', 'oceanCurrent'),
        ('oceanEnvironment', 'oceanSurvivalWaves'),
        ('oceanEnvironment', 'oceanSurvivalWind'),
        ('oceanEnvironment', 'oceanWaves'),
        ('oceanEnvironment', 'oceanWind'),
        ('oceanEnvironment', 'saltwaterExposure'),
        ('stabilityAndFouling', 'capsizeControlRecovery'),
        ('stabilityAndFouling', 'recoveryPropulsorWeeds'),
        ('stabilityAndFouling', 'selfRighting'),
        ('stabilityAndFouling', 'submergedWeedPassage'),
        ('stabilityAndFouling', 'weedBlockageResponse'),
        ('stabilityAndFouling', 'weedSnagShedding'),
        ('sustainedEnergyFeasibility', 'energyEvidenceReadiness'),
        ('sustainedEnergyFeasibility', 'peakSupplyCapability'),
        ('sustainedEnergyFeasibility', 'repeatableCycleBalance'),
        ('sustainedEnergyFeasibility', 'sustainedReserveProtection'),
        ('transGorgeChallenge', 'courseCompletion'),
        ('transGorgeChallenge', 'emergencyIntervention'),
        ('transGorgeChallenge', 'liveObservation'),
        ('transGorgeChallenge', 'repeatedOperation'),
        ('transGorgeChallenge', 'sailingPropulsion'),
        ('transGorgeChallenge', 'unassistedAttempt'),
    }
    expected.update((r['parent'], r['usage']) for r in ATOMIC['leaves'])
    expected.update(tuple(edge) for edge in ATOMIC['shared_links'])
    assert set(published_model.edges) == expected
    assert len(published_model.edges) == len(expected)


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

def test_mission_drivers_do_not_entail_owner_constraints(published_model):
    # Two mission goals do not mean every requirement is a logical consequence of them.
    edges = set(published_model.edges)
    for constraint in ['transportability', 'desktopManufacture', 'serviceability']:
        assert not any(child == constraint for _, child in edges)
    report = native('-render-document', 'BlueDogDocuments::RelationshipRegister')
    for constraint in ['transportability', 'desktopManufacture', 'serviceability']:
        assert f'| {constraint} | DesignIntent |' in report
    assert '| multiDayEndurance | hawaiiVoyage |' in report
    assert ('sailingPropulsion', 'roundTrip') not in edges
    assert ('hawaiiVoyage', 'sustainedEnergyFeasibility') not in edges

def test_register_preserves_ids_status_and_relationships(published_model):
    ids = re.findall(r"^\| ([CHEMPNSRQL]-[0-9]+) \|", published_model.markdown, re.MULTILINE)
    expected = {"H-001", "M-001", "M-002",
                *(f"C-00{i}" for i in range(7)), *(f"E-00{i}" for i in range(1, 8))}
    expected.update(['P-001', 'P-002', 'P-003', 'S-001', 'S-002', 'S-003', 'S-004', 'S-005', 'N-001', 'N-002', 'N-003', 'R-001', 'R-002', 'C-101', 'C-102'])
    expected.update(['N-010', 'N-020', 'N-011', 'N-012', 'N-013', 'N-014', 'N-015', 'N-021', 'N-022', 'N-023', 'N-024', 'N-025', 'N-030', 'N-031', 'N-032', 'N-033', 'N-034', 'N-035', 'N-041', 'N-042', 'N-043', 'N-044', 'N-045', 'N-046', 'N-047', 'N-051', 'N-052', 'N-053', 'N-054', 'N-055', 'N-056'])
    expected.update(['E-008', 'R-003', 'R-004'])
    expected.update(r['id'] for r in ATOMIC['leaves'])
    expected.update(ENERGY_IDS)
    expected.update(RELIABILITY_IDS)
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


def test_focused_views_cover_all_derivations(published_model):
    # The full native graph is an oracle only; readers receive bounded views.
    edges = set()
    refinements = set()
    pages = list(Path('docs/figures').glob('requirements-*.md'))
    assert len(pages) == 49
    assert not Path('docs/figures/requirements-derivation.md').exists()
    for page in pages:
        import re
        for diagram in re.findall(r'```mermaid\n(.*?)```', page.read_text(encoding='utf-8'), re.S):
            nodes = dict(re.findall(r'(n[0-9]+)\("`.*?\*\*([A-Za-z0-9_:]+) :', diagram, re.S))
            nodes = {key: name.rsplit('::', 1)[-1] for key, name in nodes.items()}
            assert 2 <= len(nodes) <= 4, page
            assert 'flowchart BT' in diagram
            for child, parent in re.findall(r'(n[0-9]+) -\.->\|"derive"\| (n[0-9]+)', diagram):
                edges.add((nodes[parent], nodes[child]))
            for detail, abstract in re.findall(r'(n[0-9]+) -\.->\|"refine"\| (n[0-9]+)', diagram):
                refinements.add((nodes[detail], nodes[abstract]))
    assert edges == set(published_model.edges)
    assert refinements == {('roundTrip', 'courseCompletion'), ('communications', 'liveObservation')}


def test_statements_exclude_supporting_material(published_model):
    statement_rows = re.findall(r'^\| [A-Z]-\d+ \| \w+ \| open \| (.*?) \|$',
                                published_model.markdown, re.M)
    assert len(statement_rows) == 208
    assert all(len(text.split()) <= 45 for text in statement_rows)
    assert all('Verification uses' not in text and 'Aggregate requirement' not in text
               and 'Shared verification context' not in text for text in statement_rows)
    context = native('-render-document', 'BlueDogDocuments::RequirementContext')
    for text in ['Qualification conditions (normative)', '## Rationale', '## Open issues',
                 '1800 scheduled one-second epochs', '20 flexible branched stems',
                 '600 seconds', 'V-N-053', 'weedPassageSpeed, weedPassageSteering']:
        assert text in context


def test_planned_verification_cannot_report_a_pass(run_model):
    code, report = run_model('package VerificationProbe {}', '-analysis',
                            'BlueDogRequirementVerification::EnergyAwarenessVerification')
    assert code != 0
    assert not [d for d in report['diagnostics'] or [] if d['pass'] != 'runtime']
    values = {v['name']: v['value'] for v in report['checks'][0]['values']}
    assert values['verdict'] == 'VerdictKind::inconclusive'

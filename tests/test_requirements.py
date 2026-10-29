"""Integration checks for the native publishing outputs, not a second SysML parser."""
from types import SimpleNamespace
import json
from pathlib import Path
import re
import pytest
from tests.native_cases import native, native_graph, native_register, MODELS


RELIABILITY_IDS = {'L-101', 'Q-101', 'Q-102', 'L-103', 'L-001', 'Q-001', 'L-104', 'Q-103', 'L-102'}
STRUCTURE_LEAVES = {'bendingStrength', 'appendageDeflection', 'hullDeflection', 'panelStrength', 'panelDeflection', 'rootProofLoad', 'wetCouponStrength', 'wetCouponStiffness', 'bondProof'}
STRUCTURE_IDS = {'T-001', *(f'T-{i}' for i in range(100, 114))}
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
    links = re.findall(r'"(n[0-9]+)" -> "(n[0-9]+)" \[label="refine"', model.dot)
    model.refinements = {(model.nodes[a], model.nodes[b]) for a, b in links
                         if a in model.nodes and b in model.nodes}
    return model


def test_native_validation():
    assert not json.loads(native("-validate", "-json"))["diagnostics"]

def test_challenge_is_standalone():
    from tools.boat_analysis.model.runtime import ROOT, connection, load_model
    path=ROOT/'models/gorge-challenge.sysml'
    challenge=connection().parse_sources(((str(path),path.read_text()),),strict=True)
    assert challenge.get('GorgeChallenge::transGorgeChallenge') is not None
    assert challenge.get('BlueDog') is None
    integrated=load_model()
    assert integrated.get('BlueDog::Mission::Challenge') is None
    assert integrated.get('GorgeChallenge').id=='GorgeChallenge'
    assert integrated.get('BlueDog::Mission::Course::policy') is not None
    assert integrated.get('BlueDog::Requirements::Communications::monitoringTechnologyIssue') is not None


def test_standalone_challenge_rejects_a_boat_dependency():
    from opensysml.errors import ModelError
    from tools.boat_analysis.model.runtime import ROOT, connection
    path=ROOT/'models/gorge-challenge.sysml'
    source=path.read_text()
    probe='package BoatCouplingProbe { dependency invalid from GorgeChallenge::transGorgeChallenge to BlueDog::Requirements::roundTrip; }'
    # This check must fail if a boat reference is introduced without its model.
    with pytest.raises(ModelError) as error:
        connection().parse_sources(((str(path),source),('coupling-probe.sysml',probe)),strict=True)
    assert 'BlueDog' in str(error.value)


def test_diagram_preserves_expected_derivations(published_model):
    # Deliberate aggregate implications remain; chosen allocations do not.
    expected = {tuple(edge) for edge in ATOMIC['aggregate_derivations']}
    assert set(published_model.edges) == expected
    assert len(published_model.edges) == len(expected) == 67
    for edge in [('energyAwareness', 'energyEstimateCadence'),
                 ('trafficCoexistence', 'trafficSafety'),
                 ('navigationRules', 'navigationConspicuity'),
                 ('resetRecovery', 'logInterruptionDurability')]:
        assert edge not in expected
    for detail, general in [('energyEstimateCadence', 'energyAwareness'),
                            ('trafficSafety', 'trafficCoexistence'),
                            ('submergedWeedPassage', 'vegetationResilience')]:
        assert (detail, general) in published_model.refinements


def test_use_case_and_satisfaction_traceability():
    text = native("-render-document", "BlueDogDocuments::Traceability")
    for case, requirement in [('prepare', 'transportability'), ('sailGorge', 'roundTrip'),
                              ('sailOcean', 'hawaiiVoyage'), ('monitor', 'telemetryEquipment'),
                              ('recover', 'emergencyControl'), ('maintain', 'serviceability'),
                              ('avoidTraffic', 'trafficSafety'), ('presentNavigationSignals', 'navigationConspicuity')]:
        assert re.search(f'\\| {case} \\|[^\\n]+\\| {requirement} \\|', text)
    assert '| recoveryPropulsion | boat |' in text
    assert '| commandIntegrity | commandGateway |' in text
    assert '| regulatoryClassification |  |' in text
    for deferred in ['oceanEnvironment', 'oceanWind', 'oceanWaves', 'oceanCurrent',
                     'oceanSurvivalWind', 'oceanSurvivalWaves', 'saltwaterExposure',
                     'sustainedEnergyFeasibility', 'repeatableCycleBalance']:
        assert f'| {deferred} |  |' in text
    diagram = native('-render', 'Page_architecture_2::operations', '-render-form', 'dot')
    assert '// kind: case' in diagram
    # The published operations view is now scoped to sailing and traffic.
    # Preparation/transportability remains checked in the full register above.
    assert 'M-001 Gorge mission' in diagram
    assert 'S-001 Traffic safety' in diagram
    assert 'OtherVessel' in diagram
    context = native('-render', 'Page_architecture_0::context', '-render-form', 'dot')
    assert 'OtherVessel' in context

def test_mission_drivers_do_not_entail_owner_constraints(published_model):
    # Two mission goals do not mean every requirement is a logical consequence of them.
    edges = set(published_model.edges)
    for constraint in ['transportability', 'desktopManufacture', 'serviceability']:
        assert not any(child == constraint for _, child in edges)
    report = native('-render-document', 'BlueDogDocuments::RelationshipRegister')
    for constraint in ['transportability', 'desktopManufacture', 'serviceability']:
        assert f'| {constraint} | DesignIntent |' in report
    assert '| multiDayEndurance | hawaiiVoyage |' not in report
    assert '| multiDayEndurance | roundTrip |' in report
    assert ('sailingPropulsion', 'roundTrip') not in edges
    assert ('hawaiiVoyage', 'sustainedEnergyFeasibility') not in edges

def test_register_preserves_ids_status_and_relationships(published_model):
    ids = re.findall(r"^\| ([CHEMPNSRQLT]-[0-9]+) \|", published_model.markdown, re.MULTILINE)
    expected = {"H-001", "M-001", "M-002",
                *(f"C-00{i}" for i in range(10)), *(f"E-00{i}" for i in range(1, 8))}
    expected.update(['P-001', 'P-002', 'P-003', 'S-001', 'S-002', 'S-003', 'S-004', 'S-005', 'N-001', 'N-002', 'N-003', 'R-001', 'R-002', 'C-101', 'C-102'])
    expected.update(['N-010', 'N-020', 'N-011', 'N-012', 'N-013', 'N-014', 'N-015', 'N-021', 'N-022', 'N-023', 'N-024', 'N-025', 'N-030', 'N-031', 'N-032', 'N-033', 'N-034', 'N-035', 'N-041', 'N-042', 'N-043', 'N-044', 'N-045', 'N-046', 'N-047', 'N-051', 'N-052', 'N-053', 'N-054', 'N-055', 'N-056'])
    expected.update(['E-008', 'E-009', 'R-003', 'R-004'])
    expected.update(r['id'] for r in ATOMIC['leaves'])
    expected.update(f"C-{i:03d}" for i in range(10, 28) if i != 11)
    expected.update(ENERGY_IDS)
    expected.update(RELIABILITY_IDS)
    expected.update(STRUCTURE_IDS)
    expected.update(['N-004', *(f'C-{i:03d}' for i in range(28, 33))])
    assert set(ids) == expected
    assert len(ids) == len(expected)
    for source, target in published_model.edges:
        # Construction relations have no status metadata; their requirement
        # definitions do. Do not manufacture an 'open' value in the publisher.
        status = '' if source == 'structuralIntegrity' else 'open'
        assert f'| {source} | {target} | {status} |' in published_model.markdown
    rows = [line for line in published_model.markdown.splitlines() if line.startswith('| ')]
    assert len(rows) == len(expected) + len(published_model.edges) + 4
    data = [line for line in rows if line not in (
        '| ID | Requirement | Status | Statement |',
        '| Original | Derived | Status | Rationale |', '| --- | --- | --- | --- |')]
    assert all(' | open | ' in line or line.startswith('| structuralIntegrity | ') for line in data)


def test_focused_views_cover_all_derivations(published_model, rendered_site):
    # The full native graph is an oracle only; readers receive bounded views.
    edges = set()
    refinements = set()
    pages = [rendered_site / 'imports/docs/requirements' / p.name
             for p in Path('docs/requirements').glob('requirements-*.md')]
    assert len(pages) == 6
    assert not Path('docs/figures/requirements-derivation.md').exists()
    for page in pages:
        import re
        for diagram in re.findall(r'```mermaid\n(.*?)```', page.read_text(encoding='utf-8'), re.S):
            from tools.publishing.relationships import diagram_nodes
            nodes = diagram_nodes(diagram)
            nodes = {key: name.rsplit('::', 1)[-1] for key, name in nodes.items()}
            assert 1 <= len(nodes) <= 40, page
            assert 'flowchart BT' in diagram
            for child, parent in re.findall(r'(n[0-9]+) -\.->\|"derive"\| (n[0-9]+)', diagram):
                edges.add((nodes[parent], nodes[child]))
            for detail, abstract in re.findall(r'(n[0-9]+) -\.->\|"refine"\| (n[0-9]+)', diagram):
                refinements.add((nodes[detail], nodes[abstract]))
    assert edges == set(published_model.edges)
    assert refinements == published_model.refinements


def test_statements_exclude_supporting_material(published_model):
    statement_rows = re.findall(r'^\| [A-Z]-\d+ \| \w+ \| open \| (.*?) \|$',
                                published_model.markdown, re.M)
    assert len(statement_rows) == 242 + len(STRUCTURE_IDS)
    assert all(len(text.split()) <= 45 for text in statement_rows)
    assert all('Verification uses' not in text and 'Aggregate requirement' not in text
               and 'Shared verification context' not in text for text in statement_rows)
    context = native('-render-document', 'BlueDogDocuments::RequirementContext')
    for text in ['Qualification conditions (normative)', '## Rationale', '## Open issues',
                 '1800 scheduled one-second epochs', '20 flexible branched stems',
                 '600 seconds', 'V-N-053', 'weedPassageSpeed, weedPassageSteering']:
        assert text in context


@pytest.mark.parametrize('case', [
    'BlueDog::Verification::Requirements::EnergyAwarenessVerification',
    'BlueDog::Verification::Challenge::PassageQualificationVerification',
    'BlueDog::Verification::Requirements::CapsizeResilienceVerification',
    'BlueDog::Verification::Requirements::VegetationResilienceVerification',
    'BlueDog::Verification::Requirements::MissionPerformanceAssessmentVerification',
    'BlueDog::Verification::Requirements::ReliabilityEvidenceVerification',
    'BlueDog::Verification::Requirements::PeakSupplyCapabilityVerification',
    'BlueDog::Verification::Requirements::ConstructionArchitectureVerification',
])
def test_planned_verification_cannot_report_a_pass(run_model, case):
    code, report = run_model('package VerificationProbe {}', '-analysis',
                            case)
    assert code != 0
    assert not [d for d in report['diagnostics'] or [] if d['pass'] != 'runtime']
    values = {v['name']: v['value'] for v in report['checks'][0]['values']}
    assert values['verdict'] == 'VerdictKind::inconclusive'


@pytest.mark.parametrize("view,actions", [
    ("normal", ("ObserveWind", "SelectSailingCommand", "ApplySailingCommand")),
    ("traffic", ("ObserveTraffic", "ObserveNavigation", "AssessEncounter", "SelectAvoidanceManeuver", "ExecuteAndReassess")),
    ("recovery", ("LatchAbort", "RecordAndSignalAbort", "ObserveNavigation", "ObserveTraffic", "AssessRecoveryBoundary", "ObserveReserve", "SelectReachableShore", "RecoverAndReassess", "PersistRecoveryAuthorization", "ApplyRecoveryCommand", "RecordRecoveryOutcome")),
])
def test_oosem_scenarios_render_declared_behavior(view, actions):
    diagram = native("-render", f"Page_architecture_{view}::scenario", "-render-form", "mermaid")
    assert "declares no nodes" not in diagram
    for action in actions:
        assert action in diagram
    assert diagram.count(" --> ") == len(actions) - 1


def test_oosem_context_exposes_mission_participants():
    diagram = native("-render", "Page_architecture_0::context", "-render-form", "mermaid")
    for participant in ("Boat", "Operator", "ShoreSupport", "Environment", "OtherVessel"):
        assert f": {participant}" in diagram

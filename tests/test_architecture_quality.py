"""Native architecture coverage, configuration and meaningful missing-link controls."""
import pytest

from tools.boat_analysis.model.architecture_audit import native_architecture_audit
from tools.boat_analysis.model.runtime import model_files


@pytest.fixture(scope='module')
def sources():
    return tuple((str(p), p.read_text()) for p in model_files())


def altered(sources, old, new, file):
    assert sum(text.count(old) for path,text in sources if path.endswith(file)) == 1
    return tuple((path,text.replace(old,new) if path.endswith(file) else text) for path,text in sources)


def test_scenarios_responsibilities_and_exchanges_have_native_correspondences(sources):
    report = native_architecture_audit(sources)
    assert not report['diagnostics']
    assert not report['errors']
    assert report['summary']['scenarios'] == 9
    assert report['summary']['scenarioSteps'] == 41
    assert report['summary']['logicalResponsibilities'] == 14
    assert report['summary']['logicalExchanges'] == 28
    assert report['tables']['OpenDecisions']['rows'][0]['cells'][0]


def test_missing_recovery_scenario_owner_is_detected(sources):
    src = altered(sources,
        'allocate abortAndRecover.actuate to BlueDogLogicalArchitecture::vessel.recoveryActuation;',
        '', '/vehicle/method.sysml')
    assert 'L01 Unowned scenario action: BlueDogMethod::Scenarios::AbortAndRecover::actuate' in native_architecture_audit(src)['errors']


def test_missing_propulsion_responsibility_allocation_is_detected(sources):
    block = '''    allocation recoveryActuation : IC01Responsibility allocate vessel.recoveryActuation to ic01.recoveryPropulsor {
        attribute :>> path = ImplementationPath::recovery;
        attribute :>> scope = "Execute permitted recovery commands; achieved upright/inverted thrust remains unverified";
    }
'''
    src = altered(sources, block, '', '/vehicle/architecture-contracts.sysml')
    assert 'L02 Missing candidate allocation: BlueDogLogicalArchitecture::LogicalVessel::recoveryActuation' in native_architecture_audit(src)['errors']


def test_missing_recovery_command_mapping_is_detected(sources):
    block = '''    allocation recoveryCommandsRecoveryCommandData : IC01Exchange allocate vessel.recoveryCommands to ic01.recoveryCommandData {
        attribute :>> path = ImplementationPath::recovery;
        attribute :>> scope = "Candidate payload transfer; installed timing, transport and fault handling remain to be specified";
    }
'''
    src = altered(sources, block, '', '/vehicle/architecture-contracts.sysml')
    assert 'I01 Unmapped logical exchange: BlueDogLogicalArchitecture::LogicalVessel::recoveryCommands' in native_architecture_audit(src)['errors']


def test_archived_design_cannot_become_the_candidate_mapping_subject(sources):
    old = 'ref part configuration : MarineDesign::Design = BlueDogIC01::design;'
    # Override one allocation convention, not the archived study or its values.
    block = '''    allocation def IC01Responsibility {
        end part logical;
        end part implementation;
        '''+old
    src = altered(sources, block, block.replace('BlueDogIC01::design','BlueDogSRRCurrent::candidate'), '/vehicle/architecture-contracts.sysml')
    errors = native_architecture_audit(src)['errors']
    assert 'C01 Wrong or missing candidate configuration: BlueDogArchitectureCorrespondence::recoveryManagement' in errors


def test_operator_cannot_replace_candidate_propulsion_allocation(sources):
    src = altered(sources,
        'allocate vessel.recoveryActuation to ic01.recoveryPropulsor',
        'allocate vessel.recoveryActuation to missionContext.operator', '/vehicle/architecture-contracts.sysml')
    assert any(e.startswith('L03 Invalid candidate responsibility target: BlueDogLogicalArchitecture::LogicalVessel::recoveryActuation')
               for e in native_architecture_audit(src)['errors'])


def test_scope_is_required_for_shared_implementation_claims(sources):
    src = altered(sources,
        'attribute :>> scope = "Recovery-side qualification restrictions and fallback authority; primary-loss arbitration remains open";',
        'attribute :>> scope = "";', '/vehicle/architecture-contracts.sysml')
    assert 'L02 Unscoped allocation: BlueDogArchitectureCorrespondence::recoverySupervision' in native_architecture_audit(src)['errors']


def test_rendered_architecture_tables_identify_both_sides(rendered_site):
    text = (rendered_site/'imports/docs/architecture.md').read_text()
    assert '| Logical responsibility | Implementation |' in text
    assert '| Logical exchange | Implementation |' in text
    # Native rendering inserts word boundaries into camel-case identifiers.
    # Compare the two cells together without making that typography a contract.
    rows = [[ ''.join(cell.split()).casefold() for cell in line.split('|')[1:-1] ]
            for line in text.splitlines() if line.startswith('|')]
    assert ['recoveryactuation', 'recoverypropulsor'] in rows
    assert ['recoverycommands', 'recoverycommanddata'] in rows


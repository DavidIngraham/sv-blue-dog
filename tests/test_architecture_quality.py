"""Native architecture coverage, configuration and meaningful missing-link controls."""
import pytest

from tools.boat_analysis.model.architecture_audit import native_architecture_audit
from tools.boat_analysis.model.runtime import model_files
from tests.native_edits import replace_unique, set_values, delete_symbols


@pytest.fixture(scope='module')
def sources():
    return tuple((str(p), p.read_text()) for p in model_files())


def altered(sources, old, new):
    # A former source file now shares the canonical project document.
    return replace_unique(sources, old, new)


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
        'allocate abortAndRecover.actuate to BlueDog::Architecture::Logical::vessel.recoveryActuation;',
        '')
    assert 'L01 Unowned scenario action: BlueDog::Method::Scenarios::AbortAndRecover::actuate' in native_architecture_audit(src)['errors']


def test_missing_propulsion_responsibility_allocation_is_detected(sources):
    src = delete_symbols(sources, 'BlueDog::Architecture::Correspondence::recoveryActuation')
    assert 'L02 Missing candidate allocation: BlueDog::Architecture::Logical::LogicalVessel::recoveryActuation' in native_architecture_audit(src)['errors']


def test_missing_recovery_command_mapping_is_detected(sources):
    src = delete_symbols(sources, 'BlueDog::Architecture::Correspondence::recoveryCommandsRecoveryCommandData')
    assert 'I01 Unmapped logical exchange: BlueDog::Architecture::Logical::LogicalVessel::recoveryCommands' in native_architecture_audit(src)['errors']


def test_archived_design_cannot_become_the_candidate_mapping_subject(sources):
    # Change the allocation convention, not any archived configuration values.
    src = set_values(sources, {
        'BlueDog::Architecture::Contracts::IC01Responsibility::configuration':
        'BlueDog::Evidence::SRRCurrent::candidate',
    })
    errors = native_architecture_audit(src)['errors']
    assert 'C01 Wrong or missing candidate configuration: BlueDog::Architecture::Correspondence::recoveryManagement' in errors


def test_operator_cannot_replace_candidate_propulsion_allocation(sources):
    src = altered(sources,
        'allocate vessel.recoveryActuation to ic01.recoveryPropulsor',
        'allocate vessel.recoveryActuation to missionContext.operator')
    assert any(e.startswith('L03 Invalid candidate responsibility target: BlueDog::Architecture::Logical::LogicalVessel::recoveryActuation')
               for e in native_architecture_audit(src)['errors'])


def test_scope_is_required_for_shared_implementation_claims(sources):
    src = set_values(sources, {
        'BlueDog::Architecture::Correspondence::recoverySupervision::scope': '""',
    })
    assert 'L02 Unscoped allocation: BlueDog::Architecture::Correspondence::recoverySupervision' in native_architecture_audit(src)['errors']


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


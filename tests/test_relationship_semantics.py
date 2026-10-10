"""Check published native semantics and their bounded embedded views."""
from pathlib import Path
import re

import pytest

from scripts.render_requirements import native


@pytest.fixture(scope='module')
def relationship_report():
    return native('-render-document', 'BlueDogDocuments::RelationshipRegister')


def test_formal_refinements_are_distinct_from_design_dependencies(relationship_report):
    refinements, dependencies = relationship_report.split('## Plain dependency')
    for source, target in [
        ('roundTrip', 'courseCompletion'), ('communications', 'liveObservation'),
        ('SustainedReserveProtectionCriterion', 'sustainedReserveProtection'),
        ('RepeatableCycleBalanceCriterion', 'repeatableCycleBalance'),
        ('PeakSupplyCapabilityCriterion', 'peakSupplyCapability'),
        ('HarvestCampaignCoverageCriterion', 'harvestCampaignCoverage'),
        ('LegProgressCriterion', 'legProgress'), ('PassageDurationCriterion', 'passageDuration'),
        ('MissionReliabilityCriterion', 'missionSuccessProbability'), ('FailureRateCriterion', 'failureRateBudget'),
    ]:
        assert f'| {source} | {target} |' in refinements
        assert f'| {source} | {target} |' not in dependencies
    # Numerical screening is a refinement; merely assessing a requirement is not.
    assert 'CruiseReliability |' not in refinements
    assert 'EnergyEvidenceReadinessCriterion |' not in refinements
    assert '| recoveryPropulsion | safeRecovery |' in dependencies
    assert '| desktopManufacture | DesignIntent |' in dependencies


@pytest.mark.parametrize('slug,kinds', [
    ('mission-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('energy-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('cruise-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('reliability-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('manufacturing-semantics', {'satisfy', 'verify'}),
    ('weed-semantics', {'derive', 'satisfy', 'verify'}),
])
def test_semantic_diagrams_are_small_connected_native_views(slug, kinds):
    text = Path(f'docs/figures/{slug}.md').read_text(encoding='utf-8')
    nodes = set(re.findall(r'^  (n\d+)[(\[]', text, re.M))
    edges = re.findall(r'(n\d+) -\.->\|"(\w+)"\| (n\d+)', text)
    assert 3 <= len(nodes) <= 5
    assert {kind for _, kind, _ in edges} == kinds
    assert {node for a, _, b in edges for node in [a, b]} == nodes
    assert 'flowchart BT' in text
    seen = {next(iter(nodes))}
    while True:
        reachable = {node for a, _, b in edges if a in seen or b in seen for node in [a, b]}
        if reachable <= seen:
            break
        seen |= reachable
    assert seen == nodes


def test_authored_pages_embed_the_generated_diagrams_only():
    count = 0
    for name in ['design-guide', 'sustained-operations', 'cruise-reliability']:
        text = Path(f'docs/{name}.md').read_text(encoding='utf-8')
        assert '<!-- Generated from SysML' not in text
        for slug, body in re.findall(r'<!-- diagram:([\w-]+) -->(.*?)<!-- /diagram -->', text, re.S):
            generated = Path(f'docs/figures/{slug}.md').read_text(encoding='utf-8')
            diagrams = '\n\n'.join(re.findall(r'```mermaid\n.*?```', generated, re.S))
            assert body.strip() == diagrams
            count += 1
    assert count == 7

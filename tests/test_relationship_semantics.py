"""Check published native semantics and their bounded embedded views."""
from pathlib import Path
import re

import pytest

from tests.native_cases import native


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
def test_semantic_diagrams_are_small_connected_native_views(slug, kinds, rendered_site):
    locations = {
        'mission-semantics': ('architecture', 'MissionSemantics'),
        'manufacturing-semantics': ('architecture', 'ManufacturingSemantics'),
        'energy-semantics': ('energy', 'EnergySemantics'),
        'cruise-semantics': ('reliability', 'CruiseSemantics'),
        'reliability-semantics': ('reliability', 'ReliabilitySemantics'),
        'weed-semantics': ('reliability', 'WeedSemantics'),
    }
    page, view = locations[slug]
    from tools.publishing.build import blocks
    authored = Path(f'docs/{page}.md').read_text(encoding='utf-8')
    target = next(token.info.split()[1] for token in blocks(authored) if token.info.split()[1].endswith('::'+view))
    rendered = (rendered_site / f'imports/docs/{page}.md').read_text(encoding='utf-8')
    # Explanatory sketches can precede native views. Select by native provenance,
    # not by a position shared with the authored SysML-only block list.
    text = next(diagram for diagram in re.findall(r'```mermaid\n(.*?)```', rendered, re.S)
                if f'%% {target} ' in diagram)
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



def test_authored_pages_contain_views_not_copied_diagrams(rendered_site):
    from tools.publishing.build import blocks
    for name in ['architecture', 'energy', 'reliability']:
        source = Path(f'docs/{name}.md').read_text(encoding='utf-8')
        sketches = re.findall(r'```mermaid\n(.*?)```', source, re.S)
        for sketch in sketches:
            # Method illustrations may coexist with native semantics, but must
            # not copy the generated model's identities or requirement edges.
            assert 'accTitle:' in sketch and 'accDescr:' in sketch
            assert not re.search(r'BlueDog\w*::|GorgeChallenge::|[CHEMPNSRQL]-\d{3}|"(?:derive|refine|satisfy|verify)"', sketch)
        assert blocks(source)
        rendered = (rendered_site / f'imports/docs/{name}.md').read_text(encoding='utf-8')
        assert '```sysml-view' not in rendered
        assert rendered.count('```mermaid') == len(blocks(source)) + len(sketches)
        for block in blocks(source):
            assert f'%% {block.info.split()[1]} ' in rendered

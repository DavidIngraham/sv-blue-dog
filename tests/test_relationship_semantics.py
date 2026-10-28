"""Check published native semantics and their bounded embedded views."""
from pathlib import Path
import re

import pytest

from tests.native_cases import native


def test_mixed_compact_and_native_diagram_identities():
    from tools.publishing.relationships import diagram_nodes
    diagram = '''n0("`*«requirement»*\n**C-000 Challenge**`")
n1("`*«requirement»*\n**BlueDogRequirements::roundTrip : RoundTrip**`")
%% source-node n0 GorgeChallenge::transGorgeChallenge
'''
    assert diagram_nodes(diagram) == {
        'n0': 'GorgeChallenge::transGorgeChallenge',
        'n1': 'BlueDogRequirements::roundTrip',
    }


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
        ('PassageDurationCriterion', 'passageDuration'),
    ]:
        assert f'| {source} | {target} |' in refinements
        assert f'| {source} | {target} |' not in dependencies
    for source, target in [('LegProgressCriterion', 'legProgress'), ('MissionReliabilityCriterion', 'missionSuccessProbability'), ('FailureRateCriterion', 'failureRateBudget')]:
        assert f'| {source} | {target} |' in dependencies
        assert f'| {source} | {target} |' not in refinements
    # Binding numerical criteria refine; provisional study comparisons do not.
    assert 'CruiseReliability |' not in refinements
    assert 'EnergyEvidenceReadinessCriterion |' not in refinements
    assert '| recoveryPropulsion | autonomousShoreRecovery |' in dependencies
    assert '| desktopManufacture | DesignIntent |' in dependencies


@pytest.mark.parametrize('slug,kinds', [
    ('mission-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('energy-semantics', {'derive', 'refine', 'satisfy', 'verify'}),
    ('cruise-semantics', {'derive', 'satisfy', 'verify'}),
    ('reliability-semantics', {'dependency', 'satisfy', 'verify'}),
    ('manufacturing-semantics', {'satisfy', 'verify'}),
    ('weed-semantics', {'refine', 'satisfy', 'verify'}),
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
        views = [block for block in blocks(source) if block.info.startswith('sysml-view ')]
        assert '```sysml-report' not in rendered
        report_views = {
            'BlueDogFailureViews::SystemTree': 'BlueDogFailureViews::SystemTreeView',
            'BlueDogFailureViews::PrimaryTree': 'BlueDogFailureViews::PrimaryTreeView',
            'BlueDogFailureViews::ScannerTree': 'BlueDogFailureViews::ScannerTreeView',
        }
        diagrams_from_reports = [report_views[block.info.split()[1]] for block in blocks(source)
                                 if block.info.startswith('sysml-report ')
                                 and block.info.split()[1] in report_views]
        assert rendered.count('```mermaid') == len(views) + len(sketches) + len(diagrams_from_reports)
        for view in diagrams_from_reports:
            assert f'%% {view} ' in rendered
        for block in views:
            assert f'%% {block.info.split()[1]} ' in rendered


def test_requirement_context_does_not_repeat_authoritative_statements(rendered_site):
    text = (rendered_site / 'imports/docs/requirements/requirements-mission.md').read_text(encoding='utf-8')
    # The challenge remains visible in several diagrams but its full definition
    # is rendered only once, through a native query with a page-scoped name set.
    statement = '**M-001 RoundTrip** — The vessel shall sail from the Bingen departure gate'
    assert text.count(statement) == 1
    assert text.count('```mermaid') == 4


def test_construction_views_show_model_basis_and_qualification(rendered_site):
    text=(rendered_site/'imports/docs/requirements/requirements-practicality.md').read_text(encoding='utf-8')
    diagrams=re.findall(r'```mermaid\n(.*?)```',text,re.S)
    construction=next(d for d in diagrams if '%% Page_practicality_construction::thread ' in d)
    materials=next(d for d in diagrams if '%% Page_practicality_materials::thread ' in d)
    assert len(re.findall(r'^  n\d+[(\[]',construction,re.M))==4
    assert construction.count('|"dependency"|')==2
    envelope=next(d for d in diagrams if '%% Page_practicality_printEnvelope::thread ' in d)
    assert len(re.findall(r'^  n\d+[(\[]',envelope,re.M))==2
    assert envelope.count('|"refine"|')==1
    assert len(re.findall(r'^  n\d+[(\[]',materials,re.M))==17
    assert materials.count('|"derive"|')>=9
    assert materials.count('|"dependency"|')>=3
    assert 'Each print job shall fit within a 250 mm by 250 mm by 250 mm build volume.' in text
    assert 'wet-layup glass/epoxy reinforcement' in text
    assert 'Stiffness credited in structural qualification' in text

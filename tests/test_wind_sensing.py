"""Sensor configuration separation and complete mission-to-detail publication."""
from pathlib import Path
import re
import pytest
from tools.boat_analysis.model.runtime import native_value
from tools.publishing.relationships import basis_links, include_basis, diagram_nodes


def test_native_sensor_budgets(run_model):
    code, report = run_model('package WindProbe {}', '-analysis', 'BlueDog::Configurations::WindEquipment::Rollup')
    assert code == 0
    values = {v['name']: native_value(v['value']) for v in report['checks'][0]['values']}
    assert values['testbedInstalledMassKg'] == pytest.approx(.128)
    assert values['challengeInstalledMassKg'] == pytest.approx(.150)
    assert values['testbedSupplierRuntimeHours'] == 150
    assert values['challengeVesselBusW'] == pytest.approx((5*.00015+.05)*1.25/.9)
    assert values['challengeEnergyPerDayWh'] == pytest.approx(values['challengeVesselBusW']*24)
    assert values['challengeEvidenceAccepted'] is False


def test_plain_dependencies_are_not_relabelled_as_derivations():
    report = '## Plain dependency\n| trim | navigation | rationale |\n| external | navigation | rationale |'
    diagram = '```mermaid\nflowchart BT\nn1("`*«requirement»*\n**BlueDog::Requirements::trim : Trim**`")\nn2("`*«requirement»*\n**BlueDog::Requirements::navigation : Navigation**`")\n```'
    result = include_basis(diagram, basis_links(report))
    assert 'n1 -.->|"dependency"| n2' in result
    assert 'derive' not in result and 'external' not in result


def test_compact_labels_retain_native_identity():
    text = '```mermaid\nflowchart BT\nn0("`*«requirement»*\n**BlueDog::Requirements::windObservation : WindObservation**`")\n```\n\n**E-009 WindObservation** — statement'
    result = include_basis(text, [])
    assert '**E-009 Wind Observation**' in result
    assert diagram_nodes(result) == {'n0': 'BlueDog::Requirements::windObservation'}


def test_wind_thread_reaches_current_mission_root(rendered_site):
    text=(rendered_site/'imports/docs/requirements/requirements-autonomy.md').read_text()
    text=text.split('## Wind observation', 1)[1]
    diagram=re.search(r'```mermaid\n(.*?)```',text,re.S)[1]
    assert 'hawaiiVoyage' not in diagram
    for node in ['transGorgeChallenge', 'navigationAndControl',
                 'windObservation', 'windSpeedAccuracy', 'windDirectionAccuracy',
                 'windSampleCadence', 'windStaleInvalidation', 'windSensingEndurance']:
        assert node in diagram
    assert '|"dependency"|' in diagram and '|"derive"|' in diagram
    assert 'E-147 WindSpeedAccuracy' in text


def test_all_requirement_views_include_their_upstream_context(rendered_site):
    from tests.native_cases import native_graph, native
    dot=native_graph()
    nodes=dict(re.findall(r'"(n\d+)" \[.*?<b>((?:BlueDog::Mission::Challenge|BlueDog::Goals|BlueDog::Requirements)::\w+) :',dot))
    names={q.rsplit('::',1)[-1] for q in nodes.values()}
    edges={(nodes[a].rsplit('::',1)[-1],nodes[b].rsplit('::',1)[-1])
           for a,b in re.findall(r'"(n\d+)" -> "(n\d+)" \[label="(?:derive|refine)"',dot)
           if a in nodes and b in nodes}
    dependencies={(a,b) for a,b in basis_links(native('-render-document','BlueDogDocuments::RelationshipRegister')) if a in names and b in names}
    deferred_report=native('-render-document','BlueDogDocuments::FutureMissionRequirements')
    deferred={name[0].lower()+name[1:] for name in re.findall(r'^\| [A-Z]-\d+ \| (\w+) \|',deferred_report,re.M)}
    for page in (rendered_site/'imports/docs/requirements').glob('*.md'):
        for diagram in re.findall(r'```mermaid\n(.*?)```',page.read_text(),re.S):
            node_names={n:q.rsplit('::',1)[-1] for n,q in diagram_nodes(diagram).items()}
            visible=set(node_names.values())
            future_scope=bool(visible & deferred)
            assert visible, page.name
            drawn_dependencies={(node_names[a],node_names[b]) for a,b in re.findall(r'(n\d+) -\.->\|"dependency"\| (n\d+)',diagram)}
            for child,parent in edges:
                if child in visible:
                    if parent in deferred and not future_scope:
                        continue  # Shared criteria do not import a deferred mission.
                    assert parent in visible, (page.name,child,parent)
            # Focused views need not expand the complete change-impact network.
            # A plain basis is shown whenever both of its endpoints are visible.
            for child,parent in dependencies:
                if {child,parent} <= visible:
                    assert (child,parent) in drawn_dependencies, (page.name,child,parent)


def test_same_named_requirements_keep_their_native_ids():
    diagram = '''```mermaid
flowchart BT
n0("`*«requirement»*
**BlueDog::Mission::Challenge::communicationOutageAutonomy : OutageAutonomy**`")
n1("`*«requirement»*
**BlueDog::Requirements::outageAutonomy : OutageAutonomy**`")
```'''
    labels = {'BlueDog::Mission::Challenge::communicationOutageAutonomy': 'C-020',
              'BlueDog::Requirements::outageAutonomy': 'E-121',
              'OutageAutonomy': 'E-121'}
    result = include_basis(diagram, [], labels)
    assert result.count('**C-020 Outage Autonomy**') == 1
    assert result.count('**E-121 Outage Autonomy**') == 1


def test_native_common_namespace_elision_keeps_basis_edges():
    diagram = '''```mermaid
flowchart BT
n0("`*«requirement»*
**navigationRules : NavigationRules**`")
n1("`*«requirement»*
**operatorSafetyIntervention : OperatorSafetyIntervention**`")
```'''
    labels = {'BlueDog::Mission::Challenge::navigationRules': 'C-007',
              'BlueDog::Mission::Challenge::operatorSafetyIntervention': 'C-031'}
    result = include_basis(diagram, [('operatorSafetyIntervention', 'navigationRules')], labels)
    assert 'n1 -.->|"dependency"| n0' in result
    assert diagram_nodes(result)['n1'] == 'BlueDog::Mission::Challenge::operatorSafetyIntervention'

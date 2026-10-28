"""Check architecture correspondences using resolved native model/query facts.

This reports structural obligations and explicit open decisions. It does not
infer routing, behavior, physical independence or verification verdicts.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from .install import REVISION
from .runtime import ROOT, connection, model_files


def native_architecture_audit(sources=None):
    sources = tuple(sources) if sources is not None else tuple(
        (str(p), p.read_text()) for p in model_files())
    query_file = ROOT/'tools/publishing/reference.sysml'
    model = connection().parse_sources((*sources, (str(query_file), query_file.read_text())), strict=True)
    names = ('Responsibilities', 'LogicalExchanges', 'ScenarioActions', 'Mappings', 'Candidate', 'OpenDecisions')
    tables = {name: model.run_document_query('BlueDogArchitectureAudit::'+name) for name in names}
    errors = []

    def elements(scope, kind):
        return model.query(scope=[scope], select=['owner'], where={
            '@type': 'PrimitiveConstraint', 'operator': '=', 'property': '@type', 'value': [kind]})

    logical_owner = 'BlueDogLogicalArchitecture::LogicalVessel'
    implementation_owner = 'BlueDogPhysicalArchitecture::IC01Candidate'
    logical_parts = {r.id for r in elements(logical_owner, 'PartUsage') if r.get('owner') == logical_owner}
    candidate_parts = {r.id for r in elements(implementation_owner, 'PartUsage') if r.get('owner') == implementation_owner}
    candidate_flows = {r.id for r in elements(implementation_owner, 'FlowUsage') if r.get('owner') == implementation_owner}
    for row in tables['Responsibilities']:
        if row.element.id not in logical_parts:
            continue
        targets = row.cells[tables['Responsibilities'].columns.index('Implementation')]
        if not targets:
            errors.append('L02 Missing candidate allocation: '+row.element.id)
        for target in targets:
            if target.type != 'PartUsage' or target.id not in candidate_parts:
                errors.append('L03 Invalid candidate responsibility target: '+row.element.id+' -> '+target.id)
    for row in tables['LogicalExchanges']:
        targets = row.cells[tables['LogicalExchanges'].columns.index('Implementation')]
        if not targets:
            errors.append('I01 Unmapped logical exchange: '+row.element.id)
        for target in targets:
            if not ((target.type == 'FlowUsage' and target.id in candidate_flows) or
                    (target.type == 'PartUsage' and target.id in candidate_parts)):
                errors.append('I01 Invalid exchange implementation: '+row.element.id+' -> '+target.id)

    # Native owner and typing facts select steps within the scenario definitions
    # used by the package's scenario usages, rather than guessing from names.
    scenario_package = 'BlueDogMethod::Scenarios'
    action_owners = {r.id: r.get('owner') for r in elements(scenario_package, 'ActionUsage')}
    definitions = {t.id for row in tables['ScenarioActions']
                   if action_owners.get(row.element.id) == scenario_package for t in row.cells[1]}
    scenario_steps = [row for row in tables['ScenarioActions']
                      if row.element.type == 'ActionUsage' and action_owners.get(row.element.id) in definitions]
    operator = 'BlueDog::Architecture::MissionContext::operator'
    for row in scenario_steps:
        if not row.cells[0]:
            errors.append('L01 Unowned scenario action: '+row.element.id)
        for target in row.cells[0]:
            if target.id not in logical_parts and target.id != operator:
                errors.append('L01 Invalid scenario owner: '+row.element.id+' -> '+target.id)

    mapping_counts = {}
    for row in tables['Mappings']:
        scope, configurations, paths, types = row.cells
        kinds = [t.id for t in types if t.id.startswith('BlueDogArchitectureContracts::')]
        if len(kinds) != 1:
            errors.append('L03 Missing or ambiguous mapping convention: '+row.element.id)
            continue
        kind = kinds[0].rsplit('::', 1)[-1]
        mapping_counts[kind] = mapping_counts.get(kind, 0)+1
        if not scope or not any(str(v).strip() for v in scope):
            errors.append('L02 Unscoped allocation: '+row.element.id)
        if kind != 'ContextMapping':
            if [r.id for r in configurations] != ['BlueDogIC01::design']:
                errors.append('C01 Wrong or missing candidate configuration: '+row.element.id)
            if len(paths) != 1 or paths[0].id not in {
                'BlueDogArchitectureContracts::ImplementationPath::'+p for p in ('primary', 'recovery', 'shared')}:
                errors.append('L05 Missing implementation path: '+row.element.id)

    candidate = list(tables['Candidate'])
    if len(candidate) != 1 or [r.id for r in candidate[0].cells[0]] != ['BlueDogIC01::design']:
        errors.append('C01 Candidate assembly is not bound to IC-01 design')
    if len(candidate) != 1 or [r.id for r in candidate[0].cells[1]] != ['BlueDogIC01::integration']:
        errors.append('C01 Candidate assembly is not bound to IC-01 integration assumptions')

    return dict(modelHash=model.hash, runtimeRevision=REVISION,
        sourceHashes={str(Path(p).relative_to(ROOT)) if Path(p).is_relative_to(ROOT) else p:
                      hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (query_file, Path(__file__))},
        diagnostics=[str(d) for d in model.diagnostics], errors=errors,
        summary=dict(logicalResponsibilities=len(logical_parts), logicalExchanges=len(tables['LogicalExchanges'].rows),
                     scenarios=len(definitions), scenarioSteps=len(scenario_steps), mappings=mapping_counts),
        tables={name: asdict(table) for name,table in tables.items()},
        interpretation='Native ownership, endpoint coverage, mapping scope and configuration checks only. '
            'Internal mappings are implementation obligations, not executed software. Interface timing, protocol, '
            'authority arbitration, supply and independence decisions remain open; no physical qualification verdict is assigned.')


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = native_architecture_audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, default=str, indent=2)+'\n')
    print(json.dumps(dict(summary=report['summary'], diagnostics=report['diagnostics'], errors=report['errors']), indent=2))
    raise SystemExit(bool(report['errors'] or report['diagnostics']))


if __name__ == '__main__':
    main()

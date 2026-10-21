"""Native coverage and relationship audit; no second SysML parser or verdict engine."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
from tools.boat_analysis.model.install import REVISION
from tools.boat_analysis.model.runtime import ROOT, connection, model_files

GOVERNING = ('GorgeChallenge', 'BlueDog::Goals', 'BlueDogRequirements', 'BlueDogStructure')


def native_audit(sources=None):
    sources = tuple(sources) if sources is not None else tuple((str(p), p.read_text(encoding='utf-8')) for p in model_files())
    model = connection().parse_sources(sources, strict=True)
    roots = sorted({child.id for root in model.roots for child in root.children()})
    audit_file = Path(__file__).with_suffix('.sysml')
    audit = connection().parse_sources((*sources, (str(audit_file), audit_file.read_text())), strict=True)
    deferred = {row.element.id for row in audit.run_document_query('BlueDogAudit::Deferred')}
    studies = {row.element.id for row in audit.run_document_query('BlueDogAudit::StudyObjectives')}
    definitions = {row.id: row.properties for row in model.query(scope=list(GOVERNING), select=['shortName', 'name'], where={
        '@type': 'PrimitiveConstraint', 'property': '@type', 'operator': '=', 'value': ['RequirementDefinition']})}
    coverage = []
    for row in audit.run_document_query('BlueDogAudit::Coverage'):
        # WhereType includes satisfaction usages; these are assertions, not new obligations.
        if row.element.type != 'RequirementUsage':
            continue
        types = [value.id for value in row.cells[1]]
        coverage.append(dict(requirement=row.element.id, definitions=types,
            ids=[definitions[value].get('shortName', '') for value in types if value in definitions],
            applicability='future_only' if any(value in deferred for value in types) else 'current_gorge',
            classification='study_objective' if any(value in studies for value in types) else 'requirement',
            verification=[value.id for value in row.cells[2]], satisfaction=[value.id for value in row.cells[3]],
            executedByAudit=False, evidenceAcceptanceAssessed=False))
    derivations = [asdict(row) for row in audit.run_document_query('BlueDogAudit::Derivations')]
    dependencies = [asdict(row) for row in audit.run_document_query('BlueDogAudit::Dependencies', {'roots': roots})]
    refinements = {row.element.id for row in audit.run_document_query('BlueDogAudit::Refinements', {'roots': roots})}
    for row in dependencies:
        row['relationshipKind'] = 'refinement' if row['element']['id'] in refinements else 'dependency'
    errors = []
    for row in coverage:
        if row['applicability'] == 'current_gorge' and not row['verification']:
            errors.append('Missing current verification objective: ' + row['requirement'])
        if not row['definitions']:
            errors.append('Untyped governing requirement: ' + row['requirement'])
    for row in derivations:
        original, derived = row['cells'][:2]
        if len(original) != 1 or not derived:
            errors.append('Invalid derivation arity: ' + row['element']['id'])
        if any(value['type'] != 'RequirementUsage' for value in (*original, *derived)):
            errors.append('Non-requirement derivation end: ' + row['element']['id'])
        if {value['id'] for value in original} & {value['id'] for value in derived}:
            errors.append('Self-derivation: ' + row['element']['id'])
    impacts = []
    for element, relationship, direction in (
        ('GorgeChallenge::capsizeRecovery', 'derivation', 'incoming'),
        ('BlueDogRequirements::recoveryEnergy', 'verification', 'incoming'),
        ('BlueDogRequirements::capsizeQualificationRetention', 'verification', 'incoming'),
        ('BlueDogRequirements::capsizeQualificationRetention', 'satisfaction', 'incoming'),
        ('BlueDogRequirements::safeRecovery', 'satisfaction', 'incoming'),
        ('BlueDogLogicalArchitecture::LogicalVessel::supervision', 'allocation', 'outgoing'),
    ):
        rows = audit.run_document_query('BlueDogAudit::Impact', dict(element=element, relationship=relationship, direction=direction, depth=2))
        impacts.append(dict(element=element, relationship=relationship, direction=direction, depth=2, results=[row.element.id for row in rows]))
    current = [row for row in coverage if row['applicability'] == 'current_gorge']
    implementation = (audit_file, Path(__file__), Path(__file__).with_name('runtime.py'),
                      Path(__file__).with_name('install.py'), ROOT/'uv.lock')
    return dict(modelHash=model.hash, auditModelHash=audit.hash, toolRevision=REVISION,
        sourceRevision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        sourceTreeModified=bool(subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=ROOT, text=True).strip()),
        sourceHashes={str(Path(path).relative_to(ROOT)): hashlib.sha256(text.encode()).hexdigest()
            for path, text in (*sources, *((str(path), path.read_text()) for path in implementation))
            if Path(path).is_absolute() and Path(path).is_relative_to(ROOT)},
        diagnostics=[str(d) for d in model.diagnostics],
        summary=dict(requirements=len(coverage), current=len(current), future=len(coverage)-len(current),
            currentRequirements=sum(row['classification'] == 'requirement' for row in current),
            currentStudyObjectives=sum(row['classification'] == 'study_objective' for row in current),
            currentWithObjectives=sum(bool(row['verification']) for row in current),
            derivations=len(derivations), refinements=len(refinements), dependencies=len(dependencies)-len(refinements)),
        coverage=coverage, derivations=derivations, dependencies=dependencies, impactExamples=impacts, errors=errors,
        interpretation='Coverage identifies defined objectives, not executed procedures or accepted physical evidence. Future-only is applicability, not a verification verdict. Native pass/fail/inconclusive/error semantics are unchanged.')


def archive_audit():
    """Check existing immutable-run schema and detect unregistered run JSON."""
    from tools.boat_analysis.evidence.records import verify_run_sources
    result = []
    for manifest_path in sorted((ROOT/'evidence/runs').glob('*/manifest.json')):
        manifest = json.loads(manifest_path.read_text())
        if not {'files', 'sourceRevision'} <= manifest.keys():
            continue  # Aerodynamic archives use their existing separate validator.
        directory = manifest_path.parent
        registered = set(manifest['files'])
        unregistered = {p.name for p in directory.glob('*.json')} - registered - {'manifest.json'}
        if unregistered:
            raise ValueError(f'Orphaned run JSON in {directory.name}: {sorted(unregistered)}')
        manifest_sources, inputs = manifest_integrity(manifest)
        result.append(dict(manifest=str(manifest_path.relative_to(ROOT)), sourceHashesChecked=verify_run_sources(directory),
            manifestSourceHashesChecked=manifest_sources, inputArtifactsChecked=inputs, records=len(registered)))
    return result


def manifest_integrity(manifest):
    """Validate provenance recorded on the manifest instead of its run records."""
    from tools.boat_analysis.evidence.records import digest
    for path, expected in manifest.get('modelSources', {}).items():
        content = subprocess.check_output(['git', 'show', f"{manifest['sourceRevision']}:{path}"], cwd=ROOT)
        if hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise ValueError('Archived manifest source mismatch: ' + path)
    for path, expected in manifest.get('inputArtifacts', {}).items():
        # Dependency fingerprints use the existing LF-normalized digest contract;
        # registered archived record bytes are checked raw by run_record instead.
        if digest(ROOT/path) != expected:
            raise ValueError('Archived input artifact mismatch: ' + path)
    return len(manifest.get('modelSources', {})), len(manifest.get('inputArtifacts', {}))


def markdown(report):
    summary = report['summary']
    lines = ['# Native OOSEM model audit', '', report['interpretation'], '',
        f"Model hash: `{report['modelHash']}`. OpenSysML: `{report['toolRevision']}`.", '',
        f"{summary['currentWithObjectives']} of {summary['current']} current statements have verification objectives ({summary['currentRequirements']} requirements and {summary['currentStudyObjectives']} provisional study objectives); {summary['future']} have explicit future applicability.", '',
        '## Verification coverage', '', '| ID | Requirement | Applicability | Classification | Defined verification objectives |', '| --- | --- | --- | --- | --- |']
    for row in report['coverage']:
        lines.append('| ' + ' | '.join((', '.join(row['ids']), row['requirement'], row['applicability'], row['classification'], ', '.join(row['verification']) or 'None')) + ' |')
    lines += ['', '## Native impact queries', '']
    for row in report['impactExamples']:
        lines.append(f"- `{row['element']}` — {row['relationship']} {row['direction']}, depth {row['depth']}: " + ', '.join(f'`{value}`' for value in row['results']))
    lines += ['', '## Checks requiring action', ''] + (['- ' + value for value in report['errors']] or ['No missing current objective or malformed governing derivation found.'])
    lines += ['', 'The JSON companion contains every queried derivation and dependency, its native endpoints and declared rationale. Empty rationale remains visible for engineering review; this tool does not certify semantic validity from graph shape.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'build/oosem-audit.json')
    parser.add_argument('--archives', action='store_true')
    args = parser.parse_args()
    report = native_audit()
    if args.archives:
        report['archives'] = archive_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    args.output.with_suffix('.md').write_text(markdown(report))
    print(json.dumps(report['summary'], indent=2))
    if report['errors']:
        raise SystemExit('\n'.join(report['errors']))


if __name__ == '__main__':
    main()

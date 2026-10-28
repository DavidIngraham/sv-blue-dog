"""Collect native model facts for this review without modifying model inputs.

From the repository root, run:
    .venv/bin/python reviews/requirements-audit-2026-10-22/evidence/collect.py
"""
import dataclasses
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from opensysml.document import ElementRef
from tools.boat_analysis.model.install import REVISION, binary_path
from tools.boat_analysis.model.runtime import load_model, model_files

OUT = Path(__file__).resolve().parent
inputs = model_files()
model = load_model(inputs)
main_scopes = ('GorgeChallenge::', 'BlueDog::Goals::', 'BlueDogRequirements::', 'BlueDogStructure::')
definitions = model.query(where={'@type': 'PrimitiveConstraint', 'operator': '=',
                                  'property': '@type', 'value': ['RequirementDefinition']})
main_definitions = {r.id for r in definitions if r.id.startswith(main_scopes)}
packages = model.query(where={'@type': 'PrimitiveConstraint', 'operator': '=',
                             'property': '@type', 'value': ['Package']})
roots = [ElementRef(p.id) for p in packages if not p.get('owner')]
query_file = OUT / 'queries.sysml'
publishing_queries = ROOT / 'tools/publishing/reference.sysml'
query_model = load_model((*inputs, publishing_queries, query_file))
tables = {}
for name in ['Requirements', 'Conditions', 'Notes', 'RationaleRows', 'IssueRows',
             'DeferredRequirements', 'Derivations', 'RefinementLinks', 'DesignBasisLinks']:
    tables[name] = dataclasses.asdict(query_model.run_document_query('BlueDogDocuments::' + name))
for name in ['Dependencies', 'Basis', 'BasisTargets', 'Uses']:
    tables[name] = dataclasses.asdict(query_model.run_document_query('RequirementsAuditQueries::' + name))
for name in ['AllDependencies', 'AllRefinements', 'AllVerification', 'AllAllocationSources', 'AllDerivations']:
    result = query_model.run_document_query('RequirementsAuditQueries::' + name, bindings={'roots': roots})
    tables[name] = dataclasses.asdict(result)

uses = tables['Uses']
type_index = uses['columns'].index('type')
uses['rows'] = [r for r in uses['rows'] if any(t in main_definitions for t in r['cells'][type_index])]
source_files = (*inputs, publishing_queries, query_file, ROOT / 'models/README.md', ROOT / 'docs/current-assessment.md')
snapshot = {
    'baseline': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
    'runtimeRevision': REVISION,
    'runtimeVersion': subprocess.check_output([str(binary_path()), '-version'], cwd=ROOT, text=True).strip(),
    'ignoredMcp': {'version': 'develop-62b904178', 'root': 'C:/Users/davin/OneDrive/Documentos/Personal Projects/SV Bluedog/models',
                   'reason': 'Different workspace and runtime revision; not used as audit evidence.'},
    'modelDocuments': len(inputs),
    'diagnostics': [str(d) for d in model.diagnostics],
    'queryDiagnostics': [str(d) for d in query_model.diagnostics],
    'sources': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
    'otherRequirementDefinitions': [r.as_dict() for r in definitions if r.id not in main_definitions],
    'tables': tables,
}
output = OUT / 'native-review.json'
output.write_text(json.dumps(snapshot, default=str, indent=2) + '\n')
print('Saved:', output.relative_to(ROOT))
print('Model documents:', len(inputs), 'diagnostics:', len(model.diagnostics))
print('Native table rows:', {name: len(table['rows']) for name, table in tables.items()})
print('Allocation targets:', sum(len(r['cells'][0]) for r in tables['AllAllocationSources']['rows']))
print('Additional requirement definitions:', [r.id for r in definitions if r.id not in main_definitions])

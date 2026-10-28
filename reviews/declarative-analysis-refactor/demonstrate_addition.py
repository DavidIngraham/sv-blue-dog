"""Prove native configuration and typed-case extension without registry edits."""
import json
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.studies.runner import run_study

review = ROOT/'reviews/declarative-analysis-refactor'
fixture = ROOT/'tests/fixtures/declarative-studies.sysml'
addition = review/'synthetic-addition.sysml'
config = review/'synthetic-discovery.yaml'
before = run_study(config, models=(fixture,))
after = run_study(config, models=(fixture, addition))
new = 'discovered/default/AdditionalStudy::configured'
assert len(after['nativeOutputs']) == len(before['nativeOutputs']) + 1
assert after['nativeOutputs'][new]['product'] == 105
assert after['nativeOutputs'][new]['label'] == 'Added synthetic configuration'
result = dict(
    baselineCases=list(before['nativeOutputs']), extendedCases=list(after['nativeOutputs']),
    newConfiguration='AdditionalStudy::candidate', addedCase='AdditionalStudy::configured',
    outputs=after['nativeOutputs'][new], sameConfigSha256=(
        before['provenance']['configuration']['sha256'] == after['provenance']['configuration']['sha256']),
    configuration=after['provenance']['configuration'],
    sourceHashes=after['provenance']['sourceHashes'], driverHashes=after['provenance']['driverHashes'],
    runtimeRevision=after['provenance']['runtimeRevision'],
    interpretation='Synthetic interface reuse and discovery regression; no physical evidence.')
assert result['sameConfigSha256']
(review/'synthetic-addition-result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
print(json.dumps(result, indent=2))

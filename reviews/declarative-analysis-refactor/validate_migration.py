"""Reproduce migrated real analyses and compare retained numerical evidence."""
import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.studies.runner import run_study
from tools.boat_analysis.mission.demonstration import run

baseline = json.loads((ROOT/'.tools/numerical-baseline.json').read_text())
old_demo = json.loads((ROOT/'.tools/demonstration-baseline.json').read_text())
comparisons = []
for filename in ('recovery.yaml', 'sail-trade.yaml', 'recovery-scenarios.yaml'):
    report = run_study(ROOT/'examples/studies'/filename)
    (ROOT/'.tools'/('refactor-'+filename.removesuffix('.yaml')+'.json')).write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    for group in report['provenance']['groups']:
        for entry in group['runs']:
            if filename == 'recovery-scenarios.yaml':
                expected = baseline['BlueDogIntegratedCandidate::IC01RecoveryIllustration']
            else:
                expected = baseline[entry['case']]
            actual = report['nativeOutputs'][entry['key']]
            assert actual == expected, (filename, entry['key'], actual, expected)
            comparisons.append(dict(study=filename, case=entry['case'], run=entry['key'],
                                    identical=True, outputs=len(actual)))
demo = run(ROOT/'.tools/demonstration-refactor.json', ROOT/'.tools/demonstration-refactor.sysml')
for name in ('nativeOutputs', 'behaviorTraces', 'configuration', 'configurationId', 'configurationInputs'):
    assert demo[name] == old_demo[name], name
assert set(demo['nativeAnalyses']) == set(old_demo['nativeAnalyses'])
summary = dict(baseline='9c8878f', cases=comparisons,
               recoveryNominalWh=baseline['BlueDogIntegratedCandidate::IC01RecoveryIllustration']['requiredWh'],
               recoveryInvertedWh=baseline['BlueDogIntegratedCandidate::IC01InvertedRecoveryIllustration']['requiredWh'],
               buoyancyPositiveNm=baseline['BlueDogSailTrade::buoyancyIllustration']['positiveMomentNm'],
               buoyancyNegativeNm=baseline['BlueDogSailTrade::buoyancyIllustration']['negativeMomentNm'],
               demonstrationOutputsAndBehaviorIdentical=True,
               nativeRecords=str(ROOT/'.tools/demonstration-refactor.sysml'),
               interpretation='Exact software/model numerical regression; no physical validation or qualification.')
(ROOT/'.tools/numerical-comparison.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
print(json.dumps(summary, indent=2))

"""Execute the named IC-01 configuration through native recovery and supervisor cases.

These bounded examples supply hypothetical observations. They do not predict a
full voyage, certify equipment or implement a physical autopilot. Native analysis
reports and action outputs retain their own semantics; this file only orchestrates
the runs and records configuration and source provenance.
"""
import argparse
import json
from pathlib import Path
import subprocess

from ..evidence.records import source_hashes, validate
from ..model.install import REVISION
from ..model.runtime import ROOT, analysis_values, load_model, native, record_analyses
from .logic import MissionLogic


CASES = tuple('BlueDogIntegratedCandidate::'+name for name in (
    'IC01RecoveryIllustration', 'IC01InvertedRecoveryIllustration',
    'IC01NoRecoveryAuthority'))


def behavior_examples(independent_path, numerical_outputs):
    """Feed explicit observations to native actions and retain their trace."""
    safe = MissionLogic()
    safe.cycle(0)
    safe.event('capsize', 1)
    safe.capsize(1, True, False, True)
    safe.cycle(1, capsized=True, safety_confirmed=True, communications_available=False)
    safe.event('unassisted_righting', 2)
    safe.capsize(2, True, True, True)
    safe.cycle(2)

    compound = MissionLogic()
    compound.cycle(0)
    compound.event('capsize', 1)
    compound.capsize(1, True, False, True)
    compound.cycle(1, capsized=True, reserve_threatened=True,
                   safety_confirmed=True, communications_available=False)
    compound.capsize(2, True, True, True)
    compound.cycle(2)

    navigation = MissionLogic()
    navigation.cycle(0)
    navigation.cycle(1, navigation_valid=False, safety_confirmed=True)
    navigation.cycle(2, navigation_valid=False, safety_confirmed=False,
                     communications_available=False)

    recovery = {}
    for case, output in numerical_outputs.items():
        logic = MissionLogic()
        event = logic.event('power_loss', 0)
        logic.cycle(0, abort_requested=True, communications_available=False)
        permitted = logic.recovery_authority(0, 'power_loss', event['recoveryPermitted'], independent_path)
        logic.fallback(0, output['reserveFits'], permitted)
        recovery[case] = logic.trace
    return {'safeUnassistedRighting': safe.trace,
            'capsizeReserveThreatAndCommunicationLoss': compound.trace,
            'navigationDegradationThenSafetyLoss': navigation.trace,
            'recoveryFromNativeReserveScreens': recovery}


def run(output=None, records=None):
    hashes = source_hashes([
        'tools/boat_analysis/mission/demonstration.py',
        'tools/boat_analysis/mission/logic.py',
        'tools/boat_analysis/model/runtime.py',
        'tools/boat_analysis/model/install.py',
        'tools/boat_analysis/evidence/records.py', 'uv.lock'])
    model = load_model()
    allocation = analysis_values('BlueDogIntegratedCandidate::Inputs')
    numerical_outputs = {case: analysis_values(case) for case in CASES}
    reports = {case: json.loads(native('-analysis', case, '-json')) for case in CASES}
    behaviors = behavior_examples(allocation['independentRecoveryAssumed'], numerical_outputs)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=ROOT, text=True).strip())
    report = dict(configuration='BlueDogIC01::design', configurationId=allocation['identifier'],
                  configurationInputs=allocation, modelHash=model.hash,
                  sourceRevision=revision, sourceTreeModified=dirty,
                  runtimeRevision=REVISION, sourceHashes=hashes,
                  nativeAnalyses=reports, nativeOutputs=numerical_outputs, behaviorTraces=behaviors,
                  physicalQualification=False,
                  scope='Native conditional recovery arithmetic and supervisor policy with explicitly supplied hypothetical observations; no whole-course, installed hardware, righting dynamics or physical qualification claim.')
    if records is not None:
        record_analyses(CASES, records)
        report['nativeAnalysisRecords'] = str(Path(records))
    validate(hashes)
    if output is not None:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'build/analysis/ic01-demonstration.json')
    parser.add_argument('--records', type=Path, help='Also save official native AnalysisRecords as a standalone SysML snapshot')
    args = parser.parse_args()
    report = run(args.output, args.records)
    print(json.dumps({'output': str(args.output), 'configurationId': report['configurationId'],
                      'nativeOutputs': report['nativeOutputs'], 'physicalQualification': False}, indent=2))


if __name__ == '__main__':
    main()

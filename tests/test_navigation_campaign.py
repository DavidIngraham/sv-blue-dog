from collections import Counter
from tools.boat_analysis.evidence.records import ROOT, run_record, verify_run_sources

ARCHIVE=ROOT/'evidence/runs/2026-10-17-navigation-integration'


def test_navigation_replay_retains_native_provenance_and_frozen_scope():
    assert verify_run_sources(ARCHIVE)>100
    record=run_record(ARCHIVE,'navigation-integration.json')
    assert not record['resized'] and not record['completeComplianceEstablished']
    assert 'models/libraries/navigation/inland-pair.sysml' in record['sourceHashes']
    assert 'models/analyses/navigation-controller.sysml' in record['sourceHashes']
    assert len(record['runs'])==99
    assert all(row['sameOutcome'] for row in record['baselineArchiveChecks'])


def test_summary_keeps_adverse_controls_and_refusal_separate_from_steering():
    record=run_record(ARCHIVE,'navigation-integration.json')
    for mode,summary in record['summary'].items():
        rows=[r for r in record['runs'] if r['mode']==mode]
        assert summary['outcomes']==dict(Counter(r['outcome'] for r in rows))
        assert summary['nominalOutcomes']=={'qualified_completion':10,'disqualified':8}
        assert sum(r['outcome']=='safety_violation' for r in rows)==2
        if mode!='baseline':
            assert summary['changedSelections']==0
            refused=[r for r in rows if r['cause']=='navigation_obligation_unresolved_or_no_supported_candidate']
            assert refused and all(r['outcome']=='disqualified' for r in refused)

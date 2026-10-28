"""Observed facts supplied to the native integrated-candidate requirement."""
import math
from ..model.runtime import load_model


def safe(row):
    consequence=row['consequence_summary']
    return (row['outcome'] not in ('safety_violation','censored','incomplete')
            and consequence.get('termination') not in ('drift_censored','recovery_censored','shore_contact')
            and row['outside_performance_coverage_seconds']==0
            and not consequence.get('collision',False)
            and not consequence.get('clearance_violated',False)
            and not consequence.get('truthClearanceViolated',False))


def recovered(row):
    return safe(row) and row['recovery_summary']['outcome']=='recovery_approach_reached'


def assess(report):
    candidate=report['sizing'];p=candidate['allocation']
    nominal=[r for r in report['missions'] if r['case']=='clear']
    encounters=[r for r in report['missions'] if r['case']!='clear']
    rows=report['missions']+report['casualties']
    timing=[t for r in rows for t in r['timing_trace']]
    paired={(r['case'],r['seed'],r['night']) for r in report['missions'] if 'windMps' not in r}
    expected={(case,int(seed),night) for case in ('clear','non-AIS crossing','low target','weed patch') for seed in p['seeds'] for night in (False,True)}
    complete=expected<=paired and {r['windMps'] for r in nominal if 'windMps' in r}==set(candidate['inputs']['performance']['winds'])
    casualties={'sensing_loss','steering_loss','power_loss','capsize','end-exposure power_loss','end-exposure capsize'}
    refinement=report.get('refinement',[])
    refined=({r['case'] for r in refinement}=={'clear','weed patch'} and all(safe(r) and (r['outcome']=='qualified_completion' or recovered(r)) and any(base['case']==r['case'] and base['seed']==r['seed'] and base['night']==r['night'] and base['outcome']==r['outcome'] for base in report['missions']) for r in refinement))
    facts=dict(
        sizingPass=bool(candidate['replay']['profileSampledStaticScreensPass'] and all(candidate['inputs']['performance']['validWinds'])),
        nominalPass=complete and all(safe(r) and r['outcome']=='qualified_completion' for r in nominal),
        encountersPass=complete and all(safe(r) and (r['outcome']=='qualified_completion' or recovered(r)) for r in encounters),
        recoveryPass=casualties=={r['case'] for r in report['casualties']} and all(recovered(r) for r in report['casualties']),
        energyPass=bool(report['recoveryCoverage']['passed']) and all(r['minimum_energy_wh']>0 and r['energy_summary']['recoveryStoredWh']>0 for r in rows),
        timingPass=refined and bool(timing) and all(math.isclose(t['appliedSeconds']-t['selectedSeconds'],p['commandLatencySeconds'],abs_tol=1e-7) and math.isclose(t['maneuverCompleteSeconds']-t['appliedSeconds'],p['maneuverSeconds'] if t['turn'] else 0.,abs_tol=1e-7) for t in timing),
        assumptionsRecorded=bool(report['assumptions'] and report['physicalEvidenceNeeds']))
    verdict=load_model().verify_requirement('BlueDog::Analyses::IntegratedCandidate::VirtualClosure',named_arguments=facts)
    return dict(facts=facts,virtualClosure=bool(verdict.holds),physicalQualification=False,
                scope='Allocated candidate in the declared synthetic reach and static nominal Gorge passage screen; no field qualification or complete charted-course recovery coverage.')

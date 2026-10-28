# One-time authoring record. Not idempotent; do not rerun against the changed model.
from pathlib import Path
exec(Path(__file__).with_name('apply_model.py').read_text().split("REQ = 'models/vehicle/requirements.sysml'")[0])
REQ='models/vehicle/requirements.sysml';VE='models/vehicle/verification.sysml'
append(VE,'BlueDogRequirementVerification','''verification def MissionPerformanceAssessmentVerification {
        doc /* Review the declared reproducible whole-route ensemble and performance evidence for the identified configuration. Include sailing legs, holds, maneuvers and failed routes. Establish input provenance, coverage and limits independently of the provisional reliability targets; a favorable isolated passage is insufficient. */
        objective acceptance {
            verify BlueDogRequirements::legProgress;
            verify BlueDogRequirements::cruiseEvidence;
        }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
    verification def ReliabilityEvidenceVerification {
        doc /* Review the configuration-specific mission exposure, critical-function failure-rate bound, confidence method, censoring and observed failures. Assess dependence, common causes and constant-hazard applicability. Accepted rates and a study result do not establish whole-vessel reliability without this argument. */
        objective acceptance { verify BlueDogRequirements::reliabilityEvidence; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
''','Retain direct planned verification of binding performance and reliability evidence obligations')

# Contexts follow the explicitly maintained acceptance family manifest and the
# audit's native requirement inventory; shared event links never supply scope.
leaves=json.loads((ROOT/'tests/atomic_requirements.json').read_text())['leaves']
audit=list(csv.DictReader((HERE.parent/'requirements-audit-2026-10-22/requirement-review.csv').open()))
byname={r['element'].rsplit('::',1)[-1]:r for r in audit}
byusage={r['element'].rsplit('::',1)[-1][0].lower()+r['element'].rsplit('::',1)[-1][1:]:r for r in audit}
contexts=[]
for leaf in leaves:
    record=byname[leaf['name']]
    if record['conditions']:continue
    parent=byusage[leaf['parent']]
    contexts.append((record['element'],f" Apply the {parent['id']} qualification conditions for this criterion. Explicit mode coverage and independent shared obligations stated in {leaf['id']} continue to govern. "))
edit(REQ,lambda e:[e.add_comment(target,body,name='conditions') for target,body in contexts],f'Make qualification-context references explicit on {len(contexts)} flat acceptance leaves')

sources=snapshot(REQ);texts=dict(sources);name=str(ROOT/REQ)
changes=[
('All leaves apply to every release.','N-118 RightingDeadline, N-119 CapsizeRigRetention, N-120 CapsizeBallastRetention and N-121 CapsizeElectronicsSealing apply to every release.'),
('Both leaf criteria apply to every repetition;','N-128 WeedSnagSpeedRecovery and N-129 WeedSnagSteeringRecovery apply to every repetition;'),
('        comment aggregateMembers /*\n         *  N-051 incorporates N-118 RightingDeadline, N-119 CapsizeRigRetention, N-120 CapsizeBallastRetention and N-121 CapsizeElectronicsSealing for every declared release. */\n',''),
('        comment aggregateMembers /*\n         *  N-054 incorporates N-128 WeedSnagSpeedRecovery and N-129 WeedSnagSteeringRecovery for every declared repetition. */\n',''),
]
for old,new in changes:
    assert texts[name].count(old)==1,old
    texts[name]=texts[name].replace(old,new,1)
# Restore the native owner's indentation after declaration replacements.
texts[name]=texts[name].replace('\n#refinement dependency','\n    #refinement dependency').replace('\ndependency sharedAcceptance','\n    dependency sharedAcceptance').replace('\ndependency energyDerivation','\n    dependency energyDerivation')
for child in ['N-053','N-054','N-055','N-056']:
    texts[name]=texts[name].replace(child+' specifies a detailed acceptance condition for N-003',child+' specifies a detailed acceptance condition for N-004')
commit(tuple((n,texts[n]) for n,_ in sources),'Put stable aggregate membership in normative conditions and align vegetation rationale')
(HERE/'context-steps.json').write_text(json.dumps(LOG,indent=2)+'\n')

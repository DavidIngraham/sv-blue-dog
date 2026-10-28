# One-time authoring record. Not idempotent; do not rerun against the changed model.
"""Process responsibilities, scoped evidence objectives and decision closure records."""
from pathlib import Path
exec(Path(__file__).with_name('apply_model.py').read_text().split("REQ = 'models/vehicle/requirements.sysml'")[0])

def literals(file, changes, label):
    sources = snapshot(file)
    texts = dict(sources)
    name = str(ROOT/file)
    for old, new in changes:
        assert texts[name].count(old) == 1, old[:100]
        texts[name] = texts[name].replace(old,new,1)
    commit(tuple((n,texts[n]) for n,_ in sources),label)

MISSION='models/missions/transgorge.sysml'
governing = 'Before entry approval, the entrant shall submit a rule-applicability assessment for the identified vessel, propulsion modes, course and operating conditions. Identify the governing provisions and current local restrictions, required lights/shapes/sound signals, applicable exceptions and supporting authority. The organizer shall record the reviewed rule and notice baseline; later effective changes shall be reviewed before launch.'
entry = 'Entry approval shall require organizer acceptance of configuration-specific evidence covering relevant sailing, overtaking, crossing and constrained-water encounters, uncertain classification, restricted visibility, degraded sensing and safety intervention. Record assumptions, observation and maneuver limits, pass/fail criteria, physical demonstrations, simulation coverage and remaining exclusions. Unsupported conditions shall be excluded from admission; unresolved capability within admitted conditions prevents entry approval. Entrants shall justify detection distances, margins and maneuver capability. Passing a limited software rule subset does not establish compliance with C-007.'
adjudication = 'A collision, established navigation-rule breach or unsafe conduct requiring safety intervention disqualifies the attempt. Safety action shall not be delayed to preserve qualification, and the operator shall intervene when necessary if autonomous action is insufficient and intervention is available. Operator intervention or motor propulsion ends qualification under C-003/C-004 even when it prevents a violation. A compliant autonomous avoidance maneuver does not by itself end qualification. The organizer shall adjudicate using retained observations, commands, motion history and independent evidence where available, with a recorded reason. Insufficient evidence leaves qualification unconfirmed; absence of collision alone is not proof of compliance. Entry approval does not waive ongoing obligations.'
policies = [
('C-028','NavigationRuleApplicability','navigationRuleApplicability','Before entry approval, the entrant shall submit a configuration-specific navigation-rule applicability assessment.', governing.split(' The organizer')[0]),
('C-029','NavigationRuleBaseline','navigationRuleBaseline','The organizer shall record and maintain the reviewed rule and notice baseline for the attempt.', 'The organizer'+governing.split('The organizer')[1]),
('C-030','NavigationEntryEvidence','navigationEntryEvidence','The organizer shall approve entry only when the configuration-specific navigation evidence satisfies the entry-evidence conditions.', entry),
('C-031','OperatorSafetyIntervention','operatorSafetyIntervention','The operator shall intervene when necessary if autonomous safety action is insufficient and intervention is available.', 'Safety action shall not be delayed to preserve qualification. Operator intervention or motor propulsion ends qualification under C-003/C-004 even when it prevents a violation.'),
('C-032','NavigationAdjudication','navigationAdjudication','The organizer shall record the attempt qualification decision and its supporting reason against the navigation adjudication conditions.', adjudication),
]
notation=''
for rid,name,usage,statement,conditions in policies:
    notation+=f'''requirement def <'{rid}'> {name} {{
        doc /* {statement} */
        comment conditions /* {conditions} */
        metadata workStatus : ModelingMetadata::StatusInfo {{ status = ModelingMetadata::StatusKind::open; }}
    }}
    requirement {usage} : {name};
    dependency {usage}Basis from {usage} to navigationRules;
    '''
append(MISSION,'GorgeChallenge',notation,'Identify five existing navigation process and policy obligations as C-028 through C-032')
literals(MISSION, [
('comment governingBaseline /* '+governing+'*/','comment processResponsibilities /* C-028 identifies entrant applicability review; C-029 controls the organizer rule and notice baseline; C-030 governs entry evidence; C-031 identifies operator safety intervention; C-032 governs adjudication. These preserve the C-007 entry and qualification policy. */'),
('        comment entryEvidence /* '+entry+'*/\n',''),
('        comment adjudication /* '+adjudication+'*/\n',''),
('comment conditions /* Monitoring-link loss shall not interrupt autonomous mission execution. Retained telemetry shall be transmitted after contact returns. */','comment conditions /* C-020 governs autonomous continuation, retention and telemetry replay during monitoring-link outages. */'),
], 'Relocate process policy intact and reference the single C-020 outage obligation')
edit('models/missions/verification.sysml',lambda e:[e.add_verify('GorgeChallengeVerification::NavigationRulesEntryAndAdjudicationVerification::acceptance','GorgeChallenge::'+p[2]) for p in policies], 'Attach navigation process requirements to the existing entry/adjudication review')

# Correct candidate satisfaction scope. The model supplies the package span;
# exact authored clauses are guarded rather than interpreted by a text parser.
ALLOC='models/vehicle/allocations.sysml'
literals(ALLOC,[
('Design satisfaction allocations, not verification evidence. Physical','Candidate design satisfaction assertions, not verification evidence. Physical'),
('satisfy BlueDogRequirements::serviceability by missionContext.boat.hullAndRig.enclosure;','satisfy BlueDogRequirements::serviceability by missionContext.boat;'),
('satisfy BlueDogRequirements::wetElectricalIntegrity by BlueDogLogicalArchitecture::vessel.communications;','satisfy BlueDogRequirements::wetElectricalIntegrity by missionContext.boat;'),
('// Proposed allocations of atomic acceptance leaves; not verification evidence.','// Candidate satisfaction assertions for acceptance leaves; evidence remains open.'),
], 'Scope whole-vessel serviceability and wet wiring claims to the whole candidate')
edit(ALLOC,lambda e:e.add_satisfy('BlueDogSatisfaction','BlueDogRequirements::vegetationResilience',by='missionContext.boat'), 'Add the explicit vegetation candidate assertion')
append('models/vehicle/use-cases.sysml','BlueDogUseCases', 'dependency poweredRecoveryBasis from recover to BlueDogRequirements::recoveryPropulsion;', 'Reference the separate R-001 capability from the recovery scenario')

REL='models/analyses/reliability.sysml'
literals(REL,[(line+'\n','') for line in [
'            verify BlueDogRequirements::reliabilityEvidence;',
'            verify BlueDogRequirements::legProgress;',
'            verify BlueDogRequirements::passageDuration;',
'            verify BlueDogRequirements::cruiseEvidence;',
]], 'Restrict the aggregate reliability verdict to the two provisional study objectives')
edit(REL,lambda e:e.add_documentation('BlueDogReliability::VoyageReliabilityVerification',' Study assessment of provisional L-101 and L-102 only. A failed numerical study target does not fail a binding product or evidence-process requirement. L-103, Q-101 and Q-103 retain their independent planned review objectives. '), 'Document the provisional verdict scope')
append(REL,'BlueDogReliability','''verification def PassageDurationVerification {
        doc /* Evaluate Q-102 independently of the provisional reliability target and demonstration duration. This checks the supplied profile only; whole-route ensemble completeness and installed qualification evidence remain separate review objectives. */
        subject profile : VoyageProfile;
        attribute profileValid : Boolean = SequenceFunctions::size(profile.legs) > 0 and
            profile.legs->ControlFunctions::forAll { in leg : SailingLeg; leg.valid } and
            profile.holdTime >= 0 [s] and profile.qualifiedDuration > 0 [s];
        attribute durationMet : Boolean = BlueDogRequirements::PassageDurationCriterion(profile.voyageDuration, profile.qualifiedDuration);
        objective durationAcceptance {
            verify BlueDogRequirements::passageDuration;
            require constraint { profileValid and durationMet }
        }
        return verdict : VerificationCases::VerdictKind =
            if not profile.profileEvidenceAccepted ? VerificationCases::VerdictKind::inconclusive
            else VerificationCases::PassIf(profileValid and durationMet);
    }
''', 'Add a conditional Q-102 duration verdict independent of provisional reliability criteria')

BASIS='models/vehicle/requirement-basis.sysml'
append(BASIS,'BlueDogRequirementBasis','''metadata def ProcessObligation {
        attribute responsibleRole : String;
        attribute output : String;
        attribute acceptance : String;
    }
    metadata def AllocationDecision {
        attribute source : String;
        attribute applicability : String;
        attribute valueJustification : String;
        attribute marginBasis : String;
        attribute evidenceNeeded : String;
        attribute owner : String;
        attribute closureAction : String;
        attribute accepted : Boolean;
    }
''', 'Define process responsibility and allocation-decision records')
processes={
'RegulatoryClassification':('Project owner','Deployment compliance assessment','Configuration-specific applicable navigation, radio and authorization evidence reviewed before deployment.'),
'DeploymentComplianceRecord':('Project owner','Deployment compliance record','Identify the governing matrix, evidence, authority and unresolved exclusions.'),
'DeploymentReleaseGate':('Project owner','Deployment release decision','Reject unresolved applicable compliance obligations.'),
'LegProgress':('Project owner, mission assessment','Reproducible whole-route scenario assessment','Include sailing legs, holds, maneuvers and failed routes; no fixed speed floor.'),
'CruiseEvidence':('Project owner, mission assessment','Configuration-specific mission performance evidence','Review route ensemble coverage and installed validity; calculations alone do not accept evidence.'),
'ReliabilityEvidence':('Project owner, reliability assessment','Reliability evidence argument','Review mission-critical functions, exposure, rates, dependence and evidence applicability independently of provisional targets.'),
'CriticalFailureDisposition':('Project owner, safety assessment','Failure dispositions','Resolve applicable critical failure and common-cause actions before release.'),
'EnergyEvidenceReadiness':('Project owner, energy assessment','Energy-case acceptance record','Identify accepted installed loads, resource bounds, battery derating and interval resolution evidence.'),
}
notation=''
for target,(owner,output,acceptance) in processes.items():
    notation+=f'''metadata process{target} : ProcessObligation about BlueDogRequirements::{target} {{
        responsibleRole = {json.dumps(owner)}; output = {json.dumps(output)}; acceptance = {json.dumps(acceptance)};
    }}
    '''
for rid,name,usage,statement,conditions in policies:
    owner='Entrant' if rid=='C-028' else 'Operator' if rid=='C-031' else 'Organizer'
    notation+=f'''metadata process{name} : ProcessObligation about GorgeChallenge::{name} {{
        responsibleRole = "{owner}"; output = "{name} record for the identified configuration and attempt"; acceptance = "Review the requirement conditions using the entry/adjudication verification case; no accepted evidence is implied by this role assignment.";
    }}
    '''
append(BASIS,'BlueDogRequirementBasis',notation,'Assign responsibility and reviewable outputs to assessment, release and navigation process obligations')
(HERE/'process-steps.json').write_text(json.dumps(LOG,indent=2)+'\n')

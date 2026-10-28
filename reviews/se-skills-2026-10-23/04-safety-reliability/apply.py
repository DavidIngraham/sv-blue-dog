import json
from tools.boat_analysis.model.runtime import ROOT,connection,model_files
sources={p:p.read_text() for p in model_files()}
fmea=ROOT/'models/analyses/dfmea.sysml'
reliability=ROOT/'models/analyses/reliability.sysml'
safety=ROOT/'models/analyses/safety.sysml'
new_modes=[
 ('recoveryCaptureFault','FM-013','hullAndRig.handling','Retain and retrieve the vessel safely',
  'Recovery approach cannot be captured or retained','Unsuitable shore geometry, waves or incompatible handling interface',
  'Vessel escapes or requires an unsafe manual reach','Operator exposure and loss of recoverable vessel',
  'Surveyed approach and independent capture/retention observation; unverified',
  'Test approach, capture, retention and one-person pickup under admitted conditions','Owner/handling',
  'BlueDogRequirements::soloRetrieval'),
 ('commandContextFault','FM-014','control.missionManager','Apply only current authorized actuation',
  'Stale, replayed or mismatched permission/command is accepted','Clock, restart, configuration or authority disagreement',
  'Actuation bypasses current restrictions','Unintended motion, contact hazard or disqualification',
  'Consumer context/ordering/inhibit checks; implementation unverified',
  'Fault inject expiry, replay, restart and missing durable acknowledgment at physical enable boundary','Autonomy/recovery',
  'BlueDogRequirements::commandIntegrity'),
 ('commonSensingFault','FM-015','navigation.traffic','Preserve required observation across primary failure',
  'Primary and recovery observations share an undetected failure','Common visibility, clock, configuration, software or installation dependence',
  'Both paths supply absent or plausible incorrect observations','Required lookout/navigation unavailable during sailing or recovery',
  'Independent references and mode-specific coverage evidence; unresolved',
  'Assess shared dependencies and inject correlated sensing/context failures in upright and inverted modes','Sensing/system safety',
  'BlueDogRequirements::trafficSafety')]
blocks=[]
links=[]
for name,identifier,affected,function,mode,cause,local,effect,detection,action,owner,criterion in new_modes:
    lines=[f'        part {name} : ReviewRow subsets modes {{',
        f'            ref part :>> affected = BlueDog::Architecture::missionContext.boat.{affected};',
        f'            attribute :>> identifier = {json.dumps(identifier)};',
        f'            attribute :>> intendedFunction = {json.dumps(function)};']
    for field,value in [('failureMode',mode),('cause',cause),('localEffect',local),('missionEffect',effect)]:
        lines += [f'            occurrence {field}Event : FailureAnalysis::Event {{ attribute :>> description = {json.dumps(value)}; }}',
                  f'            ref occurrence :>> {field} = {field}Event;']
    lines += [f'            attribute :>> proposedDetection = {json.dumps(detection)};',
              f'            attribute :>> recommendedAction = {json.dumps(action)};',
              f'            attribute :>> ownerRole = {json.dumps(owner)};',
              '            attribute :>> safetyCritical = true;',
              '            metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }',
              '            metadata risk : RiskMetadata::Risk;', '        }']
    blocks.append('\n'.join(lines))
    links.append(f'    dependency {name}Criterion from starter::{name} to {criterion};')
    for source,target in [('cause','failureMode'),('failureMode','localEffect'),('localEffect','missionEffect')]:
        links.append(f'    connection {name}_{source}_{target} : CauseAndEffect::Causation connect starter.{name}.{source} to starter.{name}.{target};')
marker='    }\n    dependency hullLeakDesign'
assert sources[fmea].count(marker)==1
sources[fmea]=sources[fmea].replace(marker,'\n'.join(blocks)+'\n    }\n    dependency hullLeakDesign',1)
sources[fmea]=sources[fmea].rstrip()[:-1]+'\n'+'\n'.join(links)+'\n}\n'
old='        attribute constantHazardAccepted : Boolean;'
assert sources[reliability].count(old)==1
sources[reliability]=sources[reliability].replace(old,old+'''
        attribute criticalFunctionPartitionAccepted : Boolean default = false;
        attribute dependenceTreatmentAccepted : Boolean default = false;
        attribute commonCauseCoverageAccepted : Boolean default = false;
        comment rateBasis /* Review assertions, not measured rates or proof of independence.
         * Establish non-overlapping critical-function loss terms, dependence treatment
         * and common-cause coverage for this configuration/profile before crediting
         * the study evidence. A primary component fault need not be function loss.
         * NIST Handbook 8.1.8 and defense R&M BoK 2025 section 3.2.4 inform this basis. */''')
old='out attribute evidenceReady : Boolean = profile.profileEvidenceAccepted and profile.rateEvidenceAccepted and profile.constantHazardAccepted;'
assert sources[reliability].count(old)==1
sources[reliability]=sources[reliability].replace(old,'''out attribute evidenceReady : Boolean = profile.profileEvidenceAccepted and profile.rateEvidenceAccepted and profile.constantHazardAccepted
            and profile.criticalFunctionPartitionAccepted and profile.dependenceTreatmentAccepted and profile.commonCauseCoverageAccepted;''')

hazards=[
 ('collisionExposure','HAZ-01','Unsafe motion or clearance in the presence of people, craft or their equipment',
  'Collision, strike or entanglement affecting other waterway users',
  'Sailing, holds, degraded operation and powered/unpowered recovery',
  'Safety/navigation','Admit only supported sensing/maneuver conditions; preserve lookout/avoidance and assess the independent recovery path. Controls and secondary effects need evidence.',
  ('steeringJam','sailJam','powerCommonCause','navigationFault','controlLockup','trafficMiss','commonSensingFault'),
  ('BlueDogRequirements::trafficSafety','BlueDogRequirements::navigationAvailability'),
  ('BlueDogRequirementVerification::TrafficSafetyVerification','GorgeChallengeVerification::WindSportEncounterVerification')),
 ('boundaryLoss','HAZ-02','Required navigation or control cannot retain the approved water envelope',
  'Grounding or hazardous interaction with excluded waterway structures and traffic',
  'Sailing, waiting, degraded navigation and recovery','Navigation/recovery',
  'Validate the permitted domain and uncertainty; retain current observations, boundary supervision and a supported recovery response. A planner result alone is insufficient.',
  ('steeringJam','powerCommonCause','navigationFault','controlLockup','commonSensingFault'),
  ('BlueDogRequirements::operatingBoundary','GorgeChallenge::restrictedWaters'),
  ('BlueDogRequirementVerification::OperatingBoundaryVerification','GorgeChallengeVerification::RestrictedWatersVerification')),
 ('unintendedThrust','HAZ-03','Motor thrust is enabled without current safe authority or during human handling',
  'Propeller/contact or entanglement exposure; unwanted propulsion also ends qualification',
  'Launch, qualifying attempt, restart, recovery, capture and service','Recovery/handling',
  'Establish current authority, known nonqualifying state, durable disqualification and effective isolation. Driver faults and handling exposure require physical controls and trials.',
  ('motorUncommanded','controlLockup','commandContextFault'),
  ('BlueDogRequirements::challengeMotorInhibition','BlueDogRequirements::motorIsolationDeadline','BlueDogRequirements::qualificationPersistence'),
  ('BlueDogVerificationPlanning::InterfaceAndDurabilityIntegrationVerification','BlueDogRequirementVerification::EmergencyControlVerification')),
 ('flotationRetentionLoss','HAZ-04','Casualty load or ingress defeats flotation or major-component retention',
  'Vessel loss or released components/debris affecting people, property or the environment',
  'Loaded operation, capsize, flooding, recovery and retrieval','Hull/structure',
  'Establish configuration-specific flotation, load paths and retention under casualty exposure; assess hazards introduced by retention choices. Static intact volume alone is insufficient.',
  ('hullLeak','keelLoss','sailJam'),
  ('GorgeChallenge::casualtyFlotation','GorgeChallenge::majorComponentRetention','BlueDogStructure::structuralIntegrity'),
  ('BlueDogRequirementVerification::FlotationEvidence','GorgeChallengeVerification::MajorComponentRetentionVerification')),
 ('electricalThermalExposure','HAZ-05','Water, faults, charging or temperature compromise energy containment and required electrical function',
  'Thermal/electrical/material exposure to people or vessel and loss of required functions',
  'Charging, bench testing, operation, casualty recovery and service','Power/system safety',
  'Evaluate design/containment/protection alternatives, ingress and thermal limits, supply transients and safe service isolation using the selected installation. No component or protection scheme is selected by this record.',
  ('batteryFault','hullLeak','powerCommonCause'),
  ('BlueDogRequirements::wetElectricalIntegrity','BlueDogRequirements::peakSupplyCapability','BlueDogRequirements::batteryChargeTemperatureInhibition'),
  ('BlueDogRequirementVerification::WetElectricalIntegrityVerification','BlueDogRequirementVerification::PeakSupplyCapabilityVerification','BlueDogRequirementVerification::SolarHeatingVerification')),
 ('handlingRetrievalExposure','HAZ-06','Approach, capture, retention or lifting cannot be completed with the admitted site and handling arrangement',
  'Operator fall/contact/exposure or vessel escape during attempted retrieval',
  'Transport, launch, shore capture, pickup and maintenance handling','Owner/handling',
  'Review site access and handling design before relying on procedures; validate the full one-person task and retained vessel rather than approach alone. Preserve failed/incomplete trials.',
  ('recoveryCaptureFault','steeringJam'),
  ('BlueDogRequirements::soloRetrieval','BlueDogRequirements::transportability','BlueDogStructure::launchClearance'),
  ('BlueDogVerificationPlanning::HumanRecoveryUseValidation','BlueDogRequirementVerification::LaunchSiteEvidence','BlueDogRequirementVerification::TransportabilityVerification'))]
head='''package BlueDogSafety {
    private import ScalarValues::*;
    doc /* Initial current-Gorge hazard/control argument, not complete coverage or
     * accepted risk. MIL-STD-882E Change1 sections 4.3 and Task106, NASA SE
     * Handbook6.4 and defense R&M BoK2025 inform the structure. Project scales
     * and acceptance responsibilities remain to be established; no DoD matrix
     * or authority is adopted. Proposed controls have no credited effectiveness. */
    part def HazardRecord {
        attribute identifier : String;
        ref part configuration : MarineDesign::Design = BlueDogIC01::design;
        ref part contributors : FailureAnalysis::ReviewRow [1..*];
        attribute condition : String;
        attribute potentialMishap : String;
        attribute modes : String;
        attribute ownerRole : String;
        attribute controlIntent : String;
        attribute implementationEvidenceAccepted : Boolean default = false;
        attribute effectivenessEvidenceAccepted : Boolean default = false;
        attribute residualRiskAssessmentAccepted : Boolean default = false;
        attribute riskDispositionAccepted : Boolean default = false;
        attribute controlEvidenceRecord : String [0..1];
        attribute acceptanceRecord : String [0..1];
        attribute acceptanceAuthority : String [0..1];
        attribute recordsIdentified : Boolean = SequenceFunctions::size(controlEvidenceRecord) == 1 and
            SequenceFunctions::size(acceptanceRecord) == 1 and SequenceFunctions::size(acceptanceAuthority) == 1 and
            controlEvidenceRecord->ControlFunctions::forAll { in value : String; value != "" } and
            acceptanceRecord->ControlFunctions::forAll { in value : String; value != "" } and
            acceptanceAuthority->ControlFunctions::forAll { in value : String; value != "" };
        attribute closed : Boolean = implementationEvidenceAccepted and effectivenessEvidenceAccepted and
            residualRiskAssessmentAccepted and riskDispositionAccepted and recordsIdentified;
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        metadata risk : RiskMetadata::Risk;
        doc /* Closed is a modeled review precondition over supplied dispositions
         * and record identities. It does not inspect records or accept risk.
         * Existing RiskMetadata levels are unassessed, not a numerical hazard
         * matrix or a zero/low risk assertion. Contributor links describe credible
         * mechanisms, not probabilities or inevitable mishaps. */
    }
    part def HazardSet {
        ref part failureReview : FailureAnalysis::Review;
        part hazards : HazardRecord [1..*];
        attribute scopeReviewed : Boolean default = false;
    }
    part gorge : HazardSet {
        ref part :>> failureReview = BlueDogDFMEA::starter;
'''
body=[]
links=[]
for name,identifier,condition,mishap,modes,owner,intent,contributors,controls,verifications in hazards:
    lines=[f'        part {name} : HazardRecord subsets hazards {{']
    for field,value in [('identifier',identifier),('condition',condition),('potentialMishap',mishap),('modes',modes),('ownerRole',owner),('controlIntent',intent)]:
        lines.append(f'            attribute :>> {field} = {json.dumps(value)};')
    lines += ['            ref part :>> contributors = ('+', '.join('BlueDogDFMEA::starter.'+c for c in contributors)+');','        }']
    body.append('\n'.join(lines))
    for index,target in enumerate(controls):links.append(f'    dependency {name}Control{index+1} from gorge::{name} to {target};')
    for index,target in enumerate(verifications):links.append(f'    dependency {name}Verification{index+1} from gorge::{name} to {target};')
tail='''    }
    analysis def SafetyReview {
        subject assessment : HazardSet;
        analysis failureModes : FailureAnalysis::DesignFailureReview { subject = assessment.failureReview; }
        out attribute hazardCount : Integer = SequenceFunctions::size(assessment.hazards);
        out attribute unresolvedHazardCount : Integer = NumericalFunctions::sum(
            assessment.hazards->ControlFunctions::collect { in hazard : HazardRecord; if hazard.closed ? 0 else 1 });
        out attribute hazardRecordsClosed : Boolean = hazardCount > 0 and
            assessment.hazards->ControlFunctions::forAll { in hazard : HazardRecord; hazard.closed };
        out attribute fmeaReady : Boolean = failureModes.reviewReady;
        out attribute reviewReady : Boolean = assessment.scopeReviewed and fmeaReady and hazardRecordsClosed;
        return ready : Boolean = reviewReady;
        doc /* Uses the native FMEA review and explicit hazard dispositions.
         * A successful calculation is not safety qualification or risk acceptance. */
    }
    analysis currentReview : SafetyReview { subject = gorge; }
    dependency dispositionBasis from SafetyReview to BlueDogRequirements::criticalFailureDisposition;
    metadata issue : ModelingMetadata::Issue {
        text = "S-01: Complete lifecycle/mode/human/environment hazard coverage, including manufacturing materials, storage, charging and disposal; the initial six hazards are not exhaustive. S-02: Establish likelihood/consequence/uncertainty and project risk criteria without treating unknown as low. S-03: Select and verify controls, secondary effects and common-cause isolation on the installed configuration. S-04: Record actual effectiveness evidence and residual-risk dispositions with the responsible authority; all current hazard and failure actions remain open. S-05: Justify non-overlapping critical-function rate terms, dependence/common-cause treatment and exposure/statistical applicability before crediting reliability evidence.";
    }
'''
sources[safety]=head+'\n'.join(body)+'\n'+tail+'\n'.join(links)+'\n}\n'
candidate=connection().parse_sources(tuple((str(p),t) for p,t in sources.items()),strict=True)
assert not candidate.diagnostics,candidate.diagnostics
for path in (fmea,reliability,safety):path.write_text(sources[path])
print('Native candidate accepted: three failure mechanisms, six scoped hazards, combined safety review and reliability-basis gates.')


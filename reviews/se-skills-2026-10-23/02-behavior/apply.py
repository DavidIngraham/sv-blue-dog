from tools.boat_analysis.model.runtime import ROOT,connection,model_files
sources={p:p.read_text() for p in model_files()}
method=ROOT/'models/vehicle/method.sysml'
behavior=ROOT/'models/vehicle/behavior-contracts.sysml'

def replace(old,new):
    assert sources[method].count(old)==1,old[:120]
    sources[method]=sources[method].replace(old,new)

replace('''        action def SelectSailingCommand {
            in wind : WindEstimate;''','''        action def SelectSailingCommand {
            in wind : WindEstimate;
            in navigation : BlueDogLogicalArchitecture::NavigationEstimate;
            in permission : BlueDogLogicalArchitecture::OperationPermission;''')
replace('''        action def ApplySailingCommand {
            in command : SailingCommand;''','''        action def ApplySailingCommand {
            in command : SailingCommand;
            in permission : BlueDogLogicalArchitecture::OperationPermission;''')
replace('''        #logicalScenario action def NormalSailing {
''','''        #logicalScenario action def NormalSailing {
            in navigation : BlueDogLogicalArchitecture::NavigationEstimate;
            in permission : BlueDogLogicalArchitecture::OperationPermission;
''')
replace('''            flow observe.wind to select.wind;
            flow select.command to actuate.command;''','''            flow observe.wind to select.wind;
            bind select.navigation = navigation;
            bind select.permission = permission;
            bind actuate.permission = permission;
            flow select.command to actuate.command;''')
replace('''        action def SelectAvoidanceManeuver {
            in assessment : BlueDogLogicalArchitecture::TrafficAssessment;''','''        action def SelectAvoidanceManeuver {
            in assessment : BlueDogLogicalArchitecture::TrafficAssessment;
            in navigation : BlueDogLogicalArchitecture::NavigationEstimate;
            in permission : BlueDogLogicalArchitecture::OperationPermission;''')
replace('''        action def ExecuteAndReassess {
            in command : SailingCommand;''','''        action def ExecuteAndReassess {
            in command : SailingCommand;
            in permission : BlueDogLogicalArchitecture::OperationPermission;''')
replace('''        #logicalScenario action def TrafficEncounter {
''','''        #logicalScenario action def TrafficEncounter {
            in permission : BlueDogLogicalArchitecture::OperationPermission;
''')
replace('''            flow assess.assessment to select.assessment;
            flow select.command to execute.command;''','''            flow assess.assessment to select.assessment;
            flow navigate.navigation to select.navigation;
            bind select.permission = permission;
            bind execute.permission = permission;
            flow select.command to execute.command;''')
replace('''        action def ApplyRecoveryCommand {
            in command : BlueDogLogicalArchitecture::RecoveryCommand;
        }''','''        action def PersistRecoveryAuthorization {
            in record : BlueDogLogicalArchitecture::MissionRecord;
            out authorizationStored : ScalarValues::Boolean;
            doc /* Confirm durable disqualification storage before motor enable.
             * Failure or unknown acknowledgment cannot authorize propulsion.
             * This descriptive step does not implement storage hardware. */
        }
        action def ApplyRecoveryCommand {
            in command : BlueDogLogicalArchitecture::RecoveryCommand;
            in permission : BlueDogLogicalArchitecture::OperationPermission;
            in authorizationStored : ScalarValues::Boolean;
            out record : BlueDogLogicalArchitecture::MissionRecord;
            doc /* Check current authority, command applicability, qualification,
             * durable state and interlocks before enable. Record the observed
             * execution disposition; acceptance does not establish shore arrival. */
        }''')
replace('''            then action recover : RecoverAndReassess;
            then action actuate : ApplyRecoveryCommand;''','''            then action recover : RecoverAndReassess;
            then action persist : PersistRecoveryAuthorization;
            then action actuate : ApplyRecoveryCommand;''')
replace('''            flow recover.command to actuate.command;
            flow recover.record to record.record;''','''            flow recover.command to actuate.command;
            flow recover.record to persist.record;
            flow persist.authorizationStored to actuate.authorizationStored;
            flow abort.permission to actuate.permission;
            flow actuate.record to record.record;''')
replace('''        action def ValidateNavigation {
            in observation : BlueDogLogicalArchitecture::NavigationEstimate;
            out current : BlueDogLogicalArchitecture::NavigationEstimate;
            doc /* Mark stale or invalid observations unusable. Backup safety
             * confirmation is a separate observation, not inferred from this flag. */''','''        action def ValidateNavigation {
            in observation : BlueDogLogicalArchitecture::NavigationEstimate;
            out current : BlueDogLogicalArchitecture::NavigationEstimate;
            out usable : ScalarValues::Boolean;
            doc /* Preserve the producer assertion and report consumer usability
             * separately using the allocated age/context criteria. Backup safety
             * confirmation is a separate observation, not inferred from this flag. */''')
replace('''        action def SelectNavigationGuidance {
            in navigation : BlueDogLogicalArchitecture::NavigationEstimate;''','''        action def SelectNavigationGuidance {
            in navigation : BlueDogLogicalArchitecture::NavigationEstimate;
            in navigationUsable : ScalarValues::Boolean;
            in permission : BlueDogLogicalArchitecture::OperationPermission;''')
replace('''        #logicalScenario action def NavigationUpdate {
''','''        #logicalScenario action def NavigationUpdate {
            in permission : BlueDogLogicalArchitecture::OperationPermission;
''')
replace('''            flow validate.current to guide.navigation;
            flow guide.command to actuate.command;''','''            flow validate.current to guide.navigation;
            flow validate.usable to guide.navigationUsable;
            bind guide.permission = permission;
            bind actuate.permission = permission;
            flow guide.command to actuate.command;''')
replace('''        allocate abortAndRecover.actuate to BlueDogLogicalArchitecture::vessel.recoveryActuation;''','''        allocate abortAndRecover.persist to BlueDogLogicalArchitecture::vessel.recording;
        allocate abortAndRecover.actuate to BlueDogLogicalArchitecture::vessel.recoveryActuation;''')
sources[behavior]='''package BlueDogBehaviorContracts {
    private import ScalarValues::*;
    private import ISQ::*;
    private import ModelingMetadata::refinement;
    doc /* Partial executable consumer contracts for the current Gorge mission.
     * NASA SE Handbook 4.3.1.2.2 and defense SE Guidebook 2026 section 6.2.3
     * inform end-to-end functions/allocation; SysML 2.0 sections 7.17-7.18
     * govern action semantics. Actual outcomes follow the named requirements.
     * No hardware scheduler, synchronized clock or durable storage is inferred. */

    action def AssessObservationUsability {
        in producerValid : Boolean;
        in contextApplicable : Boolean;
        in clockEstablished : Boolean;
        in observedAt : TimeValue;
        in now : TimeValue;
        in maximumAge : TimeValue;
        out usable : Boolean;
        first start;
        then action assess {
            assign usable := BlueDogInterfaceContracts::ObservationUsable(
                producerValid,contextApplicable,clockEstablished,observedAt,now,maximumAge);
        }
        then done;
    }
    action def SailingActuationGate {
        doc /* Evaluate immediately before dispatch against current observations
         * and permission, not only at command creation. Boolean applicability
         * inputs are assessed using the interface contracts; they are not defaults. */
        in commandApplicable : Boolean;
        in permissionApplicable : Boolean;
        in sailingPermitted : Boolean;
        in abortLatched : Boolean;
        in qualificationLost : Boolean;
        in capsized : Boolean;
        in windUsable : Boolean;
        in navigationUsable : Boolean;
        in requiredSafetyConfirmed : Boolean;
        out actuate : Boolean;
        first start;
        then action gate {
            assign actuate := commandApplicable and permissionApplicable and sailingPermitted
                and not abortLatched and not qualificationLost and not capsized
                and windUsable and navigationUsable and requiredSafetyConfirmed;
        }
        then done;
    }
    action def RecoveryActuationGate {
        doc /* R-101 inhibits motor thrust while qualifying or status unknown.
         * E-138 requires durable disqualification before commanded motor enable.
         * R-102 requires established recovery authorization after restart.
         * Abort is intentionally not a motor inhibit: recovery follows abort. */
        in recoveryRequested : Boolean;
        in commandApplicable : Boolean;
        in recoveryAuthorized : Boolean;
        in qualificationStateKnown : Boolean;
        in qualifying : Boolean;
        in disqualificationStored : Boolean;
        in recoveryPathAvailable : Boolean;
        in inhibitActive : Boolean;
        out motorEnable : Boolean;
        first start;
        then action gate {
            assign motorEnable := recoveryRequested and commandApplicable and recoveryAuthorized
                and qualificationStateKnown and not qualifying and disqualificationStored
                and recoveryPathAvailable and not inhibitActive;
        }
        then done;
    }
    action def RestoreQualification {
        doc /* Explicit restart assessment, distinct from constructing a new
         * attempt. E-139/E-145 require nonqualifying fallback for missing or
         * inconsistent persisted state. A live disqualification cannot be erased
         * by restoring an older record. Persistence and the 30 s restoration
         * deadline still need an actual storage/restart implementation. */
        in recordValid : Boolean;
        in persistedQualificationLost : Boolean;
        in currentQualificationLost : Boolean;
        out qualificationLostNext : Boolean;
        first start;
        then action restore {
            assign qualificationLostNext := currentQualificationLost or not recordValid or persistedQualificationLost;
        }
        then done;
    }
    action navigationValidation : AssessObservationUsability;
    action sailingGate : SailingActuationGate;
    action recoveryGate : RecoveryActuationGate;
    action restartQualification : RestoreQualification;
    allocate navigationValidation to BlueDogLogicalArchitecture::vessel.navigation;
    allocate sailingGate to BlueDogLogicalArchitecture::vessel.actuation;
    allocate recoveryGate to BlueDogLogicalArchitecture::vessel.recoveryActuation;
    allocate restartQualification to BlueDogLogicalArchitecture::vessel.supervision;
    #refinement dependency navigationAssessment from AssessObservationUsability to BlueDogMethod::Scenarios::ValidateNavigation;
    #refinement dependency sailingAssessment from SailingActuationGate to BlueDogMethod::Scenarios::ApplySailingCommand;
    #refinement dependency recoveryAssessment from RecoveryActuationGate to BlueDogMethod::Scenarios::ApplyRecoveryCommand;
    dependency motorInvariant from RecoveryActuationGate to BlueDogRequirements::motorQualificationInvariant;
    dependency durableAuthorization from RecoveryActuationGate to BlueDogRequirements::qualificationPersistence;
    dependency freshAuthorization from RecoveryActuationGate to BlueDogRequirements::freshRecoveryCommand;
    dependency restorationPolicy from RestoreQualification to BlueDogRequirements::qualificationRestoration;
    dependency unknownFallback from RestoreQualification to BlueDogRequirements::unknownQualificationFallback;
    metadata issue : ModelingMetadata::Issue {
        text = "B-01: Bind installed message contexts to usability, current permissions and consumer gates; scalar conceptual simulations do not implement serialization. B-02: Demonstrate atomic durable state, acknowledgment ordering, all restriction restoration and restart deadlines on selected hardware. B-03: Resolve controller concurrency, command arbitration, resource ownership and timeout budgets, including abort during capsize/recovery. B-04: Implement and measure estimators, achieved actuation and repeated dynamic recovery; descriptive scenarios do not prove these functions.";
    }
}
'''
model=connection().parse_sources(tuple((str(p),t) for p,t in sources.items()),strict=True)
assert not model.diagnostics,model.diagnostics
for path in (method,behavior):
    path.write_text(sources[path])
print('Native candidate accepted: explicit permission paths, durable acknowledgment and consumer/restart actions.')


"""Author reviewed use categories onto the frozen native inventory, not a SysML parser."""
import json
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
stage=ROOT/'reviews/se-skills-2026-10-23/06-analysis-credibility'
inventory=json.loads((stage/'before.json').read_text())
# Category purposes describe supportable use, never completed physical validation.
categories={
'Inputs':('Export declared parameters or provisional sensitivity assumptions for an identified caller.','The owning configuration and consumer units/vector ordering; these cases export inputs, not predicted performance.','No feasibility, measured uncertainty distribution or physical capability follows from exporting values.','Trace each value to its owner, external-data pedigree and consuming analysis; verify conversions.'),
'HistoricalReview':('Inspect recorded operating screens and unaccepted evidence for the original archived candidate.','Only the original run configuration, policy, source revision and sampled scenarios.','No current IC-01 design substitution, physical qualification or transfer of margins between configurations.','Preserve archive manifests and source hashes; assess new use separately against current configuration and policy.'),
'Rules':('Evaluate navigation-rule obligations or fixture consistency from supplied situation facts.','Declared rule edition, delivered tracks, vessel/status/visibility/channel facts and bounded encounter context.','Supplied facts do not demonstrate perception, legal status or achieved safe maneuver; no universal compliance claim.','Validate actual fact acquisition, rule applicability and full encounter behavior against authoritative rules and observations.'),
'Readiness':('Expose missing review/evidence preconditions in the named safety or configuration argument.','Declared review scope, configuration, contributors and supplied review assertions.','A true review flag or complete register does not demonstrate control effectiveness, install hardware or accept risk.','Actual configuration, implementation/effectiveness records, coverage review and responsible disposition evidence.'),
'Trade':('Compare declared rig evidence gates or illustrate a supporting buoyancy calculation.','The named candidate and ordered evidence vector, or explicit synthetic buoyancy inputs.','No invented scores, hardware downselect, accepted reliability estimate or physical qualification.','Comparable both-tack, energy, durability, construction, casualty and reliability-study evidence; separate mandatory criteria from studies.'),
'Recovery':('Screen conditional recovery authority, exposure or energy for supplied capabilities and route.','Named configuration, current, orientation, usable reserve, approach and response assumptions.','No demonstrated thrust, whole-river recoverability, physical independence, shore retention or pickup.','Measured installed propulsion/energy and casualty-response envelopes; route and approach evidence with uncertainty.'),
'Sailing':('Estimate polar demand, conditional progress or hull/route screens under declared inputs.','Supplied polar/geometry, current, wind, leeway and bounded route assumptions.','Demand ratios and solved states do not predict a measured voyage or establish performance outside the studied envelope.','Both-tack measured polar and mass/drag evidence; discretization, convergence and environment-domain sensitivity.'),
'Equipment':('Account for candidate equipment allocations or illustrative actuator/energy loads.','Declared included/excluded components, duty assumptions, modes and accounting boundary.','An allowance or arithmetic rollup is not a measured installed budget, peak capability or architecture downselect.','Identified component/BOM and synchronized mass, peak/average power, duty and environmental measurements.'),
'Encounter':('Screen class detection, acquisition or response-distance/exposure from supplied bounds.','Specified target/class, timing, uncertainty, controller state and envelope assumptions.','Allocated observation or response bounds are not demonstrated sensing coverage, maneuver completion or accepted safety margins.','Installed target-class detection/error/dropout and timing evidence including interacting faults and occupied maneuvers.'),
'Weather':('Explore environmental or passage-exposure sensitivity with declared scenario values.','Named wind/current/wave/weather assumptions, geometry and sampled domain.','Scenario sweeps are not calibrated probability distributions, full-domain coverage or voyage reliability evidence.','Observed environmental basis, dependence and coverage review; uncertainty and sensitivity for the proposed use.'),
'EnergyReliability':('Evaluate conditional energy reconciliation or mission-reliability arithmetic for the named subject.','Declared load/exposure/storage boundaries or failure-rate partition, dependence and hazard assumptions.','Numerical success does not establish measured load, accepted rates, independence or physical reliability/energy sufficiency.','Configuration-specific measurements, rate/profile justification, common-cause/dependence review and uncertainty assessment.'),
'Geometry':('Inspect a geometric/course or analytic hydrostatic fixture.','Declared coordinate/geometry conventions and simplified analytic assumptions.','A consistent fixture is not surveyed course truth, validated free-surface response or installed-vessel performance.','Independent coordinate/unit checks, geometry survey or hydrostatic comparison relevant to the proposed use.')}
def category(name):
    root,tail=name.split('::',1)
    if root in ('BlueDogCurrentSizing','BlueDogRecordedSizing','BlueDogSizingEvidence'):return 'HistoricalReview'
    if root.startswith('Inland') or root=='BlueDogNavigationController':return 'Rules'
    if root in ('BlueDogSafety','BlueDogConfigurationManagement'):return 'Readiness'
    if root=='BlueDogSailTrade':return 'Trade'
    if tail in ('Inputs','SensitivityInputs','Defaults','StudyInputs','MaterialInputs','material','convergenceInputs','sweepInputs'):return 'Inputs'
    if root in ('BlueDogIntegratedCandidate','BlueDogRecoveryRisk','RecoveryPropulsionTrade'):return 'Recovery'
    if root.startswith('BlueDogSailing') :return 'Sailing'
    if root in ('BlueDogAcousticEquipment','BlueDogWindEquipment','BlueDogWingActuator','MarineEnergy'):return 'Equipment'
    if root in ('BlueDogClassDetection','BlueDogEncounterEnvelope','BlueDogEncounterReview','BlueDogAvoidanceFailures'):return 'Encounter'
    if root in ('BlueDogWeather','BlueDogEnvironmentReview','BlueDogLocationTraffic','BlueDogPassageExposure'):return 'Weather'
    if root in ('BlueDogCandidateEnergy','BlueDogEnergy','BlueDogReliability','BlueDogReliabilityExamples'):return 'EnergyReliability'
    if root in ('BlueDogHydrostatics','TransGorgeCourse'):return 'Geometry'
    raise ValueError('Review unclassified native case: '+name)
lines=['package BlueDogAnalysisCredibility {','    private import ScalarValues::*;','    metadata def UseIntent {']
for field in ('category','intendedUse','domain','excludedUses','evidenceNeeded'):lines.append('        attribute '+field+' : String;')
lines+=['    }']
for cat,values in categories.items():
    lines.append('    metadata def '+cat+' :> UseIntent {')
    for f,v in zip(('category','intendedUse','domain','excludedUses','evidenceNeeded'),(cat,*values)):lines.append('        attribute :>> '+f+' = '+json.dumps(v)+';')
    lines.append('    }')
for i,row in enumerate(inventory,1):lines.append(f'    metadata use{i:03d} : {category(row["id"])} about {row["id"]};')
lines+=['','    calc def UsePreconditions {', '        doc /* Supplied review assertions for a proposed use, not an acceptance decision or a requirement that the design pass its screens. */']
flags=['intendedUseReviewed','configurationApplicable','domainApplicable','inputPedigreeReviewed','implementationVerified','validationAdequateForUse','uncertaintyReported','sensitivityReviewed','defectsDispositioned','limitationsReported']
for f in flags:lines.append('        in '+f+' : Boolean [1];')
lines+=['        return eligible : Boolean = '+' and '.join(flags)+';','    }','}']
(ROOT/'models/analyses/credibility.sysml').write_text('\n'.join(lines)+'\n')
(stage/'classifications.json').write_text(json.dumps({r['id']:category(r['id']) for r in inventory},indent=2)+'\n')
print('Classified',len(inventory),'native definitions/usages')

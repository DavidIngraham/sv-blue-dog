# Refinements and design-basis dependencies

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

Refinement points from a more precise representation to the element it clarifies. Plain dependency points from a dependent design obligation to its basis; it makes no satisfaction implication. These are model relationships, not completed evidence.

## Refinement

| Refining element | Refined element | Rationale |
| --- | --- | --- |
| roundTrip | courseCompletion | Ordered gate crossings make the course-completion obligation more precise; gate locations remain open. |
| communications | liveObservation | The vehicle telemetry requirement provides a more precise outage-retention and delivery specification for the observation aspect of C-005. Autonomous execution remains separately required. |
| SustainedReserveProtectionCriterion | sustainedReserveProtection | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| RepeatableCycleBalanceCriterion | repeatableCycleBalance | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| PeakSupplyCapabilityCriterion | peakSupplyCapability | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| HarvestCampaignCoverageCriterion | harvestCampaignCoverage | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| LegProgressCriterion | legProgress | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| PassageDurationCriterion | passageDuration | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| MissionReliabilityCriterion | missionSuccessProbability | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |
| FailureRateCriterion | failureRateBudget | Formalizes the numerical acceptance relation on supplied inputs. The requirement qualification conditions, input representativeness and evidence obligations still apply. |

## Plain dependency

| Dependent requirement | Design basis | Rationale |
| --- | --- | --- |
| multiDayEndurance | repeatedOperation | Repeated autonomous journeys motivate the existing endurance and harvesting requirement; M-002 defines an initial 72-hour campaign; indefinite operation remains an objective. This is design motivation or an implementation choice, not a satisfaction implication. |
| navigationAndControl | unassistedAttempt | The vessel needs onboard guidance and control to complete an unassisted attempt. This is design motivation or an implementation choice, not a satisfaction implication. |
| roundTrip | sailingPropulsion | Vehicle challenge operation excludes auxiliary motor propulsion; powered development tests are separate. This is design motivation or an implementation choice, not a satisfaction implication. |
| communications | emergencyIntervention | Vehicle communications provide emergency commands whose use ends attempt qualification. This is design motivation or an implementation choice, not a satisfaction implication. |
| multiDayEndurance | hawaiiVoyage | An ocean passage motivates sustained energy autonomy; multi-day operation is an interim capability, not an ocean endurance sizing result. This is design motivation or an implementation choice, not a satisfaction implication. |
| navigationAndControl | hawaiiVoyage | An autonomous Hawaii passage needs ocean guidance and sailing control; N-001 specifies its environmental design envelope. This is design motivation or an implementation choice, not a satisfaction implication. |
| communications | hawaiiVoyage | The long-term ocean mission motivates review of monitoring coverage and outage behavior without selecting a radio technology. This is design motivation or an implementation choice, not a satisfaction implication. |
| resetRecovery | hawaiiVoyage | Extended unattended operation motivates recovery from onboard resets. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionEvidence | hawaiiVoyage | Ocean mission assessment requires retained voyage evidence; E-007 specifies recording and retention acceptance criteria. This is design motivation or an implementation choice, not a satisfaction implication. |
| navigationAndControl | roundTrip | Autonomous completion of the route needs observations, guidance, and actuation. This is design motivation or an implementation choice, not a satisfaction implication. |
| resetRecovery | roundTrip | A reset during an autonomous journey must not leave mission behavior undefined. This is design motivation or an implementation choice, not a satisfaction implication. |
| communications | roundTrip | Mission supervision and recovery need an agreed operator communication policy. This is design motivation or an implementation choice, not a satisfaction implication. |
| ingressResponse | roundTrip | Recovering the boat after the journey motivates a defined response to small leaks. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionEvidence | roundTrip | Assessing route completion and learning from the mission requires recorded evidence. This is design motivation or an implementation choice, not a satisfaction implication. |
| energyAwareness | multiDayEndurance | Multi-day operation with variable harvesting needs energy estimation and load management. This is design motivation or an implementation choice, not a satisfaction implication. |
| lowEnergyRecovery | multiDayEndurance | Harvest shortfalls need an explicit degraded operating mode. This is design motivation or an implementation choice, not a satisfaction implication. |
| lowEnergyRecovery | energyAwareness | Available-energy estimates and reserve policy must drive low-energy transitions. This is design motivation or an implementation choice, not a satisfaction implication. |
| transportability | DesignIntent | The owner requires one-person handling independently of either voyage outcome. |
| desktopManufacture | DesignIntent | The owner selected a 250 mm cubic desktop-printer build volume independently of mission completion. |
| serviceability | DesignIntent | Between-attempt serviceability is a project lifecycle constraint; it is not entailed by unassisted endurance. |
| trafficSafety | navigationAndControl | TrafficSafety supports navigationAndControl. This is design motivation or an implementation choice, not a satisfaction implication. |
| operatingBoundary | roundTrip | OperatingBoundary supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| safeRecovery | emergencyIntervention | Permitted emergency intervention requires explicit abort, qualification, isolation and control-loss behavior. This is design motivation or an implementation choice, not a satisfaction implication. |
| navigationConspicuity | trafficSafety | NavigationConspicuity supports trafficSafety. This is design motivation or an implementation choice, not a satisfaction implication. |
| regulatoryClassification | roundTrip | RegulatoryClassification supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| environmentalEnvelope | roundTrip | EnvironmentalEnvelope supports roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| marineDurability | environmentalEnvelope | MarineDurability supports environmentalEnvelope. This is design motivation or an implementation choice, not a satisfaction implication. |
| stabilityAndFouling | environmentalEnvelope | StabilityAndFouling supports environmentalEnvelope. This is design motivation or an implementation choice, not a satisfaction implication. |
| recoveryPropulsion | safeRecovery | RecoveryPropulsion supports safeRecovery. This is design motivation or an implementation choice, not a satisfaction implication. |
| recoveryEnergy | recoveryPropulsion | RecoveryEnergy supports recoveryPropulsion. This is design motivation or an implementation choice, not a satisfaction implication. |
| telemetryEquipment | communications | TelemetryEquipment supports communications. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | communications | CommandIntegrity supports communications. This is design motivation or an implementation choice, not a satisfaction implication. |
| environmentalEnvelope | hawaiiVoyage | Ocean operation requires its own environmental envelope; Gorge success does not establish it. This is design motivation or an implementation choice, not a satisfaction implication. |
| gorgeEnvironment | roundTrip | The Gorge mission sets the river environment; it does not impose the ocean profile. This is design motivation or an implementation choice, not a satisfaction implication. |
| oceanEnvironment | hawaiiVoyage | The Hawaii mission sets the ocean environment; this profile is not a Gorge acceptance prerequisite. This is design motivation or an implementation choice, not a satisfaction implication. |
| recoveryPropulsorWeeds | recoveryPropulsion | The recovery propulsor must remain usable in the vegetation encountered by the sailing vessel. This is design motivation or an implementation choice, not a satisfaction implication. |
| launchEnergyAdmission | recoveryEnergy | LaunchEnergyAdmission isolates a separately verifiable consequence of recoveryEnergy. This is design motivation or an implementation choice, not a satisfaction implication. |
| challengeMotorInhibition | sailingPropulsion | ChallengeMotorInhibition isolates a separately verifiable consequence of GorgeChallenge::sailingPropulsion. This is design motivation or an implementation choice, not a satisfaction implication. |
| challengeMotorInhibition | unassistedAttempt | No-intervention qualification must survive resets and motor-mode transitions. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | unassistedAttempt | Accepted external control changes the attempt qualification; communications alone does not supply this rule. This is design motivation or an implementation choice, not a satisfaction implication. |
| commandIntegrity | emergencyIntervention | The emergency control channel needs authenticated, fresh commands and persistent qualification changes. This is design motivation or an implementation choice, not a satisfaction implication. |
| operatingBoundary | hawaiiVoyage | An ocean route also needs configured boundaries and no-feasible-route behavior; its boundaries differ from the Gorge course. This is design motivation or an implementation choice, not a satisfaction implication. |
| regulatoryClassification | hawaiiVoyage | Deployment permissions and applicable rules depend on the ocean route as well as the Gorge mission. This is design motivation or an implementation choice, not a satisfaction implication. |
| serviceability | hawaiiVoyage | Unattended ocean preparation and post-voyage maintenance motivate replaceable modules; this is not at-sea servicing during qualification. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedEnergyFeasibility | repeatedOperation | Repeated journeys motivate a repeatable energy cycle, beyond a one-off endurance run. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedEnergyFeasibility | hawaiiVoyage | The ocean ambition requires sustained energy autonomy; route-specific resources remain unresolved. This is design motivation or an implementation choice, not a satisfaction implication. |
| sustainedReserveProtection | recoveryEnergy | Sustained operation protects the recovery reserve sized by the existing R-002 policy. This is design motivation or an implementation choice, not a satisfaction implication. |
| cruisePerformance | roundTrip | cruisePerformance is a selected engineering objective supporting roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| cruisePerformance | hawaiiVoyage | cruisePerformance is a selected engineering objective supporting hawaiiVoyage. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | roundTrip | missionReliability is a selected engineering objective supporting roundTrip. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | hawaiiVoyage | missionReliability is a selected engineering objective supporting hawaiiVoyage. This is design motivation or an implementation choice, not a satisfaction implication. |
| missionReliability | repeatedOperation | missionReliability is a selected engineering objective supporting repeatedOperation. This is design motivation or an implementation choice, not a satisfaction implication. |

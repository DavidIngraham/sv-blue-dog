# Environmental requirements decomposition

N-001 describes the combined Gorge and northeast Pacific operating environment. Its children describe the two environments; their leaves specify independently verifiable wind, wave and current performance. Shared exposure and contingency requirements derive directly from N-001. N-002 and N-003 organize durability and capsize/vegetation tolerance.

The numerical limits are proposed engineering targets, not measured Columbia River extremes or demonstrated hardware capability. See the [native register](requirements-register.md) for authoritative statements and the [verification plan](verification-plan.md) for evidence and unresolved inputs. Work status is encoded in SysML metadata.

| Parent | Derived requirements |
| --- | --- |
| N-001 EnvironmentalEnvelope | N-010 GorgeEnvironment; N-020 OceanEnvironment; N-030–N-035 shared conditions; N-002 durability; N-003 stability/fouling |
| N-010 GorgeEnvironment | N-011 wind; N-012 waves; N-013 current; N-014 survival wind; N-015 survival waves |
| N-020 OceanEnvironment | N-021 wind; N-022 waves; N-023 current; N-024 survival wind; N-025 survival waves |
| N-002 MarineDurability | N-041 freshwater; N-042 saltwater; N-043 sealing; N-044 mechanical integrity; N-045 electrical integrity; N-046 solar heating; N-047 material aging |
| N-003 StabilityAndFouling | N-051 righting; N-052 control recovery; N-053 weed passage; N-054 snag shedding; N-055 blockage response; N-056 powered recovery through weeds |

Every row represents explicit SysML derivation connections. Each leaf has a separate design allocation. Parent acceptance requires evidence for all applicable children; a diagram or `satisfy` allocation does not establish that evidence.

| Condition | Gorge operation | Ocean operation | Survival |
| --- | --- | --- | --- |
| Mean wind / 3-second gust | 3–15 / 20 m/s | 3–15 / 20 m/s | 25 / 35 m/s, 24 h |
| Significant / individual wave height | 1 / 2 m | 3 / 6 m | Gorge 2 / 4 m; ocean 6 / 12 m, 24 h |
| Peak wave period | 2–5 s | 5–20 s | Gorge 3–7 s; ocean 6–20 s |
| Current magnitude | 1.5 m/s | 1.0 m/s | Same respective limits |
| Air / water temperature | 0–40 / 2–30 degC | Same | Same |

The model states reference conventions and functional acceptance. Physically realizable combinations and adverse directions must be considered; independent single-axis exposures alone do not establish combined-envelope capability. Calm conditions do not guarantee station keeping, and current tolerance does not guarantee upstream progress at every wind angle. Hurricanes, ice, log impact and surf-zone launch are outside this initial qualification scope.

## Milfoil and submerged weeds

The user's Columbia River milfoil observation is an explicit design input. N-053 requires five passes through a specified submerged vegetation patch without manual clearing or motor assistance, with minimum retained sailing speed and recovered rudder travel. N-054 tests individual appendage snags. N-055 requires detection and contingency response when the boat cannot continue. N-056 separately qualifies powered recovery and locked-propulsor shutdown; an air propeller is not excluded by the wording.

The patch density and geometry are repeatable engineering test targets, not claims about measured local weed-bed density. Wet bending stiffness and branch geometry must be recorded, and a surrogate must be shown representative of local milfoil before this qualification can close. Dense floating mats are an avoidance/blockage case, not an assumed pass-through capability. No weed-clearing maneuver may silently enable the motor during a qualifying attempt.

## Evidence

Record environmental histories, loading, internal temperatures, water-sensitive indicators, power/control logs, and pre/post inspection. Use controlled facilities and validated analysis where field tests cannot reproduce the required conditions. The 72-hour freshwater and 30-day saltwater exposures do not prove indefinite life or establish the eventual Hawaii passage duration.

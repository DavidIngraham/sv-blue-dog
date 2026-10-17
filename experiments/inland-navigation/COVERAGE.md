# Coverage and remaining boundaries

Source profile: [U.S. Inland Navigation Rules, 33 CFR 83–90](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-E), reviewed 16 October 2026.
This is an implementation inventory, not a legal opinion or completed verification.

| Rule | Executable representation | Still external or incomplete |
| --- | --- | --- |
| 1 | `General`: jurisdiction/local-provision gates; certificate checks in `ExemptionsAndSpecialCases` | Legal/geographic applicability, complete local-rule inventory, copy-of-rules carriage |
| 2 | Necessary-departure assessment conditions | Ordinary seamanship, responsibility and justification of departure |
| 3 | Typed vessel/status/tack/visibility inputs; composite-unit and special-craft checks | Classification from observations and all definition edge cases |
| 4 | General checks independent of visibility | Demonstrating capability in each admitted visibility condition |
| 5 | Sight, hearing and available-means checks | Sensor performance and adequate lookout assessment |
| 6 | Visibility, traffic, maneuverability, lighting, weather/current, depth and radar-factor checks | Numerical safe-speed selection and stopping prediction |
| 7 | Doubt/steady-bearing risk, radar-use and close/tow appraisal checks | Risk estimation and uncertainty from actual tracks |
| 8 | Candidate timing, substantial action, safe passing, monitoring, speed reduction and independent nonimpediment checks | Predicting clearance, selecting a maneuver and validating judgment thresholds |
| 9 | Channel edge, fishing/small-vessel nonimpediment, crossing, bends, anchoring, special-river role; signal analysis | Complete temporal passage negotiation and river-priority maneuver execution |
| 10 | Lane direction, crossing angle, inshore/separation-zone conditions, entry/exit, anchoring, nonimpediment and exemption flags | Surveyed scheme geometry; clause-specific bounds of maintenance/cable exemptions |
| 11 | Visual applicability gates | Visual observability assessment |
| 12 | Opposite/same tack and uncertain-other-tack duties | Rig-specific tack/windward classification |
| 13 | Bearing/motion test, own doubt, persistent overtaking and clearance | Stable track identity and motion/clearance evidence |
| 14 | Mutual head-on duty, starboard candidate restriction, agreement and special-river roles | Complete agreement lifecycle, commanded turn magnitude and dynamics |
| 15 | Powered crossing role and crossing-ahead restriction; river-crossing role | Encounter recognition and feasible trajectory |
| 16 | Keep-clear response plus early/substantial candidate checks | Physical achievement and quantitative interpretation |
| 17 | Hold/may-act/shall-act escalation and optional port-turn restriction | Establishing other-vessel response and give-way-only insufficiency |
| 18 | Power/sail/fishing/NUC/RAM relationships; seaplane/WIG obligations | Special-craft composition with every pairwise case; status recognition |
| 19 | Radar-only directional restrictions, minimum speed/caution, engine readiness | Restricted-visibility sensing, trajectory generation and necessary departures |
| 20 | Night/day/restricted-visibility display conditions; necessary bridge lowering and restoration checks | Installed visibility and physical lowering sequence |
| 21 | Arc/color/flash demands | Full mounted-sector observation/recognition |
| 22 | Length-based range demand and intensity calculation | Measured installed photometry |
| 23 | Powered light pattern, small-vessel and Great Lakes alternatives, air-cushion/WIG supplements | Every special installation layout |
| 24 | Tow/push/composite and group patterns, long-tow diamond/stack, partial-tow outlines, regional alternatives | Full alongside/group geometry and impracticability measures |
| 25 | Sailing/rowing alternatives, powered-sail normalization, cone boundary and optional red-over-green selection | Actual prompt torch display and installed arrangements |
| 26 | Trawl/fishing patterns, making-way/outlying-gear additions and optional close-proximity signals | Complete physical pattern instantiation |
| 27 | NUC/RAM/diving/dredging/mine patterns, obstruction sides, restricted-tow supplements, small-vessel exception | All physical arrangements and complete operational signal recognition |
| 28 | Explicit reserved marker | No Inland obligation to encode |
| 29 | Pilot display and optional identity-signal count | Active pilot-duty recognition |
| 30 | Anchor/grounding patterns, size/location exemptions, barge triggers and corner-marking demands | Measured barge-group geometry and exact local exemption geography |
| 31 | Closest-possible-compliance review trigger for seaplane/WIG | Actual permissible alternative arrangement |
| 32 | Short/prolonged duration checks | Assessed tolerance for about one second |
| 33 | Whistle/bell/gong size thresholds and small efficient-sound alternative | Installed appliance evidence |
| 34 | Inland passage/overtaking/danger/bend/departure outputs; bounded agreement memory and exchange evidence | Complete temporal protocol, actual emission/hearing and maneuver identity |
| 35 | Mode/anchor/grounding fog patterns, interval deadlines and small-vessel alternatives | Real signal scheduler, synchronized emissions and complete recovery-mode composition |
| 36 | Non-confusing/non-dazzling attention-signal gate | Physical signal interpretation and installation |
| 37 | Distress-plus-assistance requirement, Annex IV family catalog and misuse rejection | Actual signal encoding/recognition and communication delivery |
| 38 | Historical eligibility and individual exemption boundaries | Documentary evidence; no automatic exemption for a new build |
| Annex I / 84 | Range/intensity/color screening, selected height/spacing/shape/sector checks | All special installation layouts, high-speed alternatives, approval and complete photometric evidence |
| Annex II / 85 | Reserved | No additional Inland annex obligations |
| Annex III / 86 | Frequency/intensity/direction/listener-exposure checks; bell and combined-whistle constraints | Full gong measurements and installation certification |
| Annex IV / 87 | Signal-family catalog, frequency boundary, authorized-use gate and supplemental-aid distinction | Physical signal encoders/decoders and assistance delivery |
| Annex V / 88 | Blue/red-yellow eligibility; no inferred priority | Authorization and installation evidence |
| 89 | Certificate validity/carriage checks; sourced special-river applicability flags | Administrative process and exact geographic lookup |
| 90 | Mechanical composite-unit and mooring-buoy checks | Full unmanned-barge exception evidence |

The remaining column is intentional. Representing a rule group does not mean
every clause is algorithmically solved. Some are hardware acceptance criteria;
others require legal or operational judgment. `additionalApplicableClausesReviewed`
is an explicit external assessment in combined candidate evaluation, not a
claim that those clauses are already encoded. A failed or absent assessment
must not be replaced with a default true value in production integration.

# Executable Inland Rules and mission integration

The reusable SysML v2 model evaluates navigation duties, candidate-action
restrictions, signal obligations and selected equipment checks using the pinned
native OpenSysML engine. An opt-in mission adapter now uses the pairwise
assessment to filter primary sailing commands. The wider equipment and combined
compliance assessments remain separate from that controller.

The expanded model represents every numbered Inland Rule through executable
logic, definitions/applicability, or an explicit assessment boundary. That is
not a claim of exhaustive implementation of every paragraph. The [coverage
register](COVERAGE.md) identifies the distinction. In particular, a Boolean
input saying an installation was reviewed is not an implementation of its
geometry or a substitute for the review.

## Run and inspect

```sh
.tools/uv run python experiments/inland-navigation/run.py
.tools/uv run pytest -q experiments/inland-navigation/test_navigation.py tests/test_navigation_integration.py
.tools/uv run python -m tools.boat_analysis.mission.navigation_study
```

[`inland-pair.sysml`](../../models/libraries/navigation/inland-pair.sysml) owns pairwise roles, precedence, overtaking memory and
response escalation. [`inland-obligations.sysml`](../../models/libraries/navigation/inland-obligations.sysml) owns general-duty checks, channels and
traffic separation, restricted visibility, lights/shapes, signals, selected
annex calculations, special display alternatives, bounded passage agreement,
distress-signal families, exemption eligibility and combined candidate assessment.
`run.py` discovers input types through the native API, transports fixtures and
wires native outputs into the native combined assessment. Navigation equations
are not implemented in Python. Required inputs have no model defaults.

`cases.json` and `extended-cases.json` are fully specified synthetic assessed
facts with independently authored expectations. `results.json` records their
native outputs and source hashes. These are software regression cases, not
physical encounters. Additional pytest cases check missing inputs, native
missing-input rejection and composition across domains.

## What changed in the expanded scope

The pair evaluator now includes power-driven head-on/crossing encounters,
ordinary power/sail relationships, legally engaged fishing, not-under-command
and restricted-maneuverability status. A craft label alone does not establish
one of those statuses. Special inland river provisions require a separately
reviewed geographic classification; the Columbia is not classified as a
Western River merely because it is in the western United States.

Overtaking retains precedence. Channel and traffic-separation obligations are
independent of pairwise stand-on/give-way roles. A powered crossing candidate
is checked for crossing ahead and the Rule 17(c) port-turn restriction. Head-on
candidates distinguish a starboard alteration from an agreed alternative.
Rule 19 produces candidate restrictions without awarding a stand-on role.

Equipment analyses select light/shape patterns, visibility ranges, arcs,
chromaticity screens, intensity, selected installation dimensions, sound-signal
patterns and timing, and selected acoustic appliance thresholds. Size-based
alternatives and historical exemptions are conditional. Inland Rule 28 and
Annex II/Part 85 are reserved; no International constrained-by-draft privilege
is imported into the Inland profile.

## Read outputs as conditional results

- `role` and `response` describe a pairwise encounter; they do not grant overall
  priority over other waterway users.
- `nextMemory` is the native overtaking transition. Its caller preserves track
  identity and carries state between observations; this is not a persistent
  state-machine service.
- Individual `...Supported` outputs concern their stated domain only.
- `compose_candidate()` passes native domain results to `CandidateAssessment`.
  `SnapshotConsistency` rejects inconsistent shared lengths, modes, visibility,
  channel facts, collision-risk inputs or passage-agreement evidence. Motor-sailing
  requires powered fog-signal classification. The caller must still establish the
  same encounter identity, timestamp and proposed maneuver across all frames.
- `candidateSupported` means this supplied candidate passes the implemented
  checks and the explicitly supplied review assertions. It is not a trajectory
  optimizer, autonomous navigation approval or full compliance determination.
- `completeComplianceEstablished` remains false in every analysis.

The combined example checks one fixture/installation case. All installed lights,
all relevant modes, additional applicable clauses and dynamic response still
need complete evidence coverage. Passing one lamp check cannot approve the boat.

## Interpretations and external judgments

The rules contain both precise boundaries and qualitative obligations. The
model directly encodes boundaries such as 112.5 degrees for overtaking,
20 m for channel nonimpediment, light-range length bands, and fog-signal periods.
It does not invent universal collision distances, safe speeds, turn magnitudes
or delays for the words early, substantial, appropriate or finally clear.

The following choices are explicit engineering interpretations:

| Choice | Consequence |
| --- | --- |
| Unknown own-overtaking evidence is treated conservatively; uncertain other-overtaking does not award stand-on status | Avoids converting uncertainty into priority |
| Clearance requires independent evidence and a consistent no-risk appraisal | Loss of a track cannot erase an overtaking duty |
| Required directional restrictions reject unsupported candidates | A necessary departure requires a separate Rule 2 assessment |
| Facts-known and review inputs are required | Missing evidence cannot become a default pass; the truth of those assertions still needs support |
| Short-blast tolerance is supplied explicitly | The statutory word about is not assigned a hidden tolerance |
| Small commensurate shapes and special installation alternatives require review | The model does not invent a small-vessel scale factor or issue an exemption |
| Chromaticity screening orders red corner coordinates around their boundary | Published table-column order is not treated as a self-crossing polygon; this ordering needs review against the incorporated CIE standard. Optical evidence is independently required |
| Domain consistency checks cover selected shared facts | They do not solve track association, sensor fusion or guarantee the frames describe one candidate |

Tack/windward interpretation for unconventional rigs, vessel status, channel
confinement, collision risk, appropriate action, maneuver feasibility and
practicability still require external assessment. Scalar magnitudes carry units
in their names/documentation; this experiment does not establish dimensioned
quantity interoperability.

## Was SysML suitable?

Yes for typed conditional duties, persistent encounter state, candidate
restrictions and testable equipment constraints. The native engine executes the
expressions, including enum inputs/outputs, without a second navigation rule
engine. Expansion has not demonstrated a computational limit of SysML.

The awkward parts were overlapping obligations, temporal meaning and qualitative
judgments. Expanding a vessel classification affected channel duties and light
and signal selection, not just the pairwise priority table. Independent review
caught gaps in those interactions, which now have regression cases. Long nested
conditionals are harder to review than decision tables; further refactoring
should improve presentation before adding more detailed maneuver selection.

SysML cannot make a legal interpretation true merely by executing it. It also
does not supply sensor truth, hydrodynamics or physical evidence. Those are
separate engineering tasks. Code generation, embedded performance, cross-tool
portability and formal proof have not been established.

## Mission replay boundary

The adapter receives only delivered observations. Navigation metadata is absent
unless the observation scenario explicitly supplies it; it shares observation
latency and expiry. Roles and overtaking-memory transitions execute in the native
pair model. Native candidate constraints implement hold/may-act/shall-act and
keep-clear responses. A lost track cannot clear an established overtaking duty.
An unresolved applicable duty or absence of a supported candidate causes abort.

The current integration accepts an assessed clear-visibility, non-channel context.
Other contexts fail an explicit scope gate even with no contacts. The full rule
library is broader than this first controller integration. Equipment, signals,
Rule 19 maneuver control, multi-vessel negotiation and powered recovery navigation
are not established by a primary-sailing result. Bounded maneuver dynamics cannot
yet be combined with this adapter; the replay retains the archived kinematic model.

Both the geometric control and rule-enabled comparison use the same candidate
headings and piecewise command-latency, drifting-turn and sailing forecasts.
The remaining committed trajectory is checked at each control tick. Continuation
approval belongs only to pairs assessed for the current command and cannot bypass
changed duties, inadequate facts or a newly conflicting segment. Independent
traffic truth still scores actual contact and clearance; it cannot supply unseen
observations or veto a command secretly.

The [controller policy](../../models/analyses/navigation-controller.sysml) declares
2-degree/0.05 m/s hold tolerances, a 15-degree substantial-turn hypothesis,
10-degree bearing uncertainty and a twice-protected-envelope clearance-release
hypothesis. These are not statutory thresholds or accepted physical criteria.
Averaged sailing course is a bow-heading proxy; unconventional-rig tack and actual
maneuver achievement still require evidence. Depowering is not credited as a
substantial heading change.

The paired study freezes IC-01 sizing and all 29 archived local scenarios. It
compares geometry-only control, missing navigation assessments, and explicitly
hypothetical identification/response assessments. A separate four-case timed
crossing probe changes arrival time to exercise a closer encounter. It adds no
hardware mass or power credit. Earlier aborts can save energy while failing the
mission; they must not be called efficiency improvements.

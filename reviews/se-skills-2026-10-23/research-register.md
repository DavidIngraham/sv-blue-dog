# Cross-stage source discovery

Research gathered while stage 1 regressions run. This does not mark any later skill or model stage implemented.

- Behavior: NASA SE Handbook 4.3, especially 4.3.1.2.2 (functions, inputs/outputs, failure modes and end-to-end sequencing): https://www.nasa.gov/reference/4-3-logical-decomposition/ . OMG SysML 2.0 Part 1 formal/2026-03-02 sections 7.17-7.18 for action/state semantics; inspect actual clauses before using. NASA-HDBK-1009A approved 2025-03-12: https://standards.nasa.gov/system/files/tmp/2025-03-12-NASA-HDBK-1009A.pdf ; uses SysML v1 examples, so use engineering intent only when working in v2.
- Verification/validation: NASA handbook 5.3 https://www.nasa.gov/reference/5-3-product-verification/ and 5.4 https://www.nasa.gov/reference/5-4-product-validation/ . Read 5.3.1.2.1 onward for readiness/procedure/results, and 5.4.1.2 for intended use/environment and users. Defined objective is not execution/acceptance. Verification vs validation concern distinct claims; do not label all analysis validation.
- Safety: ASSIST MIL-STD-882 record https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=36027 ; indexed current technical version E Change1 incorporated dated 2023-09-27. Obtain and inspect full technical document before attributing task/clauses. Record metadata alone does not support detailed rules.
- Configuration: NASA handbook 6.5 https://www.nasa.gov/reference/6-5-configuration-management/ ; 6.5.1.2 lists planning, identification, change management, status accounting, verification. Baselines identify agreed configuration at a time; do not impose NASA SETR gates on OOSEM project. 6.7 technical assessment https://www.nasa.gov/reference/6-7-technical-assessment/ supports well-defined measures, trends, variance and decision feedback, not arbitrary project margin percentages.
- Analysis credibility: NASA-STD-7009B approved 2024-03-05, full primary PDF accessible https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf . 4.1.1.1 intended use; 4.1.1.2 criticality; 4.1.1.5 V&V/uncertainty/sensitivity/assessment acceptance criteria; 4.1.1.8 defect tracking. 4.2 development, 4.3 use and 4.3.8 reporting require further section inspection. App E distinguishes model capability and results assessment. Do not call NASA-HDBK-7009B Final 02-03-2026 approved solely from filename: indexed heading said DRAFT; verify status first.
- Decision/trade: NASA handbook 6.8 https://www.nasa.gov/reference/6-8-decision-analysis/ . 6.8.1.2.1 criteria/scales/importance; .2 alternatives; .3 proportionate evaluation methods; .4 assumptions, uncertainty and defined normalization; .5 robust recommendations (retain close alternatives when uncertainty changes ranking); .7 work products; 6.8.1.3 report context, actual decision, rationale, methods, sensitivities. Do not confuse numerical sizing baseline with rig downselect.

Accessible sources are primary agency guidance or normative language/technical standards. Tailor their use and clearly distinguish agency requirements from Blue Dog policy. Paid INCOSE/ISO/ASME provisions cannot be quoted as inspected without access. Source extraction budgets still apply; keep copied/closely summarized material concise and cite exact sections. Concrete project tests/corrections are tailored applications, not universal mandated fields or thresholds.

MIL-STD-882E Change1 full primary copy retrieved from Army Safety: https://safety.army.mil/Portals/0/Documents/ON-DUTY/SYSTEMSAFETY/Standard/MIL-STD-882E-change-1.pdf . The PDF title metadata misleadingly says 882D draft, but cover and incorporated change text identify E Change1, 2023-09-27. Verify actual text and ASSIST status rather than search title metadata. Foreword says sections 3/4 mandatory if contract invokes standard with no tasks; Blue Dog has no such contractual invocation, so tailor guidance and do not assert DoD risk acceptance authority.

The current defense SE Guidebook became accessible by clicking link32 on https://www.cto.mil/sea/pg/ : https://www.cto.mil/wp-content/uploads/2026/09/SE-Guidebook-2026.pdf . September2026 approved edition (ignore stale extracted cover metadata). 6.1.8 printed126-128 inspected and added to stage1 source/checklist. Other future sections: 6.1.2 decisionanalysis102-104; 6.1.3 TPM104-112; 6.1.6 CM117-120; 6.2.3 architecture132-135; 6.2.6 verification137-138; 6.2.7 validation138; 7.18 reliability181; 7.23 systemsafety192. Read exact clauses before using.

Stage3 preparatory scope discovery while stage2 full regression runs: native query found 95 verification definitions (67 BlueDogRequirementVerification, 28 GorgeChallengeVerification). No VerificationCases::VerificationMethod metadata applications were found in current model. Native standard library methods are VerificationMethodKind::{inspect,analyze,demo,test}; VerificationMethod.kind selects that enum. VerificationCases::VerificationCase is verificationCaseDef, not PartDefinition; do not introduce a second verdict vocabulary. Current sizing projections set evidenceAccepted=false and preserve historical configuration; do not rewrite them. BlueDogSizingEvidence::Scenario and Review live in models/analyses/sizing/evidence.sysml and distinguish screening from acceptance. Evidence record helpers normalize CRLF hashes and preserve immutable manifest/source revisions. input_record can fall back to a historical baseline; evaluate that carefully during the later configuration/credibility audit rather than changing it during stage2 validation.

NASA5.3.1.2.1-.4 inspected: configuration, procedures, equipment/calibration, data and results; NASA5.4.1.2.2-.3 inspected: operational environment/users, expected/actual comparisons, anomalies and revalidation. Current defense guidebook6.2.6/6.2.7 printed137-139 inspected: planning methods, traceable test conditions, staged integration, operational validation and change impact. These are engineering guidance, not automatic adoption of defense approval gates.

Additional primary sources: NIST TN1297 (1994), section7 reporting uncertainty, https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty (coverage factor / combined uncertainty and measurement-method basis). NASA-HDBK1009A8.14-8.19 inspected: method, criteria, verification matrices, artifacts and V&V configuration; use engineering information design, not v1 stereotypes in v2. MIL882EChange1 4.3.1-4.3.8 and Task106 identify hazard/mishap, configuration/mode, controls, risk status and verification/acceptance tracking; project tailoring does not adopt DoD acceptance authorities. Latest primary R&M BOK found via official library: December2025 https://www.cto.mil/wp-content/uploads/2025/12/RM-BoK-2025-12-10-Cleared.pdf ; inspect relevant actual sections before detailed attribution.

Potential later applications (not implemented): Stage3 can add native VerificationMethod metadata to the 95 existing plans after reviewing each actual procedure (all names enumerated natively; vehicle cases67, mission28). Preserve constant inconclusive verdicts and archived false acceptance flags. A typed review-readiness predicate should establish eligibility only, never infer expert acceptance or invent new verdict kinds. Use native document queries for method/configuration/artifact matrices. Define any new interface/durability integration procedure separately from actual execution evidence. Native query metadata paths can use fully qualified definition/feature names, as existing BlueDogAudit::Deferred does. Existing native coverage negative control expects exactly one verify roundTrip occurrence, so do not duplicate its objective merely for a new table.

Later skills should continue to distinguish proposed controls from demonstrated mitigation, installed budgets from numerical allowances, and numerical baseline choice from hardware downselect. Avoid synthetic scores, unsupported safe-state/timeout selections, invented failure rates or weights and relabeling archived evidence. Hardware/evidence gaps are explicit engineering decisions, not reasons to fabricate successful audit closure.

Stage4 preparatory native facts (no skill/model implementation yet): FailureAnalysis::ReviewRow has identifier/intendedFunction, event-backed failure/cause/local/mission effects, proposedDetection, recommendedAction, ownerRole, safetyCritical and independent dispositionAccepted/actionEvidenceAccepted=false. EvidenceReference defaults Not yet available. FailureAnalysis::Review and DesignFailureReview are native library concepts; reuse them. RiskMetadata::Risk has total/technical/schedule/cost RiskLevel fields, not quantitative severity/probability; do not fabricate these as numerical risk estimates.

BlueDogDFMEA::starter currently has 12 rows, ten unresolved critical rows and twelve open actions; scopeReviewed=false, native reviewReady=false. Existing tests/test_reliability.py asserts those counts, so any justified row additions must update counts. Existing source-model causation connections are hypothetical failure chains. Third-party harm, operator retrieval, command-context faults and shared sensing/software assumptions need explicit review beyond those component rows. Harvesting and radio-only loss have conditional/current-vs-future significance; do not blindly change criticality or imply radio outage ends qualification.

Potential stage4 correction: add explicit hazard-to-configuration/mode/contributor/control/verification/disposition records and make a combined native safety-readiness assessment depend on both existing FMEA and hazard review. Do not equate a filled record with accepted risk. Proposed controls/effectiveness/acceptance remain false or unknown until evidence exists. Add distinct missing failure mechanisms only when not duplicates; preserve FM001-FM012 identities.

Reliability current code sums non-overlapping random rates plus explicit common-cause rate and gates evidence on profile/rates/constant-hazard review. Consider explicit default-false rate-partition/dependence/common-cause coverage review flags, with synthetic accepted fixture updates rather than weakening the gate. Preserve numerical targets, equations and all archived evidence. NIST primary exponential model inspected: https://itl.nist.gov/div898/handbook/apr/section1/apr161.htm . R&M BOK2025 3.2.4 printed102-103 inspected (design analyses/mission profile); MIL882EChange1 Task106.2 and4.3.4 inspected (tracking fields and control hierarchy). Use actual source text and project tailoring, not assumed DoD thresholds/acceptance authority.

Additional stage4 source inspection: NASA SE Handbook6.4 https://www.nasa.gov/reference/6-4-technical-risk-management/ sections6.4.1.2.1-.7 and risk-triplet discussion inspected (scenario/likelihood/consequence/uncertainty; mitigation triggers, monitoring, effectiveness and work products). MIL882Task106.2 lists applicability, mode, causal factor, mishap, controls, verification, owner and actual acceptance record; 4.3.4 gives design control precedence. Tailor to project, do not assign DoD RACs or acceptance authority without an adopted basis.

Potential safety implementation should preserve the native FMEA review and add a combined native assessment rather than a Python risk verdict. Hazard records can carry proposed controls and unknown/false effectiveness/disposition, with real contributor, requirement and V&V references. Scope-reviewed must stay false until coverage is actually reviewed. Native R&M guidance does not justify invented rates or scores. Current library RiskMetadata is not a quantitative hazard matrix.

Configuration/budget source research (for stage5; not yet applied): NASA SE6.5
identification, change/status accounting and verification;6.7.1.2 consistent
measures and feedback. Defense SE Guidebook2026 actual6.1.6 printed117–120 and
6.1.3 printed110–112 inspected. Distinguish current best estimate, uncertainty
contingency, threshold and remaining margin. Its illustrative contingency
percentages are examples, not project default factors. Source cover/approval
identifies September2026 despite stale PDF title metadata. Full paid EIA649 and
INCOSE handbook not inspected; use accessible primary agency guidance and mark
tailored recommendations.

Actual IC-01 findings from read-only inspection: 8W additional electronics,1.2kg
additional equipment,60Wh recovery bank and8W recovery essentials are candidate
allowances. Main electronics includes wired-wind provision separately. Recovery
battery mass is recoveryBatteryWh/batteryWhKg; do not add it again to another
mass ledger. Recording/telemetry bus assignment is explicitly unresolved. The
440Wh BlueDogCandidateEnergy calculation belongs to its archived candidate and
must not be relabeled IC-01. BlueDogEnergyExamples is illustrative and separate.

Read-only findings for stages6/7, pending their turn:

- evidence.records.input_record validates sourceHashes OR driverHashes, not both;
  input_path returns an existing workspace file without validating either. Missing
  workspace inputs silently fall back to the historical coupled baseline. Static
  CAD/polar reference data and numerical initial guesses have legitimate historical
  uses, but current generated configuration results need an explicit role and must
  not silently substitute archived design values. Inspect callers before tailoring
  stricter APIs; preserve immutable run_record and historical-source verification.
- NASA-STD7009B approved2024-03-05 inspected4.2.1.1-.9,4.3.1.1-.6,
  4.3.3,4.3.5-.8 and AppendixE. Capability assessment and run-result applicability
  are different. Unknown uncertainty can be explicitly reported; software regression
  or numerical convergence is not physical validation. No new numerical credibility
  rating is justified without an adopted project basis.
- BlueDogSailTrade::TradeAssessment still has an ordered7gate vector and generic
  qualification language. Its progressCriterion points to legProgress (legacy study
  comparison) and reliabilityCriterion to missionSuccessProbability (provisional
  should-study objective). Review mandatory-vs-comparative classification against
  authoritative requirements before using them as hard selection gates. Preserve
  all three rigs as equal contenders and fixed-camber as numerical baseline only.
- Existing decision records preserve dispositions and needed evidence but lack a
  structured question, scope, responsible role, disposition identity and reopening
  trigger. holdingEnergy currently references only future multiDayEndurance although
  the actual rationale also concerns finite mission demand. Correct supporting
  current scope without claiming that zero holding current selects a gearbox.

Additional accessible INCOSE primary source for stage5: Technical Measurement,
INCOSE-TP-2003-020-01, Version1.0,27December2005, collaborative PSM/INCOSE/industry
report by GarryRoedler and CherylJones. Official full65page PDF retrieved with
https://www.incose.org/docs/default-source/ProductsPublications/technical-measurement-guide---dec-2005.pdf?sfvrsn=4&sfvrsn=4
(single/noquery URL failed). Inspected3.2.5,6.3.3-6.3.6,6.4. Historical guidance,
not a current contractual standard: risk-relevant selection, traceable measures,
clear aggregation/data-collection basis and responsibility. Do not import its
survey counts, military thresholds or old referenced standards as project rules.

OMG SysML2.0 Part1 formal/2026-03-02 section7.23.3 and9.4.5 trade study source
inspected. Pinned native TradeStudies::TradeStudy subject is studyAlternatives;
evaluationFunction returns comparable ScalarValue; native objectives maximize/
minimize; selectOne resolves ties by first alternative. A selectedAlternative is
an analysis result, not an authorized design decision. Do not fabricate production
scores to force a selection. Test ties, missing data, hard constraints and sensitivity
where numerical comparison is actually applicable.

7009 handbook status resolved2026-10-23: official NASA NTSS record
https://standards.nasa.gov/standard/nasa/nasa-hdbk-7009 identifies revisionB,
2026-02-03,ACTIVE; its linked full175page cover and signed approval match. The
PDF retains DRAFT page headers, so do not infer status from headers alone:
https://standards.nasa.gov/system/files/tmp/NASA-HDBK-7009B_Final%2002-03-2026.pdf .
Inspected5.6.1.1-.3 (readiness, proposed/permissible use, input pedigree),AppendixC
(user guide),AppendixF (intended/permissible/proposed/accepted/actual use). Guidance,
not automatically mandatory for Blue Dog. NASA-STD7009B2024 is also ACTIVE on
NTSS; the catalog retains an older2016change-date field while the linkedB cover
and change history identify2024approval. Cite actual inspectedBdocument, do not
invent a laterBChange1technical edition from that catalog field.

SysML variability locator corrected: Part1section7.6.7 (not7.6.3) covers variations
and variants;7.6.2-.3 cover definitions/usages. Inspected examples aroundprinted43–44.
A product family variation point, named design candidate, installed serial article
and operational state are different concepts. Do not convert independent contenders
or primary/recovery paths into a runtime mode selector merely to use variation syntax.

Further stage6 caller inspection, pending implementation: geometry.section_data,
hydro.section-profile and WingPolar intentionally consume reusable archived CAD/
inviscid grid data. Make that reference-data role explicit rather than forbidding
legitimate historical physics inputs. Missing current mass/operation/uncertainty/
sizing results should fail actionably; optimization.search's old fixed-design
record is an initial guess. source_hashes currently resolves build/analysis
locations through input_path, so any stricter role handling must also cover that
path resolution and all motion/surface/wave campaign provenance calls. Existing
baseline_record/run_record remain explicit historical APIs and must preserve bytes.
Tests directly use current prepared mass/operation/resistance records, while
historical tests use baseline_record. WORK wing-geometry may lack sourceHashes;
archived geometry is manifest-registered and has original CAD sha256/units/axes.
Do not require current driver hashes to equal old archived driver names; historical
source verification checks the original revision instead. Current work records
with both sourceHashes and driverHashes must validate both, and input_path must
validate a workspace record before returning it.

Stage7 scope should include the eight BlueDogDesignDecisions records AND six
BlueDogRequirementDecisions open acceptance questions, without pretending an
acceptance question is necessarily a hardware-alternative trade. Preserve their
actual dispositions and false accepted flags. Structured question/scope/role,
criterion class, evidence basis, implementation/reopen triggers and native
alternative references should clarify decisions without inventing approval names,
weights, scores, dates or final rig/gearbox selection.

Stage6 native inventory research (still read-only while stage5 validates):38
AnalysisCaseDefinition and72AnalysisCaseUsage elements in current project roots.
These include physics screens,input exports,historical evidence reviews,synthetic
arithmetic,weather sensitivity,rule assessment,trade and readiness/failure reviews.
Use native discovery to account for all110; definition-only inventory misses most
configured/input cases. Structured use/limitation metadata may be attached centrally
with native metadata-about relationships instead of rewriting historical projections.
Group guidance may share native definitions, while case identity/subject remains
native; no generic summary should be advertised as completed physical validation.
Any new stage7 analysis must also receive appropriate use/limitation coverage.

Pinned native AnalysisRecords library was inspected in the verified source.zip.
It is explicitly NON-NORMATIVE OpenSysML vocabulary, not OMG standard library.
RecordedRun records UTC/tool/command/kind/external tools; AnalysisRun records case,
subject,checks,inputs/outputs and trade evaluations/ties. record_analyses already
uses native %record/%save and validates requested case multiplicity; do not replace
this result model. Consider a fingerprint sidecar for actual model/record hash,
source/driver hashes,full runtime revision and CLI binary hash, preserving native
records and historical archives. Native selectedAlternative/tied evaluations do not
establish an authorized design decision. Valid analysis may show a failed design;
credibility eligibility must not require the design criterion itself to pass.

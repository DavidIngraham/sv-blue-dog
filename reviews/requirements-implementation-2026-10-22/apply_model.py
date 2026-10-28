# One-time authoring record. Not idempotent; do not rerun against the changed model.
"""Apply the authorized review using the pinned parser/editor and its source spans.

The pinned editor cannot author Dependency or short-ID declarations. For those
forms, the native delete/add-comment operation supplies the exact replacement
span; authored notation is reparsed strictly with the complete model before any
file is written. No SysML parser or relationship discovery is implemented here.
"""
import csv
import json
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT, connection, model_files

HERE = Path(__file__).resolve().parent
LOG = []

def snapshot(first):
    paths = [ROOT / first, *[p for p in model_files() if p != ROOT / first]]
    return tuple((str(p), p.read_text()) for p in paths)

def commit(sources, label):
    connection().parse_sources(sources, strict=True)
    for name, content in sources:
        p = Path(name)
        if p.read_text() != content:
            p.write_text(content)
    LOG.append(label)
    print(label, flush=True)

def edit(file, operations, label):
    sources = snapshot(file)
    model = connection().parse_sources(sources, strict=True)
    editor = model.edit()
    operations(editor)
    result = editor.apply()
    changed = {d.name: d.content for d in result.documents}
    commit(tuple((n, changed.get(n, t)) for n, t in sources), label)

def replace_nodes(file, replacements, label):
    sources = snapshot(file)
    model = connection().parse_sources(sources, strict=True)
    editor = model.edit()
    for target in replacements:
        editor.delete(target)
    result = editor.apply()
    texts = dict(sources)
    for a in sorted(result.applied, key=lambda a: a.offset, reverse=True):
        # The pinned response's offsets are not reliable after preceding batch
        # deletions. Its exact old_text is the native-located declaration span.
        assert texts[a.document].count(a.old_text) == 1, a.target
        texts[a.document] = texts[a.document].replace(a.old_text, replacements[a.target], 1)
    commit(tuple((n, texts[n]) for n, _ in sources), label)

def append(file, owner, notation, label):
    sources = snapshot(file)
    model = connection().parse_sources(sources, strict=True)
    result = model.edit().add_comment(owner, 'Native authoring insertion anchor', name='implementationAnchor').apply()
    assert len(result.applied) == 1
    a = result.applied[0]
    # Native insertion supplies indentation and location in the owner's body.
    insertion = a.new_text
    start = insertion.index('comment implementationAnchor')
    end = insertion.index('*/', start) + 2
    insertion = insertion[:start] + notation + insertion[end:]
    texts = dict(sources)
    data = texts[a.document].encode()
    texts[a.document] = (data[:a.offset] + insertion.encode() + data[a.offset+a.length:]).decode()
    commit(tuple((n, texts[n]) for n, _ in sources), label)

REQ = 'models/vehicle/requirements.sysml'
VE = 'models/vehicle/verification.sysml'
append(REQ, 'BlueDogRequirements', '''requirement def <'N-004'> VegetationResilience {
        doc /* The vessel shall preserve or autonomously recover the sailing and recovery functions specified for the declared submerged-vegetation encounters. */
        comment conditions /* N-053 through N-056 define distinct passage, snag, blockage and powered-recovery cases under the declared Gorge exposure. Submerged-weed qualification excludes dense floating mats and fishing-line entanglement. No disturbance waives required safety capability or motor inhibition. */
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
    }
    requirement vegetationResilience : VegetationResilience;
    dependency vegetationEnvironmentBasis from vegetationResilience to environmentalEnvelope;
''', 'Add the separate N-004 vegetation outcome')

rows = list(csv.DictReader((HERE.parent/'requirements-audit-2026-10-22/derivation-review.csv').open()))
replacements = {}
manifest = []
for r in rows:
    if r['status'] == 'pass with stated scope':
        manifest.append(dict(relationship=r['relationship'], action='retain derivation', reason=r['reason']))
        continue
    owner, name = r['relationship'].rsplit('::',1)
    child, parent = r['derived'], r['original']
    if parent == 'BlueDogRequirements::stabilityAndFouling':
        parent = 'BlueDogRequirements::vegetationResilience'
    shared = name.startswith('sharedAcceptance')
    assurance = r['derived_id'] == 'E-205'
    if shared:
        kind = 'dependency'; source, target = parent, child
        reason = f"{r['original_id']} relies on the {r['derived_id']} rule only for events and modes within its own qualification context. The full shared rule remains independently applicable and directly verified; this dependency does not derive its other contexts."
    elif assurance:
        kind = 'dependency'; source, target = child, parent
        reason = f"{r['derived_id']} is an evidence-acceptance work product supporting {r['original_id']}; a product capability does not logically entail the assurance record."
    else:
        kind = '#refinement dependency'; source, target = child, parent
        reason = f"{r['derived_id']} specifies a detailed acceptance condition for {r['original_id']} within their stated applicability. Selected limits, mechanisms and campaign conditions remain independent allocations; refinement makes no satisfaction implication or automatic parent-coverage claim."
    if name == 'challengeNavigationSignals':
        reason = 'S-004 clarifies C-007 signal presentation during an attempt only. Its powered-recovery and stationary-mode coverage has the separate C-027 and deployment-matrix basis; those modes are not derived from attempt-only compliance.'
    if name == 'challengeTrafficResponse':
        reason = 'S-001 specifies observation, assessment and response supporting collision-free passage. Its reviewed performance envelopes are selected allocations; C-007 independently supplies navigation duties. No-contact outcome alone does not imply the assessment process.'
    notation = f'''{kind} {name} from {source} to {target} {{
        metadata workStatus : ModelingMetadata::StatusInfo {{ status = ModelingMetadata::StatusKind::open; }}
        metadata rationale : ModelingMetadata::Rationale {{ text = {json.dumps(reason)}; }}
    }}\n'''
    replacements[r['relationship']] = notation
    manifest.append(dict(relationship=r['relationship'], action=kind, source=source, target=target, reason=reason))
replace_nodes(REQ, replacements, f'Reclassify {len(replacements)} unsupported or ambiguous derivations')
(HERE/'relationship-decisions.json').write_text(json.dumps(manifest, indent=2)+'\n')

statements = {
'EnergyAwareness': 'The vessel shall maintain conservative estimates of usable battery energy and the energy required for protected recovery.',
'EnergyEstimateAccuracy': 'Across the operating battery-temperature range, the absolute difference between estimated usable energy and calibrated charge/discharge integration shall not exceed 10 percent of measured usable full-charge energy.',
'GuidanceUpdateCadence': 'During operational qualification, mission guidance shall refresh its guidance output at intervals no greater than 1 second.',
'SailCommandCadence': 'During operational qualification, sail control shall refresh the commanded sail position at intervals no greater than 1 second.',
'SteeringCommandCadence': 'During operational qualification, steering control shall refresh the commanded steering position at intervals no greater than 1 second.',
'SoloTransport': 'The vessel and its mission equipment shall be transportable for 100 m by one adult without assistance under the P-001 handling conditions.',
'SetupDuration': 'The vessel shall be capable of assembly from its transport configuration by one adult within 30 minutes under the P-001 handling conditions.',
'PackDuration': 'The vessel shall be capable of packing into its transport configuration by one adult within 30 minutes under the P-001 handling conditions.',
'SoloLaunch': 'The assembled vessel shall be launchable by one adult without assistance under the P-001 handling conditions.',
'SoloRetrieval': 'The vessel shall be retrievable from the water by one adult without assistance under the P-001 handling conditions.',
'LaunchEnergyAdmission': 'The vessel shall inhibit mission start unless a valid usable-energy estimate no older than 1 second strictly exceeds a valid R-002 protected reserve.',
'ChallengeMotorInhibition': 'The vessel shall inhibit motor thrust until it has durably recorded a known nonqualifying status for the attempt.',
'LegProgress': 'The mission-performance assessment shall evaluate complete-route progress over the declared reproducible scenario ensemble, including sailing legs, holds and maneuvers.',
'EnergyEvidenceReadiness': 'The energy-case acceptance record shall identify accepted evidence for installed-load coverage, resource bounds, battery derating and interval resolution before the case is accepted.',
'StabilityAndFouling': 'After the declared capsize disturbances, the vessel shall provide the recovery behavior defined for the selected righting or post-abort recovery strategy.',
'SafeRecovery': 'The vessel shall preserve controlled emergency intervention through abort, local motor isolation and remote-control loss.',
}
def wording(e):
    for name, text in statements.items():
        e.add_documentation('BlueDogRequirements::'+name, ' '+text+' ', replace=True)
    for target in ['GuidanceUpdateCadence','SailCommandCadence','SteeringCommandCadence']:
        e.add_comment('BlueDogRequirements::'+target, ' Observe refresh at the guidance output consumed by control, or at the actuator command input, respectively. Repeated values count as a refresh; changed values and achieved physical motion are not required by this cadence criterion. ',name='observationBoundary')
    e.add_comment('BlueDogRequirements::SelfRighting', ' N-051 incorporates N-118 RightingDeadline, N-119 CapsizeRigRetention, N-120 CapsizeBallastRetention and N-121 CapsizeElectronicsSealing for every declared release. ',name='aggregateMembers')
    e.add_comment('BlueDogRequirements::WeedSnagShedding', ' N-054 incorporates N-128 WeedSnagSpeedRecovery and N-129 WeedSnagSteeringRecovery for every declared repetition. ',name='aggregateMembers')
edit(REQ, wording, 'Apply precise requirement wording, qualification boundaries and stable aggregate membership')
sources = snapshot(REQ)
texts = dict(sources)
replacements = {
'comment conditions /* Capsize and vegetation are separate disturbance cases. Righting and upright control restoration apply to the selected N-051 strategy; C-018 also permits post-abort limp recovery. Weed passage, snag shedding and blockage response apply to the declared Gorge exposure. No disturbance waives required safety capability or motor inhibition. */': 'comment conditions /* Righting and upright control restoration apply to selected N-051/N-052 passive-righting criteria; C-018 independently permits post-abort limp recovery. No capsize waives required safety capability or motor inhibition. N-004 separately governs vegetation encounters. */',
'comment notes /* Submerged-weed passage qualification does not cover dense floating mats or fishing-line entanglement. */': '',
'comment conditions /* Emergency intervention ends attempt qualification. Exercise active emergency, powered recovery, local isolation and remote-control loss, including coexisting low-energy flags. */': 'comment conditions /* Emergency intervention ends attempt qualification. Exercise abort, local isolation and remote-control loss with coexisting low-energy flags. S-110 through S-115 define the detailed acceptance criteria; powered shore-recovery capability is independently required by R-001. */',
}
for old, new in replacements.items():
    assert texts[str(ROOT/REQ)].count(old) == 1
    texts[str(ROOT/REQ)] = texts[str(ROOT/REQ)].replace(old,new,1)
commit(tuple((n,texts[n]) for n,_ in sources), 'Author separate normative contexts through the native parser (comment-deletion API cannot preserve adjacent declarations)')

# Native rename propagates references across parsed source documents.
def names(e):
    e.rename('BlueDogRequirements::StabilityAndFouling','CapsizeResilience')
    e.rename('BlueDogRequirements::stabilityAndFouling','capsizeResilience')
    e.rename('BlueDogRequirements::SafeRecovery','EmergencyControl')
    e.rename('BlueDogRequirements::safeRecovery','emergencyControl')
edit(REQ, names, 'Rename scoped N-003 and S-003 with native reference migration')

append(REQ,'BlueDogRequirements', '''dependency navigationDutyBasis from trafficSafety to GorgeChallenge::navigationRules;
    dependency recoverySignalBasis from navigationConspicuity to GorgeChallenge::recoveryConspicuity;
    dependency signalMatrixBasis from navigationConspicuity to regulatoryClassification;
''','Record independent navigation and post-abort signal bases')
replace_nodes(REQ, {'BlueDogRequirements::deriveRecoveryPropulsion': '''dependency deriveRecoveryPropulsion from recoveryPropulsion to GorgeChallenge::autonomousShoreRecovery {
        metadata rationale : ModelingMetadata::Rationale { text = "R-001 specifies the installed powered means supporting course-dependent shore recovery. Emergency-control acceptance remains a separate S-003 obligation."; }
    }\n'''}, 'Give powered recovery its shore-recovery source')

edit(VE, lambda e: e.rename('BlueDogRequirementVerification::StabilityAndFoulingVerification','CapsizeResilienceVerification'), 'Rename the capsize verification case')
edit(VE, lambda e: e.add_documentation('BlueDogRequirementVerification::CapsizeResilienceVerification', ' Assess capsize recovery for the declared installed configuration and casualty profile. Use N-051/N-052 only for the selected passive-righting strategy; retain independent C-018 post-capsize shore recovery. Establish required safety capability, restrictions and qualification persistence during inversion and after recovery. A righting result alone cannot close N-003. ', replace=True), 'Scope capsize verification to N-003')
append(VE,'BlueDogRequirementVerification', '''verification def <'V-N-004'> VegetationResilienceVerification {
        doc /* Apply N-053 through N-056 to the same installed configuration. Assess sailing passage, appendage snag shedding, blockage response and powered recovery separately. Review subsequent control, safety capability and energy use; separate campaign results need a justified combination argument, including compatibility with capsize exposure. */
        objective acceptance { verify BlueDogRequirements::vegetationResilience; }
        return verdict : VerificationCases::VerdictKind = VerificationCases::VerdictKind::inconclusive;
    }
''','Add integrated vegetation verification without fabricated evidence')
(HERE/'applied-steps.json').write_text(json.dumps(LOG,indent=2)+'\n')

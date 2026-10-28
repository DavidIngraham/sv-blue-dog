"""Format recorded native facts and the audit's engineering judgments as ledgers.

This consumes the native snapshot. It does not parse SysML or infer new model
relationships. The decision maps below are review judgments, not model policy.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REVIEW = HERE.parent
snapshot = json.loads((HERE / 'native-review.json').read_text())

def table(name):
    t = snapshot['tables'][name]
    return [{'element': r['element']['id'], **dict(zip(t['columns'], r['cells']))} for r in t['rows']]

def text(cell):
    return '; '.join(v.get('id', str(v)) if isinstance(v, dict) else str(v) for v in cell)

reqs = table('Requirements')
defs = {r['element']: r for r in reqs}
uses = {r['element']: r for r in table('Uses')}
use_to_def = {u['element']: u['type'][0] for u in uses.values()}
bydef = {u['type'][0]: u for u in uses.values()}
deferred = {r['element'] for r in table('DeferredRequirements')}
contexts = {n: {r['element']: text(r['Text']) for r in table(n)} for n in ['Conditions', 'Notes', 'RationaleRows', 'IssueRows']}
basis_targets = {r['element'] for r in table('BasisTargets')}

def rid(use):
    return text(defs[use_to_def[use]]['ID'])

def leaf(use):
    return use.split('::')[-1]

def source_location(row):
    element = row['element']
    if element.startswith('GorgeChallenge::'): path = 'models/missions/transgorge.sysml'
    elif element.startswith('BlueDog::Goals::'): path = 'models/vehicle/architecture.sysml'
    elif element.startswith('BlueDogStructure::'): path = 'models/vehicle/structure.sysml'
    else: path = 'models/vehicle/requirements.sysml'
    needle = "requirement def <'" + text(row['ID']) + "'>"
    lines = (ROOT / path).read_text().splitlines()
    matches = [i + 1 for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1: raise ValueError((element, matches))
    return path + ':' + str(matches[0])

# An explicit incorporation is different from a convenient design breakdown.
accepted = {
    'transGorgeChallenge': '*', 'noLittering': '*', 'structuralIntegrity': '*',
    'cruisePerformance': '*', 'missionReliability': '*',
    'selfRighting': '*', 'weedSnagShedding': '*',
    'communications': {'telemetryDeliveryCadence', 'backlogCurrentPriority'},
    'transportability': {'soloLaunch', 'soloRetrieval'},
    'serviceability': {'nondestructiveService'},
    'navigationConspicuity': {'navigationLightPresentation', 'navigationShapePresentation', 'navigationSoundPresentation'},
    'regulatoryClassification': {'deploymentReleaseGate'},
    'visibility': {'visibilityNavigationCapability', 'visibilityTrafficCapability', 'restrictedVisibilityCollisionAssessment'},
    'envelopeTransition': {'sailingResumptionInhibition'},
    'solarHeating': '*',
    'recoveryPropulsorWeeds': {'poweredWeedCurrent', 'poweredWeedTemperature'},
    'sustainedEnergyFeasibility': {'sustainedReserveProtection', 'repeatableCycleBalance', 'peakSupplyCapability'},
    'multiDayEndurance': {'sustainedReserveProtection'},
    'resetRecovery': {'resetRestrictionPreservation'},
}
ambiguous = {
    'gorgeEnvironment': '*', 'oceanEnvironment': '*', 'environmentalEnvelope': '*', 'marineDurability': '*',
    'stabilityAndFouling': {'submergedWeedPassage', 'weedSnagShedding', 'weedBlockageResponse'},
    'windObservation': '*', 'wetMechanicalIntegrity': '*',
    'commandIntegrity': {'unauthenticatedCommandRejection', 'replayCommandRejection', 'expiredCommandRejection', 'externalControlDisqualification'},
    'telemetryEquipment': {'telemetryStaleIndication', 'telemetryIdentityPreservation', 'telemetryDuplicateSuppression'},
    'serviceability': {'postServiceActuation'},
    'lowEnergyRecovery': {'lowEnergyNavigationContinuity', 'lowEnergyCollisionContinuity'},
    'missionEvidence': {'criticalEventRecording', 'invalidTimestampMarking', 'logGapIndication'},
    'ingressResponse': {'ingressFlotation'},
}
accepted_reasons = {
    'transGorgeChallenge': 'C-000 expressly incorporates the numbered challenge rule; it is a deliberate aggregate contract.',
    'noLittering': 'C-015 expressly applies C-016 through C-018, including this obligation.',
    'structuralIntegrity': 'T-100 expressly applies T-101 through T-109 independently.',
    'cruisePerformance': 'Q-001 expressly applies Q-101 through Q-103. Separate the product and assessment roles without losing the incorporation.',
    'missionReliability': 'L-001 expressly applies L-103 evidence and L-104 dispositions; provisional L-101/L-102 are excluded.',
    'selfRighting': 'N-051 expressly says all leaves apply to every defined release. Keep only with an explicit, stable aggregate leaf set.',
    'weedSnagShedding': 'N-054 expressly applies both leaf criteria to every repetition. Make that two-element aggregate explicit.',
}

def contains(mapping, parent, child):
    return mapping.get(parent) == '*' or child in mapping.get(parent, set())

derivations = []
for r in table('Derivations'):
    original = r['Original'][0]['id']
    derived = r['Derived'][0]['id']
    parent, child = leaf(original), leaf(derived)
    if contains(accepted, parent, child):
        status = 'pass with stated scope'
        finding = 'F04' if parent in {'transGorgeChallenge', 'noLittering', 'structuralIntegrity', 'selfRighting', 'weedSnagShedding', 'cruisePerformance', 'missionReliability'} else ''
        reason = accepted_reasons.get(parent, 'The parent statement or normative conditions explicitly cover this outcome or bound in the same selected scope; no added numerical allocation is inferred.')
        action = 'Retain this implication under the recorded conditions. Keep aggregate membership explicit where applicable; do not infer reverse coverage.'
    elif contains(ambiguous, parent, child):
        status, finding = 'unresolved meaning', 'F04'
        reason = 'The parent uses a profile, applicable-criterion, integrity or shared-function term whose intended incorporation of this complete child is not explicit enough to establish the implication.'
        action = 'Name the exact incorporated criterion and subject/profile, or replace with detailed-to-general refinement/basis dependency. Preserve the child and its limits.'
    else:
        status, finding = 'fail implication', 'F01'
        reason = 'The child adds a selected bound, mechanism, reporting effect or assurance obligation that is not established by the parent statement and its normative conditions.'
        action = 'Preserve the child. Replace this implication with a justified refinement from child to parent, or a child-to-basis dependency for a selected mechanism/assurance obligation.'
        if r['element'].split('::')[-1].startswith('sharedAcceptance'):
            finding = 'F02'
            reason = 'The shared child includes independent events, modes or complete-obligation scope beyond the source-specific behavior; common verification does not establish this implication.'
            action = 'Retain one normative shared requirement. Use a scoped dependency/coverage explanation and verify both obligations explicitly; do not derive the complete shared requirement from this narrower source.'
        if parent in {'trafficCoexistence', 'navigationRules'} or parent == 'challengeMotorInhibition':
            finding = 'F03'
            reason = 'Outcome compliance or qualification classification does not entail the added implementation or broader operating-mode obligation.'
        if child == 'energyEvidenceReadiness':
            finding = 'F07'
            reason = 'Product energy capability does not logically establish acceptance of its evidence. This is an assessment-process obligation.'
    derivations.append({'relationship': r['element'], 'kind': 'derivation', 'original': original,
        'original_id': rid(original), 'derived': derived, 'derived_id': rid(derived),
        'status': status, 'finding': finding, 'reason': reason,
        'original_statement': text(defs[use_to_def[original]]['Statement']),
        'original_conditions': contexts['Conditions'].get(use_to_def[original], ''),
        'derived_statement': text(defs[use_to_def[derived]]['Statement']),
        'proposed_action': action})

def write_csv(name, rows):
    with (REVIEW / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

write_csv('derivation-review.csv', derivations)

refs = {r['element'] for r in table('AllRefinements')}
dep_rows = []
for r in table('AllDependencies'):
    refined = r['element'] in refs
    assert r['Client'] and r['Supplier'], r['element']
    dep_rows.append({'relationship': r['element'], 'kind': 'refinement' if refined else 'plain dependency',
        'client': text(r['Client']), 'supplier': text(r['Supplier']),
        'status': 'pass relationship meaning',
        'scope': 'Clarifies the target representation; does not imply physical compliance or complete coverage.' if refined else 'Supporting basis, scope, motivation or change dependence; no requirement-satisfaction implication.',
        'rationale': text(r['Rationale']), 'proposed_action': 'Retain type and direction; keep evidence/configuration scope explicit.'})
write_csv('dependency-review.csv', dep_rows)

allocation_rows = []
for r in table('AllAllocationSources'):
    for target in r['Targets']:
        allocation_rows.append({'source': r['element'], 'target': target['id'],
            'status': 'pass responsibility mapping',
            'scope': 'Scenario/executable behavior to logical responsibility, logical responsibility to candidate physical realization, or human task to operator.',
            'limitation': 'Does not establish functional completeness, independent power/control, physical realization or verification.',
            'proposed_action': 'Retain allocation; resolve installed independence and coverage through the declared configuration/evidence plans (U02).',})
write_csv('allocation-review.csv', allocation_rows)

wording_flags = {
    'C-005': 'F05', 'C-007': 'F05', 'N-003': 'F04;F05', 'S-003': 'F05',
    'P-101': 'F06', 'P-103': 'F06', 'P-104': 'F06', 'P-105': 'F06', 'P-106': 'F06',
    'E-103': 'F06', 'E-105': 'F06', 'E-106': 'F06', 'E-107': 'F06', 'R-003': 'F06', 'R-004': 'F03;F06',
    'Q-101': 'F07', 'Q-103': 'F07', 'L-103': 'F07', 'L-104': 'F07', 'E-205': 'F07',
    'S-005': 'F07', 'S-122': 'F07', 'S-123': 'F07',
}
claim_scope_flags = {'P-003', 'N-045'}
process_ids = {'Q-101','Q-103','L-103','L-104','E-205','S-005','S-122','S-123'}
objective_ids = {'C-002','L-101','L-102'}
parent_uses = {r['original'] for r in derivations}
rows_out = []
for r in reqs:
    element, ident = r['element'], text(r['ID'])
    u = bydef[element]
    relevant = [d for d in derivations if d['original'] == u['element'] or d['derived'] == u['element']]
    finding_ids = sorted(set(filter(None, wording_flags.get(ident, '').split(';'))) |
                         {d['finding'] for d in relevant if d['finding']} |
                         ({'F07'} if ident in claim_scope_flags or ident == 'Q-102' else set()))
    role = 'assessment/process obligation' if ident in process_ids else 'nonbinding objective' if ident in objective_ids else 'higher-level outcome/aggregate' if u['element'] in parent_uses else 'product or qualification obligation'
    active = 'deferred future mission/profile' if element in deferred else 'current/shared; selected configuration and conditions govern'
    verifiers, satisfiers = text(u['Verifiers']), text(u['Satisfiers'])
    if not verifiers and element not in deferred: raise ValueError(('missing current verifier', element))
    rows_out.append({'id': ident, 'element': element, 'location': source_location(r),
        'applicability': active, 'role': role, 'statement': text(r['Statement']),
        'conditions': contexts['Conditions'].get(element, ''),
        'wording_review': 'proposed correction: ' + wording_flags[ident] if ident in wording_flags else 'reviewed; no additional wording defect identified',
        'source_review': 'explicit challenge rule/goal' if element.startswith(('GorgeChallenge::','BlueDog::Goals::')) else 'basis metadata recorded; numerical/physical justification remains an engineering review item (F08/U01)' if element in basis_targets else 'reviewed through normative context and native upstream/basis relationships; no invented parent required',
        'hierarchy_relationship_findings': ';'.join(finding_ids),
        'acceptance_feasibility': 'unresolved future mission allocation' if element in deferred else 'planned acceptance meaning reviewed; installed evidence/criteria release remains open where identified in U01-U06',
        'verification_links': verifiers or 'deferred; no direct planned case',
        'satisfaction_claims': satisfiers or ('process ownership/assessment, not component satisfaction' if ident in process_ids else 'no direct claim; see traceability discussion'),
        'satisfaction_review': 'unresolved whole-obligation scope: F07; distinguish a responsible component from a claim that it satisfies all cases' if ident in claim_scope_flags else 'candidate engineering claim only; retain the subject/configuration and evidence limits' if satisfiers else 'absence reviewed by role and applicability; do not invent a component claim',
        'recorded_issue': contexts['IssueRows'].get(element, ''),
        'proposed_action': 'Apply cited findings while preserving IDs, policy and numerical limits; resolve applicable U01-U06 evidence gates.' if finding_ids else 'Retain the obligation; complete its declared configuration-specific acceptance evidence before claiming compliance.'})
write_csv('requirement-review.csv', rows_out)

verification_rows = []
for r in table('AllVerification'):
    special = r['element'] == 'BlueDogReliability::VoyageReliabilityVerification'
    exposure = r['element'] in {'BlueDogRequirementVerification::AirTemperatureVerification', 'BlueDogRequirementVerification::WaterTemperatureVerification', 'BlueDogRequirementVerification::HumidityVerification'}
    verification_rows.append({'case': r['element'], 'verifies': text(r['Verifies']),
        'specification': text(r['documentation']), 'review': 'F07: shared verdict combines provisional study objectives and current performance/evidence objectives; retain aggregate scope or report per-objective results' if special else 'F08: justify exposure durations/cycles and their coverage of the parent operational envelope' if exposure else 'planned objective links and specification reviewed',
        'evidence_limit': 'A defined case is not an executed or accepted physical verdict. Software regression and conditional analysis remain separately scoped.',
        'proposed_action': 'Retain direct objectives when correcting hierarchy; record configuration, procedure, observations and review disposition.'})
write_csv('verification-review.csv', verification_rows)

summary = {'requirements': len(rows_out), 'derivations': dict(Counter(d['status'] for d in derivations)),
    'dependencies': len(dep_rows), 'refinements': len(refs), 'allocations': len(allocation_rows),
    'verification_definitions': len(verification_rows),
    'current_requirements_without_direct_verification': 0,
    'deferred_without_direct_verification': [r['id'] for r in rows_out if r['verification_links'].startswith('deferred')],
    'missing_direct_satisfaction': [r['id'] for r in rows_out if not bydef[r['element']]['Satisfiers']]}
(HERE / 'ledger-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))

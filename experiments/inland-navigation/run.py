"""Transport fixtures to native SysML; no navigation decisions are implemented here."""
from pathlib import Path
import hashlib
import json
import sys
from fractions import Fraction
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from opensysml import EnumLiteral
from tools.boat_analysis.model.runtime import connection
from tools.boat_analysis.model.install import RELEASE

HERE = Path(__file__).resolve().parent
@lru_cache(maxsize=16)
def input_types(model, analysis="InlandNavigationExperiment::Assess"):
    return {s.name: s.type_facts for s in model.find(analysis).children()
            if s.metadata.get('direction') == 'in'}

def load():
    return connection().parse_sources(tuple((str(HERE/n), (HERE/n).read_text()) for n in ['navigation.sysml', 'extended.sysml']), strict=True)

def decode(value):
    if isinstance(value, EnumLiteral):
        return value.literal_id.rsplit('::', 1)[-1]
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, dict):
        return {k: decode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [decode(v) for v in value]
    return value

def assess(model, inputs, analysis="InlandNavigationExperiment::Assess"):
    interface = input_types(model, analysis)
    if set(inputs) != set(interface):
        raise ValueError('Provide every declared input exactly once')
    args = {}
    for name, kind in interface.items():
        value = inputs[name]
        if kind.resolved_kind == 'enumDef':
            enum = kind.resolved_id
            value = EnumLiteral(enum + '::' + value, enum)
        args[name] = value
    result = model.run_analysis(analysis,
        subject=analysis.rsplit('::', 1)[0]+'::context', named_arguments=args)
    if not result:
        raise RuntimeError(str(result))
    return decode(result.outputs)

def execute_case(model, fixture, case):
    memory = fixture['base'].get('previousMemory')
    records = []
    for step in case.get('steps', [case]):
        inputs = dict(fixture['base'], **case.get('shared', {}))
        if memory is not None:
            inputs['previousMemory'] = memory
        inputs.update(step.get('inputs', {}))
        outputs = assess(model, inputs, fixture.get("analysis", "InlandNavigationExperiment::Assess"))
        for key, expected in step['expect'].items():
            assert outputs[key] == expected, (case['name'], key, outputs[key], expected)
        assert outputs['completeComplianceEstablished'] is False
        records.append(dict(inputs=inputs, expected=step['expect'], outputs=outputs))
        memory = outputs.get('nextMemory')  # All transition semantics live in SysML.
    return dict(name=case['name'], steps=records)

def compose_candidate(model, frames, assurance):
    """Wire native results into the native conjunction; no rule decisions here.

    This experiment checks one fixture/installation case. Complete installed
    equipment coverage remains an explicit applicability/evidence assessment.
    """
    results = {name: assess(model, inputs, name) for name, inputs in frames.items()}
    mapping = {
        "generalSupported": ("InlandExtended::General", "assessmentSupported"),
        "pairwiseSupported": ("InlandNavigationExperiment::Assess", "selectionSupported"),
        "restrictedVisibilitySupported": ("InlandExtended::RestrictedVisibility", "candidateSupported"),
        "channelSupported": ("InlandExtended::ChannelsAndTSS", "channelSupported"),
        "tssSupported": ("InlandExtended::ChannelsAndTSS", "tssSupported"),
        "signalsSupported": ("InlandExtended::Signals", "candidateSupported"),
        "displaySupported": ("InlandExtended::LightsAndShapes", "displayEvidenceSupported"),
        "fixturesSupported": ("InlandExtended::LightFixture", "fixtureSupported"),
        "installationSupported": ("InlandExtended::Installation", "installationSupported"),
        "soundSupported": ("InlandExtended::SoundAppliance", "equipmentSupported"),
        "specialCasesSupported": ("InlandExtended::ExemptionsAndSpecialCases", "assessmentSupported"),
    }
    mapping.update(specialDisplaysSupported=('InlandExtended::SpecialDisplays', 'displayAlternativeSupported'),
        passageProtocolSupported=('InlandExtended::PassageProtocol', 'protocolSupported'),
        distressCatalogSupported=('InlandExtended::DistressCatalog', 'useSupported'))
    inputs = {key: results[name][output] for key, (name, output) in mapping.items()}
    if set(assurance) != {'additionalApplicableClausesReviewed'}:
        raise ValueError('Assurance may only supply additionalApplicableClausesReviewed')
    inputs.update(assurance)
    core = frames['InlandNavigationExperiment::Assess']
    channel = frames['InlandExtended::ChannelsAndTSS']
    visibility = frames['InlandExtended::RestrictedVisibility']
    lights = frames['InlandExtended::LightsAndShapes']
    signals = frames['InlandExtended::Signals']
    protocol = frames['InlandExtended::PassageProtocol']
    signal_result = results['InlandExtended::Signals']
    shared = dict(signalExchangeRequired=signal_result['maneuverSignalRequired'] or signal_result['answerSameSignalRequired'] or signal_result['precautionUntilAgreementRequired'],
        protocolExchangeRequired=protocol['requiredExchange'],
        signalAgreement=signals['passingAgreementReached'],
        protocolAgreement=results['InlandExtended::PassageProtocol']['currentAgreement'],
        coreAgreement=core['passageAgreement'], coreLengthM=core['ownLengthM'], channelLengthM=channel['lengthM'],
        lightLengthM=lights['lengthM'], fixtureLengthM=frames['InlandExtended::LightFixture']['lengthM'],
        installationLengthM=frames['InlandExtended::Installation']['lengthM'],
        soundLengthM=frames['InlandExtended::SoundAppliance']['lengthM'], signalLengthM=signals['lengthM'],
        specialLengthM=frames['InlandExtended::ExemptionsAndSpecialCases']['lengthM'],
        coreSight=core['inSight'], visibilitySight=visibility['inSight'], signalSight=signals['inSight'],
        coreRisk=core['riskOfCollision'], generalRisk=frames['InlandExtended::General']['riskAssessment'],
        visibilityRisk=visibility['risk'], coreChannel=core['channelContext'], channel=channel['channel'],
        coreConfined=core['otherConfinedToChannel'], confined=channel['otherConfined'],
        coreCrossing=core['crossingChannel'], crossing=channel['crossingChannel'],
        coreNavigatingChannel=core['otherNavigatingChannel'], navigatingChannel=channel['otherNavigatingChannel'],
        coreKind=core['ownKind'], lightMode=lights['mode'], signalMode=signals['mode'],
        sailAlsoPowered=lights['sailAlsoPowered'],
        generalRiskPresent=results['InlandExtended::General']['rule7RiskPresent'],
        coreRestricted=core['restrictedVisibility'], lightRestricted=lights['restrictedVisibility'],
        signalRestricted=signals['restrictedVisibility'], visibilityRestricted=visibility['inOrNearRestricted'])
    consistency = assess(model, shared, 'InlandExtended::SnapshotConsistency')
    results['InlandExtended::SnapshotConsistency'] = consistency
    inputs['factsConsistent'] = consistency['consistent']
    inputs['inSight'] = visibility['inSight']
    inputs['inOrNearRestricted'] = visibility['inOrNearRestricted']
    results["InlandExtended::CandidateAssessment"] = assess(model, inputs, "InlandExtended::CandidateAssessment")
    return results

def main():
    fixture = json.loads((HERE / 'cases.json').read_text())
    model = load()
    cases = [execute_case(model, fixture, c) for c in fixture['cases']]
    extended = json.loads((HERE / 'extended-cases.json').read_text())
    for suite in extended['suites']:
        cases.extend(execute_case(model, suite, c) for c in suite['cases'])
    files = ['navigation.sysml', 'extended.sysml', 'cases.json', 'extended-cases.json', 'run.py']
    record = dict(kind='Synthetic rule-interpretation regression; not navigation qualification',
        toolchain=RELEASE, modelScope='Only experiments/inland-navigation/*.sysml',
        sourceSha256={n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in files},
        scenarioCount=len(cases), evaluationCount=sum(len(c['steps']) for c in cases), cases=cases)
    (HERE / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
    print(f"{record['scenarioCount']} scenarios, {record['evaluationCount']} native evaluations passed")

if __name__ == '__main__':
    main()

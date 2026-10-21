"""Named configuration authority, native numerical controls and inspectable execution."""
import json
import pytest

from tools.boat_analysis.evidence.records import run_record, validate
from tools.boat_analysis.model.runtime import ROOT, analysis_values, load_model, model_files, numerical_value
from tools.boat_analysis.mission.integrated_sizing import named_configuration


def test_named_ic01_preserves_the_complete_archived_design():
    values, design = named_configuration()
    archive = run_record(ROOT/'evidence/runs/2026-10-15-integrated-candidate', 'integrated-sizing.json')
    assert values['identifier'] == 'IC-01'
    assert design == archive['design']
    assert len(design) == 29
    assert values['recoveryDepartureWh'] == pytest.approx(43.2)
    assert values['independentRecoveryAssumed'] is True


def test_named_design_can_load_without_reading_archived_results(monkeypatch):
    from tools.boat_analysis.mission import integrated_sizing
    def forbidden(*args, **kwargs):
        raise AssertionError('Archived output must not supply current design properties')
    monkeypatch.setattr(integrated_sizing, 'run_record', forbidden)
    assert integrated_sizing.named_configuration()[1]['battery_Wh'] == 1300


def test_native_recovery_cases_distinguish_reserve_and_route_limits():
    prefix = 'BlueDogIntegratedCandidate::'
    nominal = analysis_values(prefix+'IC01RecoveryIllustration')
    inverted = analysis_values(prefix+'IC01InvertedRecoveryIllustration')
    impossible = analysis_values(prefix+'IC01NoRecoveryAuthority')
    assert nominal['remainingWh'] == 43
    assert nominal['requiredWh'] == pytest.approx(12.545454545454543)
    assert nominal['routeFeasible'] and nominal['reserveFits']
    assert inverted['requiredWh'] == pytest.approx(98)
    assert inverted['routeFeasible'] and not inverted['reserveFits']
    assert not impossible['routeFeasible'] and not impossible['reserveFits']
    assert all(row['physicalQualification'] is False for row in (nominal, inverted, impossible))


def test_configuration_mutation_changes_native_inputs_and_recovery_result(tmp_path):
    original = ROOT/'models/configurations/ic01.sysml'
    altered = tmp_path/'ic01.sysml'
    source = original.read_text()
    assert 'attribute recoveryBatteryWh : Real = 60;' in source
    source = source.replace('attribute recoveryBatteryWh : Real = 60;',
                            'attribute recoveryBatteryWh : Real = 10;')
    source = source.replace('attribute :>> battery_Wh = 1300;', 'attribute :>> battery_Wh = 900;')
    altered.write_text(source)
    model = load_model(tuple(p for p in model_files() if p != original)+(altered,))
    inputs = numerical_value(model.run_analysis('BlueDogIntegratedCandidate::Inputs').outputs)
    design = dict(zip(inputs['designNames'],inputs['designValues'],strict=True))
    result = model.run_analysis('BlueDogIntegratedCandidate::IC01RecoveryIllustration')
    assert design['battery_Wh'] == 900
    assert result.outputs['mainNameplateWh'] == 900
    assert float(result.outputs['remainingWh']) == pytest.approx(7)
    assert result.outputs['reserveFits'] is False


def test_recovery_screen_rejects_negative_exposure():
    result = load_model().run_analysis('BlueDogIntegratedCandidate::RecoveryScreen',
        named_arguments=dict(exposureHours=-1, distanceM=600,
        alongCurrentMps=-.4, crossCurrentMps=0, inverted=False))
    assert not result


def test_ic01_recovery_screen_rejects_an_alternate_configuration():
    result = load_model().run_analysis('BlueDogIntegratedCandidate::RecoveryScreen',
        subject='BlueDogConfigurations::reference', named_arguments=dict(exposureHours=4,
        distanceM=600, alongCurrentMps=-.4, crossCurrentMps=0, inverted=False))
    assert not result
    assert result.outputs['configurationApplicable'] is False
    assert result.outputs['reserveFits'] is False


def test_named_demonstration_links_native_arithmetic_to_recovery_policy(tmp_path):
    from tools.boat_analysis.mission.demonstration import run, CASES
    output = tmp_path/'demo.json'
    report = run(output)
    assert json.loads(output.read_text()) == report
    validate(report['sourceHashes'])
    assert report['configuration'] == 'BlueDogIC01::design'
    assert report['physicalQualification'] is False
    assert report['runtimeRevision'].startswith('23ca2e2f0')
    assert set(report['nativeAnalyses']) == set(CASES)
    traces = report['behaviorTraces']
    safe = traces['safeUnassistedRighting']
    assert any(r['outputs'].get('mode') == 'capsized_drift' for r in safe)
    assert safe[-1]['outputs']['sailingPermitted'] is True
    compound = traces['capsizeReserveThreatAndCommunicationLoss']
    assert any(r['outputs'].get('alert') == 'queue' for r in compound)
    assert compound[-1]['outputs']['abortLatchedNext'] is True
    assert compound[-1]['outputs']['sailingPermitted'] is False
    recovery = traces['recoveryFromNativeReserveScreens']
    assert recovery[CASES[0]][-1]['outputs']['attemptRecovery'] is True
    assert recovery[CASES[1]][-1]['outputs']['attemptRecovery'] is False
    assert recovery[CASES[2]][-1]['outputs']['attemptRecovery'] is False
    repeated = run()
    assert repeated['nativeOutputs'] == report['nativeOutputs']
    assert repeated['behaviorTraces'] == report['behaviorTraces']

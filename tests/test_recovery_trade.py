"""Native recovery trade analysis regressions; synthetic inputs, not boat evidence."""
import json
import pytest
from scripts.render_requirements import native_recovery_trade


def check_values(check):
    return {item['name']: item['value'] for item in check['values']}

@pytest.fixture
def variant(run_model):
    def variant(base, bindings):
        source = ('package TradeTest { private import SI::*; '
                  f'part candidate :> RecoveryPropulsionTrade::{base} {{ ' +
                  ' '.join(f'attribute :>> {key} = {value};' for key, value in bindings.items()) + ' } }')
        return run_model(source, '-instantiate', 'TradeTest::candidate', '-analysis',
                         'RecoveryPropulsionTrade::RecoverySizing TradeTest::candidate')

    return variant


def test_example_outputs_and_unproven_gates():
    report = json.loads(native_recovery_trade())
    for check, power, reserve in zip(report['checks'], [20.251485657, 97.59826589], [130143.209019, 297212.254322]):
        values = check_values(check)
        assert float(values['electricalPower'].split()[0]) == pytest.approx(power, rel=0, abs=5e-06)
        assert float(values['requiredReserve'].split()[0]) == pytest.approx(reserve, rel=0, abs=5e-05)
        assert values['energyFits'] == 'true'
        assert values['modeledGatesMet'] == 'false'

def test_insufficient_reserve_fails_objective(variant):
    code, report = variant('airExample', {'availableReserve': '100 [J]'})
    assert code == 1
    assert check_values(report['checks'][0])['energyFits'] == 'false'

@pytest.mark.parametrize("bindings", [
    {'diskDiameter': '0 [m]'}, {'overallEfficiency': '1.1'},
    {'axialInflow': '-1 [m/s]'}, {'density': '-1 [kg/m^3]'},
], ids=['zero-diameter', 'invalid-efficiency', 'negative-inflow', 'negative-density'])
def test_invalid_inputs_are_not_accepted(variant, bindings):
    code, report = variant('waterExample', bindings)
    assert not report['diagnostics'], 'Invalid-input test must reach execution, not fail parsing'
    assert code != 0
    assert report['status'] != 'holds'


def test_static_reference_and_diameter_sensitivity(variant):
    code, report = variant('airExample', {'axialInflow': '0 [m/s]', 'overallEfficiency': '1'})
    assert code == 0
    assert float(check_values(report['checks'][0])['idealPower'].split()[0]) == pytest.approx(32.239404774, rel=0, abs=5e-07)
    code, report = variant('airExample', {'diskDiameter': '0.5 [m]', 'axialInflow': '0 [m/s]', 'overallEfficiency': '1'})
    assert code == 0
    assert float(check_values(report['checks'][0])['idealPower'].split()[0]) == pytest.approx(32.239404774 / 2, rel=0, abs=5e-07)

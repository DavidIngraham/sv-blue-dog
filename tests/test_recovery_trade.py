"""Native recovery trade analysis regressions; synthetic inputs, not boat evidence."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.install_renderer import binary_path
from scripts.render_requirements import MODELS, native_recovery_trade


class RecoveryTradeTests(unittest.TestCase):
    @staticmethod
    def values(check):
        return {item['name']: item['value'] for item in check['values']}

    def variant(self, base, bindings):
        source = ('package TradeTest { private import SI::*; '
                  f'part candidate :> RecoveryPropulsionTrade::{base} {{ ' +
                  ' '.join(f'attribute :>> {key} = {value};' for key, value in bindings.items()) + ' } }')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'variant.sysml'
            path.write_text(source, encoding='utf-8')
            result = subprocess.run([str(binary_path()), *map(str, MODELS), str(path),
                '-instantiate', 'TradeTest::candidate', '-analysis',
                'RecoveryPropulsionTrade::RecoverySizing TradeTest::candidate', '-json'],
                capture_output=True, text=True, encoding='utf-8')
        return result.returncode, json.loads(result.stdout)

    def test_example_outputs_and_unproven_gates(self):
        report = json.loads(native_recovery_trade())
        for check, power, reserve in zip(report['checks'], [20.251485657, 97.59826589], [130143.209019, 297212.254322]):
            values = self.values(check)
            self.assertAlmostEqual(float(values['electricalPower'].split()[0]), power, places=5)
            self.assertAlmostEqual(float(values['requiredReserve'].split()[0]), reserve, places=4)
            self.assertEqual(values['energyFits'], 'true')
            self.assertEqual(values['modeledGatesMet'], 'false')

    def test_insufficient_reserve_fails_objective(self):
        code, report = self.variant('airExample', {'availableReserve': '100 [J]'})
        self.assertEqual(code, 1)
        self.assertEqual(self.values(report['checks'][0])['energyFits'], 'false')

    def test_invalid_inputs_are_not_accepted(self):
        for bindings in ({'diskDiameter': '0 [m]'}, {'overallEfficiency': '1.1'},
                         {'axialInflow': '-1 [m/s]'}, {'density': '-1 [kg/m^3]'}):
            with self.subTest(bindings=bindings):
                code, report = self.variant('waterExample', bindings)
                self.assertFalse(report['diagnostics'], 'Invalid-input test must reach execution, not fail parsing')
                self.assertNotEqual(code, 0)
                self.assertNotEqual(report['status'], 'holds')

    def test_static_reference_and_diameter_sensitivity(self):
        code, report = self.variant('airExample', {'axialInflow': '0 [m/s]', 'overallEfficiency': '1'})
        self.assertEqual(code, 0)
        self.assertAlmostEqual(float(self.values(report['checks'][0])['idealPower'].split()[0]), 32.239404774, places=6)
        code, report = self.variant('airExample', {'diskDiameter': '0.5 [m]', 'axialInflow': '0 [m/s]', 'overallEfficiency': '1'})
        self.assertEqual(code, 0)
        self.assertAlmostEqual(float(self.values(report['checks'][0])['idealPower'].split()[0]), 32.239404774 / 2, places=6)

"""Native energy accounting regressions; no Python implementation of the model."""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.install_renderer import binary_path
from scripts.render_requirements import MODELS, native_energy_case


class EnergyTests(unittest.TestCase):
    @staticmethod
    def values(check):
        return {v['name']: v['value'] for v in check['values']}

    def run_case(self, body='', base='BlueDogEnergyExamples::campaign', extra='', analysis='SustainedOperation'):
        source = ('package EnergyTest { private import SI::*; ' + extra +
                  f'part candidate :> {base} {{ {body} }} }}')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'energy-test.sysml'
            path.write_text(source, encoding='utf-8')
            result = subprocess.run([str(binary_path()), *map(str, MODELS), str(path),
                '-instantiate', 'EnergyTest::candidate', '-analysis',
                f'BlueDogEnergy::{analysis} EnergyTest::candidate', '-json'],
                capture_output=True, text=True, encoding='utf-8')
        report = json.loads(result.stdout)
        self.assertFalse([d for d in report['diagnostics'] or [] if d['pass'] != 'runtime'],
                         'Test must reach execution, not fail parsing or resolution')
        return result.returncode, report, self.values(report['checks'][0]) if report['checks'] else {}

    @staticmethod
    def numbers(sequence):
        return [float(n) for n in re.findall(r'(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?) \[', sequence)]

    def test_rollup_and_synthetic_campaign(self):
        report = json.loads(native_energy_case())
        budget, case = map(self.values, report['checks'])
        self.assertAlmostEqual(float(budget['averageDemand'].split()[0]), 6.38825)
        self.assertAlmostEqual(float(budget['coincidentPeak'].split()[0]), 31.433333333)
        self.assertEqual(case['modeledEnergyFeasible'], 'true')
        self.assertEqual(case['energyCaseSupported'], 'false')
        self.assertEqual(case['evidenceReady'], 'false')
        self.assertEqual(case['harvestHoursPerDay'], '[6.0, 6.0, 6.0]')
        history = self.numbers(case['energyHistory'])
        self.assertEqual(len(history), 7)
        self.assertAlmostEqual(history[1], 186750.0)
        self.assertAlmostEqual(history[-1], 720000.0)
        self.assertLessEqual(max(history), 720000.0)

    def test_overnight_failure_despite_recovered_final_energy(self):
        code, _, v = self.run_case('attribute :>> initialEnergy = 630000 [J];')
        self.assertEqual(code, 1)
        self.assertEqual(v['repeatableBalance'], 'true')
        self.assertEqual(v['reserveProtected'], 'false')
        self.assertEqual(v['modeledEnergyFeasible'], 'false')

    def test_no_harvest_exhausts_storage(self):
        body = ' '.join(f'part redefines harvest{i} {{ attribute :>> harvestEnabled = false; }}' for i in range(1, 4))
        code, _, v = self.run_case(body)
        self.assertEqual(code, 1)
        self.assertEqual(v['reserveProtected'], 'false')
        self.assertEqual(v['repeatableBalance'], 'false')
        # Negative balance is exposed as a deficit, not clipped to a reassuring zero.
        self.assertLess(self.numbers(v['energyHistory'])[-1], 0)

    def test_charge_rate_limit_cannot_hide_behind_available_solar(self):
        code, _, v = self.run_case('part redefines battery { attribute :>> maxChargePower = 1 [W]; }')
        self.assertEqual(code, 1)
        self.assertEqual(v['repeatableBalance'], 'false')

    def test_peak_supply_is_independent_of_average_energy(self):
        code, _, v = self.run_case('part redefines battery { attribute :>> maxDischargePower = 10 [W]; }')
        self.assertEqual(code, 1)
        self.assertEqual(v['repeatableBalance'], 'true')
        self.assertEqual(v['reserveProtected'], 'true')
        self.assertEqual(v['peakSupported'], 'false')

    def test_enabled_zero_resource_still_counts_against_campaign(self):
        code, _, v = self.run_case('part redefines dark1 { attribute :>> harvestEnabled = true; }')
        self.assertEqual(code, 1)
        self.assertEqual(v['campaignCovered'], 'false')
        self.assertEqual(v['harvestHoursPerDay'], '[24.0, 6.0, 6.0]')

    def test_invalid_input_and_missing_input_do_not_pass(self):
        for body in ['part redefines battery { attribute :>> usableFraction = 1.1; }',
                     'part redefines dark1 { attribute :>> duration = -1 [s]; }',
                     'attribute :>> initialEnergy = 720001 [J];']:
            with self.subTest(body=body):
                code, report, _ = self.run_case(body)
                self.assertNotEqual(code, 0)
                self.assertNotEqual(report['status'], 'holds')
        code, report, _ = self.run_case(base='BlueDogEnergy::Scenario')
        self.assertEqual(code, 2)
        self.assertNotEqual(report['status'], 'holds')

    def test_mode_change_and_component_growth_are_rolled_up(self):
        extra = '''part heavy :> BlueDogEnergyExamples::sailing {
            part additionalLoad :> loads {
                attribute :>> label = "Extra load";
                attribute :>> activePower = 100 [W];
                attribute :>> idlePower = 100 [W];
                attribute :>> activeFraction = 1;
                attribute :>> conversionEfficiency = 1;
                attribute :>> uncertaintyFactor = 1;
            }
        }'''
        code, _, v = self.run_case('part redefines dark1 { ref part :>> budget = heavy; }', extra=extra)
        self.assertEqual(code, 1)
        self.assertEqual(v['reserveProtected'], 'false')
        self.assertEqual(v['peakSupported'], 'false')

    def test_surviving_finite_run_does_not_establish_repeatability(self):
        body = ('part redefines battery { attribute :>> nominalEnergy = 9000000 [J]; } '
                'attribute :>> initialEnergy = 3600000 [J]; ' +
                ' '.join(f'part redefines harvest{i} {{ attribute :>> rawHarvestPower = 20 [W]; }}' for i in range(1, 4)))
        code, _, v = self.run_case(body)
        self.assertEqual(code, 1)
        self.assertEqual(v['reserveProtected'], 'true')
        self.assertEqual(v['repeatableBalance'], 'false')

    def test_verification_requires_evidence_and_numerical_success(self):
        code, _, v = self.run_case(analysis='SustainedEnergyVerification')
        self.assertNotEqual(code, 0)
        self.assertEqual(v['verdict'], 'VerdictKind::inconclusive')
        code, _, v = self.run_case('attribute :>> evidenceAccepted = true;', analysis='SustainedEnergyVerification')
        self.assertEqual(code, 0)
        self.assertEqual(v['verdict'], 'VerdictKind::pass')
        code, _, v = self.run_case('attribute :>> evidenceAccepted = true; attribute :>> initialEnergy = 630000 [J];', analysis='SustainedEnergyVerification')
        self.assertNotEqual(code, 0)
        self.assertEqual(v['verdict'], 'VerdictKind::fail')

    def test_invalid_inputs_cannot_be_verified_even_with_evidence_flag(self):
        code, _, v = self.run_case('attribute :>> evidenceAccepted = true; part redefines battery { attribute :>> usableFraction = 1.1; }', analysis='SustainedEnergyVerification')
        self.assertNotEqual(code, 0)
        self.assertEqual(v['verdict'], 'VerdictKind::fail')

    def test_harvest_window_overlap_is_counted_in_each_day(self):
        # Extend the first enabled interval across midnight. It contributes six
        # hours to day one and one hour to day two; the later harvest shifts too.
        # The profile is now 73 hours and fails complete-day coverage.
        code, _, v = self.run_case('part redefines harvest1 { attribute :>> duration = 25200 [s]; }')
        self.assertEqual(code, 1)
        self.assertEqual(v['harvestHoursPerDay'], '[6.0, 6.0, 6.0]')
        self.assertEqual(v['campaignCovered'], 'false')

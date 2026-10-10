"""Exercise the production SysML constraints with synthetic observations.

These are evaluator/criterion regressions, not vessel qualification evidence.
"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.install_renderer import binary_path
from scripts.render_requirements import MODELS


class ExecutableRequirementsTests(unittest.TestCase):
    def evaluate(self, definition, inputs):
        bindings = '\n'.join(f'attribute :>> {key} = {value};' for key, value in inputs.items())
        source = ('package CriterionExample { private import SI::*; '
                  f'requirement sample : BlueDogRequirements::{definition} {{ {bindings} }} }}')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'observation.sysml'
            path.write_text(source, encoding='utf-8')
            result = subprocess.run([str(binary_path()), *map(str, MODELS), str(path),
                                     '-requirement', 'CriterionExample::sample', '-json'],
                                    capture_output=True, text=True, encoding='utf-8')
        report = json.loads(result.stdout)
        return result.returncode, report['status']

    def test_print_job_boundaries_and_units(self):
        baseline = dict(jobX='250 [mm]', jobY='0.25 [m]', jobZ='249 [mm]')
        self.assertEqual(self.evaluate('DesktopManufacture', baseline), (0, 'holds'))
        for axis in baseline:
            for invalid in ('250.1 [mm]', '0 [mm]', '-1 [mm]'):
                with self.subTest(axis=axis, value=invalid):
                    self.assertEqual(self.evaluate('DesktopManufacture', baseline | {axis: invalid}), (1, 'fails'))

    def test_reset_deadline(self):
        for value, expected in [('30 [s]', (0, 'holds')), ('30.1 [s]', (1, 'fails')), ('-1 [s]', (1, 'fails'))]:
            with self.subTest(value=value):
                self.assertEqual(self.evaluate('RestartDeadline', {'measuredRestartTime': value}), expected)

    def test_recovery_energy_boundary(self):
        # 1.2 * (100 W * 1800 s + 10 W * 7200 s) = 302400 J.
        inputs = dict(motorPower='100 [W]', essentialPower='10 [W]', reserveEnergy='302400 [J]')
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs), (0, 'holds'))
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs | {'reserveEnergy': '302399 [J]'}), (1, 'fails'))
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs | {'motorPower': '-100 [W]'}), (1, 'fails'))

    def test_capsize_deadlines(self):
        for definition, field, limit in [('RightingDeadline', 'measuredRightingTime', 60),
                                          ('ControlRecoveryDeadline', 'measuredControlRecoveryTime', 120)]:
            for seconds, expected in [(limit, (0, 'holds')), (limit + 1, (1, 'fails')), (-1, (1, 'fails'))]:
                with self.subTest(definition=definition, seconds=seconds):
                    self.assertEqual(self.evaluate(definition, {field: f'{seconds} [s]'}), expected)

    def test_navigation_availability_counts_missing_epochs(self):
        for count, expected in [(1710, (0, 'holds')), (1709, (1, 'fails')),
                                (1800, (0, 'holds')), (1801, (1, 'fails')), (-1, (1, 'fails'))]:
            with self.subTest(validEpochs=count):
                self.assertEqual(self.evaluate('NavigationValidEpochs', {'validEpochs': str(count)}), expected)

    def test_launch_energy_gate_and_input_validity(self):
        baseline = dict(conservativeStartEnergy='101 [J]', protectedReserve='100 [J]',
                        estimateAge='1 [s]', estimateValid='true', reserveValid='true', missionStartEnabled='true')
        self.assertEqual(self.evaluate('LaunchEnergyAdmission', baseline), (0, 'holds'))
        for change in [dict(conservativeStartEnergy='100 [J]'), dict(conservativeStartEnergy='99 [J]'),
                       dict(estimateAge='1.1 [s]'), dict(estimateAge='-1 [s]'),
                       dict(estimateValid='false'), dict(reserveValid='false'), dict(protectedReserve='0 [J]')]:
            with self.subTest(change=change):
                self.assertEqual(self.evaluate('LaunchEnergyAdmission', baseline | change), (1, 'fails'))
                self.assertEqual(self.evaluate('LaunchEnergyAdmission', baseline | change | {'missionStartEnabled': 'false'}), (0, 'holds'))

    def test_challenge_motor_invariant(self):
        for known in (False, True):
            for qualifying in (False, True):
                for motor in (False, True):
                    with self.subTest(known=known, qualifying=qualifying, motor=motor):
                        allowed = not motor or (known and not qualifying)
                        inputs = dict(qualificationStateKnown=str(known).lower(),
                                      qualifying=str(qualifying).lower(), motorEnabled=str(motor).lower())
                        self.assertEqual(self.evaluate('MotorQualificationInvariant', inputs),
                                         (0, 'holds') if allowed else (1, 'fails'))

    def test_missing_observations_cannot_pass(self):
        for definition in ['DesktopManufacture', 'RestartDeadline', 'RecoveryEnergy', 'RightingDeadline', 'ControlRecoveryDeadline', 'NavigationValidEpochs', 'LaunchEnergyAdmission', 'MotorQualificationInvariant']:
            with self.subTest(definition=definition):
                code, status = self.evaluate(definition, {})
                self.assertEqual(code, 2)
                self.assertNotEqual(status, 'holds')

    def test_sustained_energy_atomic_criteria_boundaries(self):
        cases = [
            ('SustainedReserveProtection', {'samples': '(101 [J], 102 [J])', 'reserve': '100 [J]'}, {'samples': '(101 [J], 100 [J], 102 [J])'}),
            ('RepeatableCycleBalance', {'initialEnergy': '100 [J]', 'finalEnergy': '100 [J]'}, {'finalEnergy': '99 [J]'}),
            ('PeakSupplyCapability', {'demands': '(10 [W], 10 [W])', 'availablePower': '10 [W]'}, {'demands': '(10 [W], 10.1 [W])'}),
            ('HarvestCampaignCoverage', {'duration': '259200 [s]', 'dayCount': '3', 'enabledHours': '(6, 6, 6)'}, {'enabledHours': '(6, 6.1, 6)'}),
            ('EnergyEvidenceReadiness', {'accepted': 'true'}, {'accepted': 'false'}),
        ]
        for definition, inputs, failing in cases:
            with self.subTest(definition=definition):
                self.assertEqual(self.evaluate(definition, inputs), (0, 'holds'))
                self.assertEqual(self.evaluate(definition, inputs | failing), (1, 'fails'))
                self.assertEqual(self.evaluate(definition, {})[0], 2)

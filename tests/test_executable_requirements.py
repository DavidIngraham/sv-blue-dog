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
                self.assertEqual(self.evaluate('ResetRecovery', {'measuredRestartTime': value}), expected)

    def test_recovery_energy_boundary(self):
        # 1.2 * (100 W * 1800 s + 10 W * 7200 s) = 302400 J.
        inputs = dict(motorPower='100 [W]', essentialPower='10 [W]', reserveEnergy='302400 [J]')
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs), (0, 'holds'))
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs | {'reserveEnergy': '302399 [J]'}), (1, 'fails'))
        self.assertEqual(self.evaluate('RecoveryEnergy', inputs | {'motorPower': '-100 [W]'}), (1, 'fails'))

    def test_capsize_deadlines(self):
        for definition, field, limit in [('SelfRighting', 'measuredRightingTime', 60),
                                          ('CapsizeControlRecovery', 'measuredControlRecoveryTime', 120)]:
            for seconds, expected in [(limit, (0, 'holds')), (limit + 1, (1, 'fails')), (-1, (1, 'fails'))]:
                with self.subTest(definition=definition, seconds=seconds):
                    self.assertEqual(self.evaluate(definition, {field: f'{seconds} [s]'}), expected)

    def test_missing_observations_cannot_pass(self):
        for definition in ['DesktopManufacture', 'ResetRecovery', 'RecoveryEnergy', 'SelfRighting', 'CapsizeControlRecovery']:
            with self.subTest(definition=definition):
                code, status = self.evaluate(definition, {})
                self.assertEqual(code, 2)
                self.assertNotEqual(status, 'holds')

"""Shared native SysML runner; pytest retains each case in its test directory."""
import json
import subprocess

import pytest

from scripts.install_renderer import binary_path
from scripts.render_requirements import MODELS


@pytest.fixture
def run_model(tmp_path):
    def run(source, *arguments):
        path = tmp_path / 'case.sysml'
        path.write_text(source, encoding='utf-8')
        result = subprocess.run(
            [str(binary_path()), *map(str, MODELS), str(path), *arguments, '-json'],
            capture_output=True, text=True, encoding='utf-8',
        )
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            pytest.fail(f'Native CLI returned no JSON report (exit {result.returncode}):\n{result.stdout}\n{result.stderr}')
        return result.returncode, report

    return run

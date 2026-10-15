"""Shared native SysML runner; pytest retains each case in its test directory."""
import json
import subprocess

import pytest

from tools.boat_analysis.model.install import binary_path
from tests.native_cases import MODELS


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


@pytest.fixture(scope="session")
def rendered_site(tmp_path_factory):
    from tools.publishing.build import build
    from tools.boat_analysis.model.runtime import ROOT
    output = tmp_path_factory.mktemp("published-site")
    build(ROOT / "docs", output)
    return output


@pytest.fixture(scope="session")
def acceptance_model():
    """One immutable native load; verify_requirement binds fresh inputs per call."""
    from tools.boat_analysis.model.runtime import load_model, ROOT
    return load_model((*MODELS, ROOT / "tests/fixtures/shared-acceptance.sysml"))


@pytest.fixture
def acceptance(acceptance_model):
    def evaluate(definition, **inputs):
        verdict = acceptance_model.verify_requirement(
            "SharedAcceptanceTests::" + definition, named_arguments=inputs)
        if not verdict.evaluated:
            return 2, "unevaluated"
        return (0, "holds") if verdict.holds else (1, "fails")
    return evaluate

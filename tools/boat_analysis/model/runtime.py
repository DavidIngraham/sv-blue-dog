"""One model loader for analysis, validation and publishing."""
import json
from pathlib import Path
import re
import subprocess

from tools.boat_analysis.model.install import binary_path

ROOT = Path(__file__).resolve().parents[3]


def model_files():
    return tuple(sorted((ROOT / "models").rglob("*.sysml")))


MODELS = model_files()


def native(*arguments, models=None):
    files = model_files() if models is None else tuple(dict.fromkeys(models))
    result = subprocess.run(
        [str(binary_path()), *map(str, files), *map(str, arguments)],
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
    )
    if result.returncode:
        raise RuntimeError(f"OpenSysML exited {result.returncode}:\n{result.stdout}\n{result.stderr}")
    return result.stdout


def validate(models=None):
    report = json.loads(native("-validate", "-json", models=models))
    errors = [d for d in report.get("diagnostics") or [] if d["severity"] == "error"]
    if errors:
        raise ValueError("Model validation failed: " + json.dumps(errors))
    return report


def native_value(text):
    """Decode the runtime's exact rational values at the numerical boundary."""
    text = re.sub(r"(-?\d+)/(\d+)", lambda m: str(int(m[1]) / int(m[2])), text)
    return json.loads(text)

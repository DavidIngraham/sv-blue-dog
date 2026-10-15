"""One model loader for analysis, validation and publishing."""
import json
import atexit
from fractions import Fraction
from functools import lru_cache
import os
from pathlib import Path
import re
import subprocess
import tempfile
from collections import Counter

from tools.boat_analysis.model.install import RELEASE, binary_path

ROOT = Path(__file__).resolve().parents[3]


def model_files():
    return tuple(sorted((ROOT / "models").rglob("*.sysml")))


MODELS = model_files()


def native(*arguments, models=None, commands=None):
    files = model_files() if models is None else tuple(dict.fromkeys(models))
    result = subprocess.run(
        [str(binary_path()), *map(str, files), *map(str, arguments)],
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT, input=commands,
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


@lru_cache(maxsize=1)
def connection():
    """Let the upstream client own its private service and typed wire protocol."""
    import opensysml
    previous = os.environ.get("OPENSYSML_BINARY")
    os.environ["OPENSYSML_BINARY"] = str(binary_path("sysml-grpc"))
    try:
        client = opensysml.connect(version=RELEASE,
                                  require_capabilities=("parse_sources", "case_evaluations", "document_query"))
    finally:
        if previous is None:
            os.environ.pop("OPENSYSML_BINARY", None)
        else:
            os.environ["OPENSYSML_BINARY"] = previous
    atexit.register(client.close)
    return client


@lru_cache(maxsize=4)
def _loaded_model(snapshot):
    return connection().parse_sources(snapshot, strict=True)


def load_model(models=None):
    files = model_files() if models is None else tuple(dict.fromkeys(models))
    # Inline source content makes both client and service caches independent of
    # filesystem timestamp granularity and same-size edits.
    snapshot = tuple((str(path), path.read_text(encoding="utf-8")) for path in files)
    return _loaded_model(snapshot)


def numerical_value(value):
    """Convert exact rationals only where boat numerics/JSON require floats."""
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, (tuple, list)):
        return [numerical_value(item) for item in value]
    if isinstance(value, dict):
        return {key: numerical_value(item) for key, item in value.items()}
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise TypeError(f"Unsupported numerical boundary value: {type(value).__name__}")


def analysis_values(name, models=None):
    result = load_model(models).run_analysis(name)
    if not result:
        raise ValueError(f"Model analysis did not satisfy its objectives: {name}: {result}")
    return numerical_value(result.outputs)


def record_analyses(names, output, models=None):
    """Write a standalone native AnalysisRecords snapshot, without editing inputs."""
    output = Path(output).resolve()
    files = model_files() if models is None else tuple(dict.fromkeys(models))
    if output in {Path(path).resolve() for path in files}:
        raise ValueError("Analysis records must not overwrite an input model")
    if not names:
        raise ValueError("Select at least one analysis case")
    output.parent.mkdir(parents=True, exist_ok=True)
    if any(not re.fullmatch(r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)+", name) for name in names):
        raise ValueError("Use qualified analysis case names")
    # The native REPL preserves source notation when saving a multi-file session.
    # API-JSON roundtrips cannot currently preserve all Blue Dog annotations.
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        staged = Path(directory) / "evidence.sysml"
        commands = ''.join(f"%record {name} into BlueDogRecordedEvidence\n" for name in names)
        commands += f"%save {json.dumps(staged.as_posix())}\n"
        native(models=files, commands=commands)
        if not staged.is_file():
            raise RuntimeError("Native session did not save its analysis evidence")
        model = load_model((staged,))
        records = model.query(where={"@type": "PrimitiveConstraint", "operator": "=",
                                     "property": "@type", "value": ["PartUsage"]})
        recorded = Counter(model.instantiate(record.id).caseName for record in records
                           if record.id.startswith("BlueDogRecordedEvidence::"))
        if recorded != Counter(names):
            raise RuntimeError(f"Native session did not record the requested cases: {dict(recorded)}")
        staged.replace(output)
    return output

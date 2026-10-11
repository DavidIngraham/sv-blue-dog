"""Validate immutable run evidence against its original source revision."""
import hashlib
import json
from pathlib import Path
import subprocess

from tools.boat_analysis.model.runtime import ROOT

BASELINE = ROOT / "evidence/runs/2026-10-10-coupled"
WORK = ROOT / "build/analysis"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(hashes):
    for name, expected in hashes.items():
        if digest(ROOT / name) != expected:
            raise ValueError("Stale analysis input: " + name)


def baseline_record(name):
    manifest = json.loads((BASELINE / "manifest.json").read_text(encoding="utf-8"))
    entry = manifest["files"][name]
    content = (BASELINE / name).read_bytes()
    if hashlib.sha256(content).hexdigest() != entry["sha256"]:
        raise ValueError("Modified archived evidence: " + name)
    return json.loads(content)


def verify_baseline_sources():
    """Check archived outputs and recorded hashes without relabelling old runs."""
    manifest = json.loads((BASELINE / "manifest.json").read_text(encoding="utf-8"))
    revision = manifest["sourceRevision"]
    checked = {}
    for name in manifest["files"]:
        record = baseline_record(name)
        for field in ("sourceHashes", "driverHashes"):
            for path, expected in record.get(field, {}).items():
                key = (path, expected)
                if key in checked:
                    continue
                result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT,
                                        capture_output=True, check=True)
                actual = hashlib.sha256(result.stdout.replace(b"\r\n", b"\n")).hexdigest()
                if actual != expected:
                    raise ValueError(f"Archived source mismatch: {name}: {path}")
                checked[key] = True
    return len(checked)


def input_record(name):
    path = WORK / name
    if path.exists():
        record = json.loads(path.read_text(encoding="utf-8"))
        validate(record.get("sourceHashes", record.get("driverHashes", {})))
        return record
    return baseline_record(name)


def input_path(name):
    path = WORK / name
    if path.exists():
        return path
    baseline_record(name)  # Reject altered or unregistered baseline inputs.
    return BASELINE / name


def source_hashes(sources):
    """Resolve evidence locations explicitly and include the loaded physics model."""
    from tools.boat_analysis.model.runtime import model_files
    paths = list(model_files())
    for name in sources:
        path = Path(name)
        if path.as_posix().startswith("build/analysis/"):
            path = input_path(path.name)
        else:
            path = ROOT / path
        paths.append(path)
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in paths}


def output_path(name):
    WORK.mkdir(parents=True, exist_ok=True)
    return WORK / name

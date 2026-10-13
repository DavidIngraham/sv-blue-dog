"""Validate immutable run evidence against its original source revision."""
import hashlib
import json
from pathlib import Path
import subprocess

from tools.boat_analysis.model.runtime import ROOT

BASELINE = ROOT / "evidence/runs/2026-10-10-coupled"
AERODYNAMIC_REFERENCE = ROOT / "evidence/runs/2026-10-11-conservative"
CURRENT = ROOT / "evidence/runs/2026-10-12-bingen"
WORK = ROOT / "build/analysis"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(hashes):
    for name, expected in hashes.items():
        if digest(ROOT / name) != expected:
            raise ValueError("Stale analysis input: " + name)


def baseline_record(name):
    return run_record(BASELINE, name)


def run_record(directory, name):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    entry = manifest["files"][name]
    content = (directory / name).read_bytes()
    if hashlib.sha256(content).hexdigest() != entry["sha256"]:
        raise ValueError("Modified archived evidence: " + name)
    return json.loads(content)


def verify_baseline_sources():
    """Check archived outputs and recorded hashes without relabelling old runs."""
    return verify_run_sources(BASELINE)


def verify_run_sources(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    revision = manifest["sourceRevision"]
    checked = {}
    for name in manifest["files"]:
        record = run_record(directory, name)
        for field in ("sourceHashes", "driverHashes"):
            for path, expected in record.get(field, {}).items():
                key = (path, expected)
                if key in checked:
                    continue
                if path.startswith("build/analysis/"):
                    dependency = Path(path).name
                    run_record(directory, dependency)
                    content = (directory / dependency).read_bytes()
                else:
                    result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT,
                                            capture_output=True, check=True)
                    content = result.stdout
                actual = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()
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
    paths = [*model_files(), *(ROOT/"packages/sysml-python/sysml_python").rglob("*.py"), ROOT/"pyproject.toml", ROOT / "tools/boat_analysis/model/native_kernel.py",
             ROOT / "tools/boat_analysis/model/abi.py",
             ROOT / "tools/boat_analysis/model/boundary.py",
             ROOT / "tools/boat_analysis/model/contracts.py",
             ROOT / "tools/boat_analysis/model/preparation.py"]
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


def archive_run(name, filenames, revision, scope):
    """Archive JSON results plus generated dependencies against one Git revision."""
    import shutil
    import tempfile
    destination = ROOT / 'evidence/runs' / name
    if not name or '/' in name or '\\' in name or Path(name).name != name or name in ('.', '..') or destination.exists():
        raise ValueError('Expected a new immutable run name')
    revision = subprocess.check_output(['git', 'rev-parse', revision], cwd=ROOT, text=True).strip()
    pending, selected = list(filenames), set()
    while pending:
        filename = pending.pop()
        if '/' in filename or '\\' in filename or Path(filename).name != filename or not filename.endswith('.json'):
            raise ValueError('Expected a workspace JSON record filename')
        if filename in selected:
            continue
        selected.add(filename)
        record = json.loads((WORK / filename).read_text(encoding='utf-8'))
        pending.extend(Path(path).name for field in ('sourceHashes', 'driverHashes')
                       for path in record.get(field, {}) if path.startswith('build/analysis/'))
    with tempfile.TemporaryDirectory(dir=WORK) as temporary:
        staged = Path(temporary)
        files = {}
        for filename in sorted(selected):
            shutil.copyfile(WORK / filename, staged / filename)
            files[filename] = {'sha256': hashlib.sha256((staged / filename).read_bytes()).hexdigest()}
        (staged / 'manifest.json').write_text(json.dumps(dict(sourceRevision=revision,
            files=files, qualified=False, scope=scope), indent=2)+'\n', encoding='utf-8')
        verify_run_sources(staged)
        shutil.copytree(staged, destination)
    return destination

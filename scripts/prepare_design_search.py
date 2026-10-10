"""Export the native search contract and compile SysML equations to C source."""
import hashlib
import json
import re
from pathlib import Path

try:
    from .render_requirements import native, ROOT, MODELS
except ImportError:
    from render_requirements import native, ROOT, MODELS


def native_value(text):
    # OpenSysML emits exact rationals in otherwise JSON-shaped numeric sequences.
    text = re.sub(r"(-?\d+)/(\d+)", lambda m: str(int(m[1]) / int(m[2])), text)
    return json.loads(text)


def prepare():
    report = json.loads(native("-analysis", "BlueDogDesignSearch::SearchInputs", "-json"))
    if report["status"] != "holds" or report.get("diagnostics"):
        raise ValueError("Native search contract failed")
    contract = {v["name"]: native_value(v["value"]) for v in report["checks"][0]["values"]}
    native("-compile", "BlueDogDesignPhysics::EvaluateCase", "-source", "-o", str(ROOT / ".tools/design-physics.c"))
    contract["sourceHashes"] = {
        name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for name in ([p.relative_to(ROOT).as_posix() for p in MODELS if p.name not in ("design-search-results.sysml", "design-search-documents.sysml")] + ["uv.lock", "scripts/install_renderer.py"])
    }
    contract["generatedCHash"] = hashlib.sha256((ROOT / ".tools/design-physics.c").read_bytes()).hexdigest()
    (ROOT / ".tools/design-search-contract.json").write_bytes((json.dumps(contract, indent=2) + "\n").encode())
    print("Exported native contract and C kernel; run solve_design.py in a C-capable environment.")


if __name__ == "__main__":
    prepare()

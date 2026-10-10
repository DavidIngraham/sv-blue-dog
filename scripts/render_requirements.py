"""Validate and publish requirements with the pinned native OpenSysML CLI."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from .install_renderer import binary_path
except ImportError:
    from install_renderer import binary_path

ROOT = Path(__file__).resolve().parents[1]
MODELS = tuple(ROOT / "models" / name for name in (
    "challenge.sysml", "blue-dog.sysml", "requirements.sysml",
    "requirements-view.sysml", "requirements-document.sysml"))


def native(*arguments, models=MODELS):
    binary = binary_path()
    if not binary.exists():
        raise SystemExit("Run uv run python scripts/install_renderer.py first.")
    result = subprocess.run([str(binary), *map(str, models), *arguments],
                            capture_output=True, text=True, encoding="utf-8")
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    result.check_returncode()
    return result.stdout


def native_graph():
    return native("-render", "BlueDogViews::requirements", "-render-form", "dot")


def native_register():
    return native("-render-document", "BlueDogDocuments::RequirementsRegister")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check model-derived DOT and register freshness without rendering")
    args = parser.parse_args()
    native("-validate")
    outputs = {ROOT / "docs/figures/requirements-derivation.dot": native_graph(),
               ROOT / "docs/requirements-register.md": native_register()}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Stale generated file: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
    if not args.check:
        dot = shutil.which("dot")
        if not dot:
            raise SystemExit("Install Graphviz and ensure dot is on PATH, then rerun.")
        source_path = ROOT / "docs/figures/requirements-derivation.dot"
        for extension in ("svg", "png"):
            subprocess.run([dot, "-Grankdir=LR", f"-T{extension}", str(source_path), "-o", str(source_path.with_suffix('.' + extension))], check=True)
    print("Native model validation and document generation passed; satisfaction is not evaluated.")


if __name__ == "__main__":
    main()

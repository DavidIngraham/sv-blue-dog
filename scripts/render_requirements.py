"""Validate and publish requirements with the pinned native OpenSysML CLI."""
import argparse
import re
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
    "requirements-view.sysml", "requirements-document.sysml", "architecture-view.sysml", "use-cases.sysml", "satisfaction.sysml"))


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
    views = {"architecture": "BlueDogArchitectureViews::architecture",
             "context": "BlueDogArchitectureViews::context",
             "architecture-detail": "BlueDogArchitectureViews::detail",
             "use-cases": "BlueDogUseCaseViews::operations"}
    outputs[ROOT / "docs/traceability.md"] = native(
        "-render-document", "BlueDogDocuments::Traceability")
    for name, view in views.items():
        outputs[ROOT / f"docs/figures/{name}.dot"] = native(
            "-render", view, "-render-form", "dot")
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
        # Align the two mission drivers at the top without changing native edges.
        layout = source_path.read_text(encoding="utf-8")
        roots = re.findall(r'"(n[0-9]+)" \[.*?<b>(?:GorgeChallenge::transGorgeChallenge|BlueDog::Goals::hawaiiVoyage) :', layout)
        if len(roots) != 2:
            raise SystemExit("Expected both top-level requirements in the native diagram.")
        layout = layout.rstrip().removesuffix("}") + '\n{ rank=sink; ' + '; '.join(roots) + '; }\n}\n'
        for extension in ("svg", "png"):
            subprocess.run([dot, "-Grankdir=BT", f"-T{extension}", "-o", str(source_path.with_suffix('.' + extension))], input=layout, text=True, encoding="utf-8", check=True)
        for name in views:
            source = ROOT / f"docs/figures/{name}.dot"
            for extension in ("svg", "png"):
                subprocess.run([dot, f"-T{extension}", str(source), "-o",
                                str(source.with_suffix("." + extension))], check=True)
    print("Native model validation and document generation passed; satisfaction is not evaluated.")


if __name__ == "__main__":
    main()

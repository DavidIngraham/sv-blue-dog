"""Validate and publish requirements with the pinned native OpenSysML CLI."""
import argparse
import re
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
    "requirements-view.sysml", "requirements-document.sysml", "architecture-view.sysml", "use-cases.sysml", "satisfaction.sysml", "recovery-trade.sysml", "energy.sysml", "energy-examples.sysml", "diagram-documents.sysml"))


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


def native_recovery_trade():
    arguments = []
    for candidate in ("waterExample", "airExample"):
        name = f"RecoveryPropulsionTrade::{candidate}"
        arguments.extend(("-instantiate", name, "-analysis",
                          f"RecoveryPropulsionTrade::RecoverySizing {name}"))
    return native(*arguments, "-json")


def native_energy_case():
    return native("-instantiate", "BlueDogEnergyExamples::sailing", "-analysis",
                  "BlueDogEnergy::BudgetRollup BlueDogEnergyExamples::sailing",
                  "-instantiate", "BlueDogEnergyExamples::campaign", "-analysis",
                  "BlueDogEnergy::SustainedOperation BlueDogEnergyExamples::campaign", "-json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated diagrams, reports and analyses for freshness")
    args = parser.parse_args()
    native("-validate")
    outputs = {ROOT / "docs/energy-budget.md": native("-render-document", "BlueDogDocuments::EnergyBudget"),
               ROOT / "docs/analysis/sustained-energy.json": native_energy_case(),
               ROOT / "docs/analysis/recovery-trade.json": native_recovery_trade(),
               ROOT / "docs/requirements-register.md": native_register()}
    outputs[ROOT / "docs/traceability.md"] = native(
        "-render-document", "BlueDogDocuments::Traceability")
    diagrams = {}
    for name, document in {
        "requirements-derivation": "RequirementsDiagram",
        "architecture": "ArchitectureDiagram", "context": "ContextDiagram",
        "architecture-detail": "DetailDiagram", "use-cases": "UseCasesDiagram",
    }.items():
        target = f"BlueDogDiagramDocuments::{document}"
        markdown = native("-render-document", target, "-diagram-form", "mermaid")
        outputs[ROOT / f"docs/figures/{name}.md"] = markdown
        outputs[ROOT / f"docs/figures/{name}.html"] = native(
            "-render-document", target, "-diagram-form", "mermaid",
            "-doc-form", "html", "-html-mermaid", "cdn")
        diagrams[name] = markdown[markdown.index("```mermaid"):].strip()
    # Keep hand-written prose; replace only explicitly marked native diagrams.
    for path in (ROOT / "docs").glob("*.md"):
        source = path.read_text(encoding="utf-8")
        if "<!-- diagram:" in source:
            outputs[path] = re.sub(
                r"<!-- diagram:([\w-]+) -->.*?<!-- /diagram -->",
                lambda match: f"<!-- diagram:{match[1]} -->\n{diagrams[match[1]]}\n<!-- /diagram -->",
                source, flags=re.DOTALL)
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Stale generated file: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
    print("Native validation, publishing, recovery-trade and sustained-energy analyses passed; physical compliance is not evaluated.")


if __name__ == "__main__":
    main()

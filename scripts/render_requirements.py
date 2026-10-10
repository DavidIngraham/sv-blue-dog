"""Validate and publish requirements with the pinned native OpenSysML CLI."""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from .install_renderer import binary_path
except ImportError:
    from install_renderer import binary_path

ROOT = Path(__file__).resolve().parents[1]
MODELS = tuple(ROOT / "models" / name for name in (
    "challenge.sysml", "blue-dog.sysml", "requirements.sysml",
    "requirements-view.sysml", "requirements-document.sysml", "architecture-view.sysml", "use-cases.sysml", "satisfaction.sysml", "recovery-trade.sysml", "energy.sysml", "energy-examples.sysml", "diagram-documents.sysml", "requirement-verification.sysml"))


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
    validation = json.loads(native("-validate", "-json"))
    errors = [d for d in validation.get("diagnostics") or [] if d["severity"] == "error"]
    if errors:
        raise SystemExit("Model validation failed: " + "; ".join(d["message"] for d in errors))
    outputs = {ROOT / "docs/energy-budget.md": native("-render-document", "BlueDogDocuments::EnergyBudget"),
               ROOT / "docs/analysis/sustained-energy.json": native_energy_case(),
               ROOT / "docs/analysis/recovery-trade.json": native_recovery_trade(),
               ROOT / "docs/requirements-register.md": native_register()}
    outputs[ROOT / "docs/traceability.md"] = native(
        "-render-document", "BlueDogDocuments::Traceability")
    outputs[ROOT / "docs/requirements-context.md"] = native(
        "-render-document", "BlueDogDocuments::RequirementContext")
    diagrams = {}
    # Compile the model once per format, rather than once for every view.
    with tempfile.TemporaryDirectory(dir=ROOT / ".tools", prefix="documents-") as scratch:
        directory = Path(scratch)
        native("-render-documents", str(directory / "markdown"), "-diagram-form", "mermaid")
        native("-render-documents", str(directory / "html"), "-diagram-form", "mermaid",
               "-doc-form", "html", "-html-mermaid", "cdn")
        for name, document in {
            "requirements-c-000": "TransGorgeChallengeRequirements",
            "requirements-c-001": "CourseCompletionRequirements",
            "requirements-c-002": "RepeatedOperationRequirements",
            "requirements-c-003": "UnassistedAttemptRequirements",
            "requirements-c-004": "SailingPropulsionRequirements",
            "requirements-c-005": "LiveObservationRequirements",
            "requirements-c-006": "EmergencyInterventionRequirements",
            "requirements-h-001": "HawaiiVoyageRequirements",
            "requirements-m-001": "RoundTripRequirements",
            "requirements-m-002": "MultiDayEnduranceRequirements",
            "requirements-e-001": "EnergyAwarenessRequirements",
            "requirements-e-002": "NavigationAndControlRequirements",
            "requirements-s-001": "TrafficSafetyRequirements",
            "requirements-n-001": "EnvironmentalEnvelopeRequirements",
            "requirements-s-003": "SafeRecoveryRequirements",
            "requirements-r-001": "RecoveryPropulsionRequirements",
            "requirements-e-005": "CommunicationsRequirements",
            "requirements-n-010": "GorgeEnvironmentRequirements",
            "requirements-n-020": "OceanEnvironmentRequirements",
            "requirements-n-002": "MarineDurabilityRequirements",
            "requirements-n-003": "StabilityAndFoulingRequirements",
            "requirements-r-002": "RecoveryEnergyRequirements",
            "requirements-e-003": "ResetRecoveryRequirements",
            "requirements-e-004": "LowEnergyRecoveryRequirements",
            "requirements-e-006": "IngressResponseRequirements",
            "requirements-e-007": "MissionEvidenceRequirements",
            "requirements-e-008": "NavigationAvailabilityRequirements",
            "requirements-p-001": "TransportabilityRequirements",
            "requirements-p-003": "ServiceabilityRequirements",
            "requirements-s-002": "OperatingBoundaryRequirements",
            "requirements-s-004": "NavigationConspicuityRequirements",
            "requirements-s-005": "RegulatoryClassificationRequirements",
            "requirements-c-101": "TelemetryEquipmentRequirements",
            "requirements-c-102": "CommandIntegrityRequirements",
            "requirements-n-033": "VisibilityRequirements",
            "requirements-n-035": "EnvelopeTransitionRequirements",
            "requirements-n-044": "WetMechanicalIntegrityRequirements",
            "requirements-n-045": "WetElectricalIntegrityRequirements",
            "requirements-n-046": "SolarHeatingRequirements",
            "requirements-n-051": "SelfRightingRequirements",
            "requirements-n-052": "CapsizeControlRecoveryRequirements",
            "requirements-n-053": "SubmergedWeedPassageRequirements",
            "requirements-n-054": "WeedSnagSheddingRequirements",
            "requirements-n-055": "WeedBlockageResponseRequirements",
            "requirements-n-056": "RecoveryPropulsorWeedsRequirements",
            "requirements-r-004": "ChallengeMotorInhibitionRequirements",
            "requirements-e-200": "SustainedEnergyFeasibilityRequirements",
            "architecture": "ArchitectureDiagram", "context": "ContextDiagram",
            "architecture-detail": "DetailDiagram", "use-cases": "UseCasesDiagram",
        }.items():
            stem = f"BlueDogDiagramDocuments-{document}"
            markdown = (directory / "markdown" / f"{stem}.md").read_text(encoding="utf-8")
            outputs[ROOT / f"docs/figures/{name}.md"] = markdown
            outputs[ROOT / f"docs/figures/{name}.html"] = (
                directory / "html" / f"{stem}.html").read_text(encoding="utf-8")
            diagrams[name] = markdown.split("\n", 1)[1].strip()
        for stylesheet in (directory / "html").glob("*.css"):
            outputs[ROOT / "docs/figures" / stylesheet.name] = stylesheet.read_text(encoding="utf-8")
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

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
    "requirements-view.sysml", "requirements-document.sysml", "architecture-view.sysml", "use-cases.sysml", "satisfaction.sysml", "recovery-trade.sysml", "energy.sysml", "energy-examples.sysml", "diagram-documents.sysml", "requirement-verification.sysml", "cruise-reliability.sysml", "dfmea.sysml", "reliability-documents.sysml", "semantic-views.sysml", "sailing-performance.sysml", "sailing-documents.sysml", "appendage-sizing.sysml", "sizing-documents.sysml", "design-search.sysml", "design-physics.sysml", "design-search-results.sysml", "design-search-documents.sysml"))


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


def native_sailing_case():
    arguments = []
    for example, analysis in (
        ("upstreamHeadwind", "PolarDemandAndHullScreen"),
        ("upstreamTailwind", "PolarDemandAndHullScreen"),
        ("downstreamHeadwind", "PolarDemandAndHullScreen"),
        ("downstreamTailwind", "PolarDemandAndHullScreen"),
        ("oceanIllustration", "PolarDemandAndHullScreen"),
        ("gorgeWesterly", "PolarVoyageAssessment"),
        ("gorgeEasterly", "PolarVoyageAssessment"),
        ("upstreamHeadwind", "SailingSensitivity"),
    ):
        subject = f"BlueDogSailingExamples::{example}"
        arguments.extend(("-instantiate", subject, "-analysis", f"BlueDogSailing::{analysis} {subject}"))
    return native(*arguments, "-json")


def native_sizing_case():
    arguments = []
    for example in ("reference", "lowRig", "slowControl", "gust", "highResistance"):
        subject = f"BlueDogSizingExamples::{example}"
        arguments.extend(("-instantiate", subject, "-analysis", f"BlueDogSizing::CoupledSizing {subject}"))
    return native(*arguments, "-json")


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
    outputs[ROOT / "docs/dfmea.md"] = native("-render-document", "BlueDogReliabilityDocuments::DFMEA")
    outputs[ROOT / "docs/cruise-reliability-results.md"] = native("-render-document", "BlueDogReliabilityDocuments::CruiseReport")
    outputs[ROOT / "docs/analysis/cruise-reliability.json"] = native(
        "-instantiate", "BlueDogReliabilityExamples::gorgeIllustration", "-analysis",
        "BlueDogReliability::CruiseReliability BlueDogReliabilityExamples::gorgeIllustration", "-json")
    outputs[ROOT / "docs/analysis/dfmea.json"] = native(
        "-instantiate", "BlueDogDFMEA::starter", "-analysis",
        "BlueDogDFMEA::DesignFailureReview BlueDogDFMEA::starter", "-json")
    outputs[ROOT / "docs/challenge-brief.md"] = native("-render-document", "BlueDogDocuments::ChallengeBrief")
    outputs[ROOT / "docs/requirements-views.md"] = native("-render-document", "BlueDogDocuments::RequirementsIndex")
    outputs[ROOT / "docs/relationship-register.md"] = native("-render-document", "BlueDogDocuments::RelationshipRegister")
    outputs[ROOT / "docs/sailing-performance-results.md"] = native("-render-document", "BlueDogSailingDocuments::SailingReport")
    outputs[ROOT / "docs/analysis/sailing-performance.json"] = native_sailing_case()
    try:
        from .plot_sailing import sailing_figures
    except ImportError:
        from plot_sailing import sailing_figures
    for name, content in sailing_figures(outputs[ROOT / "docs/analysis/sailing-performance.json"]).items():
        outputs[ROOT / "docs/figures" / name] = content
    outputs[ROOT / "docs/appendage-sizing-results.md"] = native("-render-document", "BlueDogSizingDocuments::SizingReport")
    outputs[ROOT / "docs/analysis/appendage-sizing.json"] = native_sizing_case()
    try:
        from .plot_sizing import sizing_figure
    except ImportError:
        from plot_sizing import sizing_figure
    outputs[ROOT / "docs/figures/appendage-sizing.png"] = sizing_figure(outputs[ROOT / "docs/analysis/appendage-sizing.json"])
    try:
        from .publish_design_search import read_search, result_model
        from .plot_design_search import search_figure
    except ImportError:
        from publish_design_search import read_search, result_model
        from plot_design_search import search_figure
    search = read_search()
    if (ROOT / "models/design-search-results.sysml").read_text() != result_model(search):
        raise SystemExit("Run scripts/publish_design_search.py to update the saved model subjects")
    audit = native("-analysis", "BlueDogDesignResults::full_envelopeAudit", "-analysis", "BlueDogDesignResults::nominal_5msAudit", "-json")
    outputs[ROOT / "docs/analysis/design-search-audit.json"] = audit
    outputs[ROOT / "docs/design-search-results.md"] = native("-render-document", "BlueDogDesignSearchDocuments::SearchReport")
    outputs[ROOT / "docs/figures/design-search.png"] = search_figure(audit, search)
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
            "requirements-q-001": "CruisePerformanceRequirements",
            "requirements-l-001": "MissionReliabilityRequirements",
            "sailing-integration": "SailingIntegrationDiagram",
            "sizing-integration": "SizingIntegrationDiagram",
            "mission-semantics": "MissionSemantics",
            "energy-semantics": "EnergySemantics",
            "cruise-semantics": "CruiseSemantics",
            "reliability-semantics": "ReliabilitySemantics",
            "manufacturing-semantics": "ManufacturingSemantics",
            "weed-semantics": "WeedSemantics",
            "architecture": "ArchitectureDiagram", "context": "ContextDiagram",
            "architecture-detail": "DetailDiagram", "use-cases": "UseCasesDiagram",
        }.items():
            stem = f"BlueDogDiagramDocuments-{document}"
            markdown = (directory / "markdown" / f"{stem}.md").read_text(encoding="utf-8")
            outputs[ROOT / f"docs/figures/{name}.md"] = markdown
            outputs[ROOT / f"docs/figures/{name}.html"] = (
                directory / "html" / f"{stem}.html").read_text(encoding="utf-8")
            diagrams[name] = "\n\n".join(re.findall(r"```mermaid\n.*?```", markdown, re.DOTALL))
        for stylesheet in (directory / "html").glob("*.css"):
            outputs[ROOT / "docs/figures" / stylesheet.name] = stylesheet.read_text(encoding="utf-8")
    generated_paths = set(outputs)
    # Keep hand-written prose; replace only explicitly marked native diagrams.
    for path in (ROOT / "docs").glob("*.md"):
        source = path.read_text(encoding="utf-8")
        if "<!-- diagram:" in source:
            outputs[path] = re.sub(
                r"<!-- diagram:([\w-]+) -->.*?<!-- /diagram -->",
                lambda match: f"<!-- diagram:{match[1]} -->\n{diagrams[match[1]]}\n<!-- /diagram -->",
                source, flags=re.DOTALL)
    for path, content in outputs.items():
        if path.suffix == ".md" and path in generated_paths:
            heading, separator, body = content.partition("\n")
            content = heading + separator + "\n<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->\n" + body
        if args.check:
            if not path.exists() or (path.read_bytes() if isinstance(content, bytes) else path.read_text(encoding="utf-8")) != content:
                raise SystemExit(f"Stale generated file: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
    print("Native validation, publishing and model analyses passed; physical compliance is not evaluated.")


if __name__ == "__main__":
    main()

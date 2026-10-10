"""Generate the Blue Dog requirements diagram and register using OpenSysML 0.9.2."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import opensysml

try:
    from .install_renderer import binary_path
except ImportError:  # Direct script invocation
    from install_renderer import binary_path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/requirements.sysml"
ARCHITECTURE = ROOT / "models/blue-dog.sysml"
CHALLENGE = ROOT / "models/challenge.sysml"


def load_model(source):
    """Reject engine diagnostics before consuming a potentially partial model."""
    model = (opensysml.parse_sources(source) if isinstance(source, list)
             else opensysml.loads(source))
    if not model.ok:
        raise ValueError("OpenSysML model errors: " + "; ".join(map(str, model.errors)))
    return model


def project_sources():
    return [(path.name, path.read_text(encoding="utf-8-sig")) for path in (CHALLENGE, ARCHITECTURE, MODEL)]


def extract(source):
    # The public API JSON export retains documentation, metadata types and
    # reference subsetting. Symbol summaries alone do not expose all three.
    # This export is experimental upstream; pin the engine and fail on gaps.
    model = load_model(source)
    elements = json.loads(str(model.to_api_json()))
    index = {e["@id"]: e for e in elements}

    def deref(ref):
        try:
            return index[ref["@id"]]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Unresolved model reference: {ref}") from exc

    def members(element):
        return [deref(ref) for ref in element.get("ownedMember", [])]

    def single(items, description):
        if len(items) != 1:
            raise ValueError(f"Expected one {description}, found {len(items)}")
        return items[0]

    def documentation(element):
        doc = single([e for e in members(element) if e["@type"] == "Documentation"], "documentation")
        return " ".join(doc["body"].split())

    def tags(element):
        return [deref(single(e.get("type", []), "metadata type"))["qualifiedName"]
                for e in members(element) if e["@type"] == "MetadataUsage"]

    def work_status(element):
        annotations = [e for e in members(element) if e["@type"] == "MetadataUsage"
                       and deref(single(e.get("type", []), "metadata type"))["qualifiedName"]
                       == "ModelingMetadata::StatusInfo"]
        if not annotations:
            return "unspecified"
        annotation = single(annotations, "StatusInfo annotation")
        field = single([e for e in members(annotation)
                        if e.get("qualifiedName", "").endswith("::status")], "status field")
        value = deref(field.get("value"))
        literal = deref(value.get("referent"))
        qualified = literal.get("qualifiedName", "")
        prefix = "ModelingMetadata::StatusKind::"
        if not qualified.startswith(prefix):
            raise ValueError("StatusInfo requires a StatusKind enum value")
        return qualified[len(prefix):]

    scope = single([e for e in elements if e["@type"] == "Package"
                    and e.get("declaredName") in {"Requirements", "BlueDogRequirements"}], "Requirements package")
    challenge_scopes = [e for e in elements if e["@type"] == "Package"
                        and e.get("qualifiedName") in {"GorgeChallenge", "BlueDog::Goals"}]
    children = [member for package in challenge_scopes + [scope]
                for member in members(package)]
    if any(e["@type"] == "Package" for e in children):
        raise ValueError("Nested requirement packages are not supported by this renderer")
    definitions, requirements, edges = {}, {}, []
    for definition in children:
        if definition["@type"] != "RequirementDefinition":
            continue
        name, short_id = definition.get("declaredName"), definition.get("declaredShortName")
        if not name or not short_id:
            raise ValueError("Every requirement definition needs a short ID and name")
        statement = documentation(definition)
        if any(d["id"] == short_id or d["name"] == name for d in definitions.values()):
            raise ValueError(f"Duplicate definition name or ID: {name}")
        definitions[definition["@id"]] = dict(id=short_id, name=name, statement=statement, status=work_status(definition))
    usage_ids = {}
    for usage in children:
        if usage["@type"] != "RequirementUsage":
            continue
        name = usage["declaredName"]
        type_id = single(usage.get("type", []), "requirement type")["@id"]
        if type_id not in definitions or name in requirements:
            raise ValueError(f"Unknown type or duplicate requirement usage: {name}")
        requirements[name] = dict(definitions[type_id], usage=name)
        usage_ids[usage["@id"]] = name
    roles = {"RequirementDerivation::OriginalRequirementMetadata": "original",
             "RequirementDerivation::DerivedRequirementMetadata": "derive"}
    for connection in children:
        if connection["@type"] != "ConnectionUsage":
            continue
        name = connection["declaredName"]
        if [tag for tag in tags(connection) if tag != "ModelingMetadata::StatusInfo"] != ["RequirementDerivation::DerivationMetadata"]:
            raise ValueError(f"Unsupported connection in requirements package: {name}")
        ends = {}
        for end in members(connection):
            if end["@type"] in {"Documentation", "MetadataUsage"}:
                continue
            if not end.get("isEnd"):
                raise ValueError(f"Unsupported connection member in {name}")
            tag = single(tags(end), "end role")
            role = roles.get(tag)
            if role is None or role in ends:
                raise ValueError(f"Unsupported or duplicate end role in {name}")
            binding = deref(end.get("ownedReferenceSubsetting"))
            target = binding.get("referencedFeature", {}).get("@id")
            if target not in usage_ids:
                raise ValueError(f"Unresolved requirement endpoint in {name}: {target}")
            ends[role] = usage_ids[target]
        if set(ends) != {"original", "derive"}:
            raise ValueError(f"Missing derivation ends in {name}")
        rationale = documentation(connection)
        edges.append(dict(name=name, source=ends["original"], target=ends["derive"], rationale=rationale, status=work_status(connection)))
    if not requirements or not edges:
        raise ValueError("Empty requirements or derivation graph")
    pairs = [(e["source"], e["target"]) for e in edges]
    if len(set(pairs)) != len(pairs):
        raise ValueError("Duplicate derivation edge")
    if len({e["name"] for e in edges}) != len(edges):
        raise ValueError("Duplicate derivation name")
    active, visited = set(), set()

    def visit(name):
        if name in active:
            raise ValueError("Cyclic requirement derivation")
        if name in visited:
            return
        active.add(name)
        for start, end in pairs:
            if start == name:
                visit(end)
        active.remove(name)
        visited.add(name)

    for name in requirements:
        visit(name)
    return requirements, edges


def native_graph():
    """Return native DOT unchanged; OpenSysML selects nodes and relationships."""
    binary = binary_path()
    if not binary.exists():
        raise SystemExit("Run uv run python scripts/install_renderer.py first.")
    result = subprocess.run(
        [str(binary), str(CHALLENGE), str(ARCHITECTURE), str(MODEL), str(ROOT / "models/requirements-view.sysml"),
         "-render", "BlueDogViews::requirements", "-render-form", "dot"],
        check=True, capture_output=True, text=True, encoding="utf-8")
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if "// kind: requirement" not in result.stdout:
        raise ValueError("Native renderer did not produce a requirement graph")
    return result.stdout


def native_register():
    """Render the model-defined document without custom table construction."""
    result = subprocess.run(
        [str(binary_path()), str(CHALLENGE), str(ARCHITECTURE), str(MODEL),
         str(ROOT / "models/requirements-document.sysml"),
         "-render-document", "BlueDogDocuments::RequirementsRegister"],
        check=True, capture_output=True, text=True, encoding="utf-8")
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check model-derived DOT and register freshness without rendering")
    args = parser.parse_args()
    requirements, edges = extract(project_sources())
    # Analyze the mission/architecture through the same OpenSysML runtime.
    # project_sources includes the architecture and both mission drivers.
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
    print(f"Checked {len(requirements)} requirements and {len(edges)} explicit derivations; no cycles or unresolved endpoints.")
    print("OpenSysML analysis and project graph checks passed; requirement satisfaction is not evaluated.")


if __name__ == "__main__":
    main()

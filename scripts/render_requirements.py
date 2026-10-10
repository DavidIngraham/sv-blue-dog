"""Generate the Blue Dog requirements diagram and register using OpenSysML 0.9.2."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

import opensysml

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/requirements.sysml"
COLORS = {"CONFIRMED INTENT": "#dbeafe", "LEGACY INTENT": "#fef3c7", "PROPOSED": "#e2e8f0"}


def load_model(source):
    """Reject engine diagnostics before consuming a potentially partial model."""
    model = opensysml.loads(source)
    if not model.ok:
        raise ValueError("OpenSysML model errors: " + "; ".join(map(str, model.errors)))
    return model


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

    scope = single([e for e in elements if e["@type"] == "Package"
                    and e.get("declaredName") == "Requirements"], "Requirements package")
    children = members(scope)
    if any(e["@type"] == "Package" for e in children):
        raise ValueError("Nested requirement packages are not supported by this renderer")
    definitions, requirements, edges = {}, {}, []
    for definition in children:
        if definition["@type"] != "RequirementDefinition":
            continue
        name, short_id = definition.get("declaredName"), definition.get("declaredShortName")
        if not name or not short_id:
            raise ValueError("Every requirement definition needs a short ID and name")
        status, separator, statement = documentation(definition).partition(": ")
        if not separator or status not in COLORS:
            raise ValueError(f"Unknown requirement maturity: {name}")
        if any(d["id"] == short_id or d["name"] == name for d in definitions.values()):
            raise ValueError(f"Duplicate definition name or ID: {name}")
        definitions[definition["@id"]] = dict(id=short_id, name=name, status=status, statement=statement)
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
        if tags(connection) != ["RequirementDerivation::DerivationMetadata"]:
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
        if not rationale.startswith("PROPOSED: "):
            raise ValueError(f"Review maturity handling before approving derivation {name}")
        edges.append(dict(name=name, source=ends["original"], target=ends["derive"], rationale=rationale))
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


def graph(requirements, edges):
    lines = ['digraph Requirements {',
             'graph [rankdir=LR, bgcolor="white", pad=0.3, nodesep=0.3, ranksep=0.8,',
             ' fontname="Arial", fontsize=18, labelloc=t, label="SV Blue Dog | Requirement derivation"];',
             'node [shape=box, style="rounded,filled", fontname="Arial", fontsize=12, color="#475569", margin="0.18,0.12"];',
             'edge [color="#64748b", style=dashed, arrowsize=0.7];']
    for name, req in requirements.items():
        title = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", req["name"])
        label = f'{req["id"]} | {title}\n{req["status"].lower()}'
        lines.append(f'{json.dumps(name)} [label={json.dumps(label)}, fillcolor="{COLORS[req["status"]]}"];')
    for edge in edges:
        lines.append(f'{json.dumps(edge["source"])} -> {json.dumps(edge["target"])} [tooltip={json.dumps(edge["rationale"])}];')
    lines.append('labelloc=b; label="SV Blue Dog | Requirement derivation\\nDashed arrows: original to derived requirement (all links proposed)\\nBlue: confirmed intent | Amber: legacy intent | Gray: proposed\\nIntent is not verification; acceptance thresholds remain open";\n}')
    return "\n".join(lines) + "\n"


def table(requirements, edges):
    lines = ["# Requirement derivation register", "", "Generated from `models/requirements.sysml`; edit the model and regenerate.", "", "## Requirements", "", "| ID | Requirement | Maturity | Statement |", "| --- | --- | --- | --- |"]
    for req in requirements.values():
        lines.append(f'| {req["id"]} | {req["name"]} | {req["status"]} | {req["statement"].replace("|", "&#124;")} |')
    lines += ["", "## Proposed derivations", "", "Direction: original requirement to derived requirement. These relationships record design reasoning, not proof of satisfaction.", "", "| Original | Derived | Rationale |", "| --- | --- | --- |"]
    for edge in edges:
        lines.append(f'| {requirements[edge["source"]]["id"]} | {requirements[edge["target"]]["id"]} | {edge["rationale"].replace("|", "&#124;")} |')
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check model-derived DOT and register freshness without rendering")
    args = parser.parse_args()
    source = MODEL.read_text(encoding="utf-8-sig")
    requirements, edges = extract(source)
    # Analyze the mission/architecture through the same OpenSysML runtime.
    load_model((ROOT / "models/blue-dog.sysml").read_text(encoding="utf-8-sig"))
    outputs = {ROOT / "docs/figures/requirements-derivation.dot": graph(requirements, edges),
               ROOT / "docs/requirements-register.md": table(requirements, edges)}
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
            subprocess.run([dot, f"-T{extension}", str(source_path), "-o", str(source_path.with_suffix('.' + extension))], check=True)
    print(f"Checked {len(requirements)} requirements and {len(edges)} explicit derivations; no cycles or unresolved endpoints.")
    print("OpenSysML analysis and project graph checks passed; requirement satisfaction is not evaluated.")


if __name__ == "__main__":
    main()

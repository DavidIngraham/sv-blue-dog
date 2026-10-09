"""Render explicit requirement derivations from sysmlpy's concrete parse tree.

Pinned to sysmlpy 0.96.4: its higher-level ConnectionUsage conversion drops
metadata ends. This narrow adapter supports one flat Requirements package,
local typed requirement usages, and one original/one derived end per connection.
Unsupported constructs fail rather than silently losing graph edges.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from sysmlpy.antlr_parser import parse

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/requirements.sysml"
COLORS = {"CONFIRMED INTENT": "#dbeafe", "LEGACY INTENT": "#fef3c7", "PROPOSED": "#e2e8f0"}


def nodes(tree, kind):
    if type(tree).__name__ == kind + "Context":
        yield tree
    for child in getattr(tree, "children", None) or []:
        yield from nodes(child, kind)


def one(tree, kind):
    found = list(nodes(tree, kind))
    if len(found) != 1:
        raise ValueError(f"Expected one {kind}, found {len(found)}")
    return found[0]


def documentation(tree):
    text = one(tree, "Documentation").getText()
    text = text[text.index("/*") + 2:text.rindex("*/")]
    return " ".join(line.strip().lstrip("*").strip() for line in text.splitlines())


def extract(source):
    tree = parse(source, rescue_language=None)
    definitions, requirements, edges = {}, {}, []
    packages = [p for p in nodes(tree, "Package")
                if p.packageDeclaration().identification().getText() == "Requirements"]
    if len(packages) != 1:
        raise ValueError("Expected exactly one Requirements package")
    scope = packages[0]
    if len(list(nodes(scope, "Package"))) != 1:
        raise ValueError("Nested requirement packages are not supported by this adapter")
    for definition in nodes(scope, "RequirementDefinition"):
        ident = definition.definitionDeclaration().identification()
        names = [n.getText().strip("'") for n in nodes(ident, "Name")]
        if len(names) != 2:
            raise ValueError("Every requirement definition needs a short ID and name")
        short_id, name = names
        doc = documentation(definition)
        status, separator, statement = doc.partition(": ")
        if not separator or status not in COLORS:
            raise ValueError(f"Unknown requirement maturity: {name}")
        if name in definitions or any(d["id"] == short_id for d in definitions.values()):
            raise ValueError(f"Duplicate definition name or ID: {name}")
        definitions[name] = dict(id=short_id, name=name, status=status, statement=statement)
    for usage in nodes(scope, "RequirementUsage"):
        name = one(usage, "Identification").getText()
        type_name = one(one(usage, "FeatureTyping"), "QualifiedName").getText()
        if type_name not in definitions or name in requirements:
            raise ValueError(f"Unknown type or duplicate requirement usage: {name}")
        requirements[name] = dict(definitions[type_name], usage=name)
    for connection in nodes(scope, "ConnectionUsage"):
        name = connection.usageDeclaration().identification().getText()
        tags = [n.getText() for n in nodes(connection.occurrenceUsagePrefix(), "PrefixMetadataFeature")]
        if tags != ["derivation"]:
            raise ValueError(f"Unsupported connection in requirements package: {name}")
        ends = {}
        for end in nodes(connection, "ExtendedUsage"):
            if not list(nodes(end, "EndUsagePrefix")):
                raise ValueError(f"Expected an end usage in {name}")
            tag = one(end, "PrefixMetadataFeature").getText()
            ref = one(one(end, "OwnedReferenceSubsetting"), "QualifiedName").getText()
            if tag not in {"original", "derive"} or tag in ends:
                raise ValueError(f"Unsupported or duplicate end role in {name}")
            if ref not in requirements:
                raise ValueError(f"Unresolved requirement endpoint: {ref}")
            ends[tag] = ref
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
    # Also parse the mission/architecture file. This is syntax validation only.
    parse((ROOT / "models/blue-dog.sysml").read_text(encoding="utf-8-sig"), rescue_language=None)
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
    print("Syntax and adapter checks only; no complete SysML semantic validation or requirement satisfaction claimed.")


if __name__ == "__main__":
    main()

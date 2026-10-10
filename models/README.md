# Modeling and publishing

Start with the [design guide](../docs/design-guide.md). SysML definitions are authoritative; generated Markdown and HTML are published views of those definitions.

## Environment

The package-free [uv project](../pyproject.toml) and [lockfile](../uv.lock) control the Python environment. The native OpenSysML CLI is separately pinned, with platform archive hashes, in [install_renderer.py](../scripts/install_renderer.py). Downloads stay in ignored `.tools/`; no global installation is needed.

```sh
uv sync --locked
uv run python scripts/install_renderer.py
uv run python scripts/render_requirements.py
uv run pytest -q
uv run python scripts/render_requirements.py --check
```

The publishing command validates the model, executes the native analysis cases, renders native documents, and copies outputs to stable paths. `--check` regenerates in scratch space and rejects stale tracked artifacts. Commit generated files with their model changes. Pytest checks native behavior, derivation coverage and repository documentation links; it is not physical test evidence.

## Authoring conventions

- Keep requirement `doc` text to a concise obligation. Use named `comment conditions` for normative qualification context and `comment notes` for explanation.
- Use standard `ModelingMetadata::Rationale`, `Issue` and `StatusInfo` metadata for justification, open decisions and work status. Status is not a verification verdict.
- Put executable acceptance predicates in the requirements and reuse them in analyses. Keep synthetic input scenarios distinct from reusable definitions.
- Use native `verify` links for verification cases and `satisfy` for intended design allocations. Unimplemented procedures and unaccepted evidence must not produce a verification pass.
- Put document queries and view definitions in SysML. The Python publisher orchestrates the native tool; it does not reinterpret requirement prose or implement analysis equations.

## Published artifacts

The publisher owns the challenge brief, requirements index/register/context, traceability, energy budget, DFMEA, cruise results, `docs/analysis/` and `docs/figures/`. Do not hand-edit these outputs. The [design guide](../docs/design-guide.md) links each report to its model source and explains the analysis methods.

Focused requirement views include one parent and at most three immediate children. `DiagramLayout::Layout` metadata limits membership; Mermaid lays out retained nodes. Dashed derivation arrows point from derived to original, with originals at the top. The complete graph is only a regression oracle. Tests verify that focused views cover all derivations.

GitHub renders native Mermaid Markdown; the blog imports the same repository files. Standalone HTML includes native rendering support and shares a generated stylesheet. `DocumentQueries` and `DiagramLayout` are OpenSysML tooling libraries. Reliability logarithms/exponentials use its non-normative `OpenSysMLMathFunctions` extension.

Update the website publication manifest when adding or removing reader-facing pages. Keep the authored documentation small: explain the design process and method limitations, then link to generated model facts. Keep review logs and temporary planning notes out of tracked docs.

## References

- [OpenSysML](https://github.com/Open-MBEE/OpenSysML)
- [Official SysML v2 release](https://github.com/Systems-Modeling/SysML-v2-Release)
- [Standard modeling metadata](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml.library/Domain%20Libraries/Metadata/ModelingMetadata.sysml)

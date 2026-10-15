# Working on Blue Dog

Use the pinned upstream OpenSysML tools for parsing, semantic queries, model edits,
verification, execution, and model view/report rendering. Prefer the `opensysml`
MCP server when available; use the matching native CLI or Python client otherwise.
Do not introduce a second SysML parser, relationship engine, or result ontology.

The dependency revision is pinned in `pyproject.toml`, `uv.lock`, and
`tools/boat_analysis/model/install.py`. Keep the CLI, Python service, MCP server
and Python client aligned. Bootstrap the pinned fork candidate with
`python tools/boat_analysis/model/install.py`
before `uv sync --locked`; Go 1.25+ is required for the development source build.
An optional `--source /path/to/OpenSysML` uses a local checkout containing the
exact pinned commit. See README.md.

Keep the existing Markdown authoring, scoped SysML view fences, article URLs,
blog import, navigation, and interactive illustrations. Model facts belong in
SysML; prose explains the engineering method. Do not create a separate public
website or framework repository as part of routine Blue Dog work.

Python owns SciPy search, numerical quadrature, geometry, tool integration and
pytest orchestration. The compiled batch adapter serves repeated numerical
evaluations; prefer native OpenSysML APIs for ordinary model operations.

Run `uv run python -m tools.boat_analysis.cli prepare` after changing model,
runtime or dependency inputs, then the relevant pytest checks. Before publishing,
run the full suite and `uv run python -m tools.publishing.build`. Preserve archived
evidence and its source provenance; software regression results are not physical
qualification or approval of an engineering review gate.

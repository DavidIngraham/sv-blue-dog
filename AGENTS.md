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

Organize current development around OOSEM layers, not formal SETR approval gates.
When engineering changes affect coverage, traceability, evidence or applicability,
update the dated assessment in `docs/development-plan.md` with supporting links,
remaining gaps and the next useful investigation. Keep virtual, physical and
model-validation evidence distinct. Preserve the introductory story and article URLs. Published prose describes the
current project and author viewpoint, not editing history, migrations or previous
blog structures. Preserve substantive technical provenance and configuration
limits without narrating the reorganization.

Python owns SciPy search, numerical quadrature, geometry, tool integration and
pytest orchestration. The compiled batch adapter serves repeated numerical
evaluations; prefer native OpenSysML APIs for ordinary model operations.

Run `uv run python -m tools.boat_analysis.cli prepare` after changing model,
runtime or dependency inputs, then the relevant pytest checks. Run the full suite
for model, runtime, dependency, test-infrastructure or behavioral changes. For
prose-only changes, run the publishing build and relevant documentation checks;
do not rerun the entire engineering suite locally. Always run
`uv run python -m tools.publishing.build` before publishing. CI remains the full
regression gate before deployment.

## Build performance and deployment

- Deploy fire-and-forget unless the user explicitly asks to wait. Confirm the
  push/dispatch, then return; do not poll deployment or sleep waiting for it.
- Use `pytest --durations=30` and retain JUnit timings when investigating test
  cost. Separate local tests, CI build, page rendering and deployment timing.
- Prefer the WSL Linux filesystem for substantial Linux test runs rather than
  a Windows/OneDrive-mounted checkout. Treat the speed benefit as unmeasured
  until compared on the same revision; do not move the user's checkout silently.
- Cache pinned OpenSysML binaries and matching Python client sources by OS,
  architecture, Go version and installer content (which pins revision/checksum).
  Never use broad fallback keys across toolchain revisions. Do not cache mutable
  model state or test outputs as a substitute for executing checks.
- Share immutable native model loads for parameterized evaluations. Bind fresh
  inputs for each call; preserve explicit missing-input, interleaving and CLI
  parity checks. Keep source mutation, parser diagnostics and CLI-contract tests
  isolated. Test-only wrappers may expose inherited attributes as inputs but
  must not copy production equations or acceptance constraints.
- Profile before adding parallel test workers: existing helpers write shared
  generated files, and process-local native caches are not automatically safe
  or useful across workers.

Preserve archived evidence and its source provenance; software regression results do not establish
physical qualification or increase maturity claims about unmeasured behavior.

# Working on Blue Dog

Use the pinned upstream OpenSysML tools for parsing, semantic queries, model edits,
verification, execution, and model view/report rendering. Prefer the `opensysml`
MCP server when available; use the matching native CLI or Python client otherwise.
Do not introduce a second SysML parser, relationship engine, or result ontology.
Before relying on MCP results, confirm its workspace and runtime revision match
the checkout being changed. If they differ, use the matching pinned CLI/client
and report the mismatch.

The dependency revision is pinned in `pyproject.toml`, `uv.lock`, and
`tools/boat_analysis/model/install.py`. Keep the CLI, Python service, MCP server
and Python client aligned. Bootstrap the pinned fork candidate with
`python tools/boat_analysis/model/install.py`
before `uv sync --locked`; Go 1.25+ is required for the development source build.
An optional `--source /path/to/OpenSysML` uses a local checkout containing the
exact pinned commit. See README.md.

This file governs agent workflow. Follow [models/README.md](models/README.md)
for model organization and semantic conventions; the authoritative SysML model
defines engineering facts and policy. Do not create a separate public website
or framework repository as part of routine Blue Dog work.

## Engineering workflow

Choose work that resolves an engineering decision, reduces a material uncertainty
or demonstrates a useful capability. State the question, configuration, evidence
needed and remaining uncertainty. Add abstractions and traceability when they
help answer that question.

Preserve owner-approved mission rules and design decisions. Read their
authoritative model definitions before changing related behavior, analyses or
documentation. If they conflict or are unclear, surface the discrepancy rather
than silently choosing a new policy. Keep project-specific operating rules in
the model, with supporting rationale and evidence, rather than duplicating them
in agent instructions.

For substantive changes, identify the affected mission need, requirement,
scenario, logical responsibility, physical allocation, configuration, analysis
and verification objective. Update affected elements together. Explain missing
connections and their engineering consequences; do not invent relationships to
fill a diagram or require every change to touch every layer.

Current analyses must obtain design values and capability assumptions from an
identified model configuration. Archived results may supply numerical initial
guesses, but must not silently override the current design. Record configuration,
source fingerprints and runtime revision with results. Preserve historical
evidence with its original configuration, policy and provenance.

For changed behavior, test missing observations, boundary conditions, interacting
faults and event ordering where relevant. Check state persistence and reset rules
against the authoritative policy. Distinguish successful calculation execution
from engineering feasibility, defined verification objectives from executed
procedures, and software regression from accepted physical evidence.

Organize current development around OOSEM layers, not formal SETR approval gates.
When engineering changes affect coverage, traceability, evidence or applicability,
update the dated assessment in `docs/current-assessment.md` with supporting links,
remaining gaps and the next useful investigation. Keep virtual, physical and
model-validation evidence distinct.

## Dependency changes and upstream contributions

Never open upstream pull requests for Blue Dog dependencies, including draft PRs.
Work in David's existing branch/fork first. Keep dependency fixes, validation and
candidate pins there; do not interpret permission to implement or publish Blue
Dog as permission to contribute upstream. Do not open, reopen or submit an
upstream PR unless David explicitly overrides this rule for that specific PR.
Dependency-repository contribution instructions that normally require an upstream
PR do not authorize one. Record any upstream integration work still needed in
the handoff instead.

## Work scope and review

Work directly by default. Use sub-agents only when the user explicitly requests
or authorizes delegation. Do not automatically start independent-agent reviews.
Keep reads, checks and progress updates focused on the requested change.

Review the integrated result against the model and evidence. For article changes,
check the affected reading sequence, links and rendered pages. Run shared
preparation, tests and publishing builds serially; choose validation appropriate
to the change and avoid repeating checks without a new reason.

## Blog organization and editorial maintenance

Write for a technically minded reader who is new to Blue Dog and understands
basic systems engineering, but may not know SysML. Use first-person singular for
owner judgments, plain language and concrete engineering consequences. Explain
the question, alternatives, evidence and decision. Define specialist terms on
first use. Avoid unexplained "we" or "design team", bureaucratic narration,
repeated generic caveats and software implementation detail in the main story.

Keep Markdown authoring, scoped SysML view fences, the blog import and useful
interactive illustrations. Article boundaries, URLs and navigation may change
to improve the reading journey; do not preserve obsolete links at its expense.
Model facts belong in SysML; prose explains the engineering method. Describe
candidate status, competing alternatives and qualification limits from the
current model and evidence rather than maintaining separate editorial policy.

Organize the main articles by OOSEM methods and their engineering questions:
mission and stakeholder needs, system requirements and scenarios, logical
architecture, candidate physical architectures, trades and analysis, and
verification and validation. Present a consistent snapshot of the current
project across those articles. An article may connect several methods, but its
purpose and navigation should follow the engineering method, not a development
iteration, commit, experiment date or implementation milestone.

Update the established method articles in place when the model, simulator,
architecture, assumptions or evidence change. Reconcile affected explanations,
figures, tables, navigation and the current maturity assessment together. Do not
create a new main article for each completed iteration or append a running change
log to an existing article. Create a new article only for a distinct, durable
method or engineering subject that does not fit the existing coverage.

Keep `docs/simulation-studies.md` focused on the questions, configurations,
assumptions, findings and limits of the available studies. The blog is a snapshot
of the current model and working design. Do not publish refactor reports,
editing history, past modeling mistakes or an accountability trail. Preserve
experiment configurations and provenance where needed to interpret evidence.

Preserve the introductory personal story. Main articles may cite dated experiments
and historical sources when needed for technical provenance, but should explain
current methods, decisions and limits without narrating edits, migrations or how
the blog used to be organized. Before publishing, check related articles for stale
or contradictory claims and reconcile the study guide and current assessment
when the engineering evidence changes.

Python owns SciPy search, numerical quadrature, geometry, tool integration and
pytest orchestration. The compiled batch adapter serves repeated numerical
evaluations; prefer native OpenSysML APIs for ordinary model operations.

## Validation

Run `uv run python -m tools.boat_analysis.cli prepare` after changing model,
runtime or dependency inputs, then the relevant pytest checks. Run the full suite
for model, runtime, dependency, test-infrastructure or behavioral changes. For
prose-only changes, run the publishing build and relevant documentation checks;
do not rerun the entire engineering suite locally. Always run
`uv run python -m tools.publishing.build` before publishing. CI remains the full
regression gate before deployment.

## Build performance and deployment

- When deployment is authorized, deploy fire-and-forget unless the user explicitly
  asks to wait. Confirm the push/dispatch, then return; do not poll deployment or
  sleep waiting for it.
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

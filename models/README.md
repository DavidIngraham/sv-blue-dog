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
- Use `#derivation` for required acceptance outcomes under the parent conditions, and standard `ModelingMetadata::Refinement` (`#refinement dependency`) when the source makes its target more precise. Use plain dependencies with rationale for design choices or motivation. Preserve owner constraints independently of mission success; do not force every obligation under a mission derivation.
- Use native `verify` links for verification cases and `satisfy` for intended design allocations. Unimplemented procedures and unaccepted evidence must not produce a verification pass.
- Put document queries and view definitions in SysML. The Python publisher orchestrates the native tool; it does not reinterpret requirement prose or implement analysis equations.

## Published artifacts

Authored documents may contain `<!-- diagram:name -->` blocks. The publisher replaces only the Mermaid inside those blocks from the corresponding native document; surrounding prose remains authored.

The publisher owns the challenge brief, requirements index/register/context, traceability, energy budget, DFMEA, cruise results, `docs/analysis/` and `docs/figures/`. Do not hand-edit these outputs. The [design guide](../docs/design-guide.md) links each report to its model source and explains the analysis methods.

Focused requirement views include one parent and at most three immediate children. `DiagramLayout::Layout` metadata limits membership; Mermaid lays out retained nodes. Dashed derivation arrows point from derived to original, with originals at the top. The complete graph is only a regression oracle. Tests verify that focused views cover all derivations and the requirement-to-requirement refinements. Small mixed views also show formal criteria, intended design satisfaction and verification. Plain dependencies are available in the generated relationship register; the pinned native GeneralView renderer does not draw them.

GitHub renders native Mermaid Markdown; the blog imports the same repository files. Standalone HTML includes native rendering support and shares a generated stylesheet. `DocumentQueries` and `DiagramLayout` are OpenSysML tooling libraries. Reliability logarithms/exponentials use its non-normative `OpenSysMLMathFunctions` extension.

Update the website publication manifest when adding or removing reader-facing pages. Keep the authored documentation small: explain the design process and method limitations, then link to generated model facts. Keep review logs and temporary planning notes out of tracked docs.

## References

- [OpenSysML](https://github.com/Open-MBEE/OpenSysML)
- [Official SysML v2 release](https://github.com/Systems-Modeling/SysML-v2-Release)
- [Standard modeling metadata](https://github.com/Systems-Modeling/SysML-v2-Release/blob/master/sysml.library/Domain%20Libraries/Metadata/ModelingMetadata.sysml)

Sailing performance uses `sailing-performance.sysml` for inverse polar demand, hull-speed screening and cruise integration. Mathematical figures are rendered from native sensitivity outputs by `scripts/plot_sailing.py`, using the uv-locked Matplotlib dependency; no sailing equations are reimplemented in Python.

Coupled sail, keel and rudder sizing is in `appendage-sizing.sysml`; `sizing-documents.sysml` defines its native report. The sizing objective checks valid computation, while `modeledFit` and `supportedSizing` distinguish numerical fit from accepted evidence. `scripts/plot_sizing.py` plots only native results.

## Coupled design search

The equations and bounds live in `design-physics.sysml` and `design-search.sysml`. SciPy searches design and trim values; the model remains authoritative for physics. `design-search-results.sysml` is generated from the selected saved inputs, and `design-search-documents.sysml` defines the native replay report. Generated subjects are not authored requirements.

The initial C adapter supports Linux with GCC (including WSL). Prepare on either platform with the pinned native CLI, then run the numerical search in a Linux uv environment. A Linux-only workflow is:

```sh
uv sync --locked
uv run python scripts/install_renderer.py
uv run python scripts/prepare_design_search.py
uv run python scripts/solve_design.py --starts 3 --budget 250
uv run python scripts/publish_design_search.py
uv run python scripts/render_requirements.py
uv run pytest -q
uv run python scripts/publish_design_search.py --check
uv run python scripts/render_requirements.py --check
```

When preparing on Windows and solving in WSL, use a separate uv environment such as `UV_PROJECT_ENVIRONMENT=.tools/solver-venv`; never reuse the Windows `.venv` binaries in Linux. Both use `uv.lock`. The C source, shared library, exported contract and environments remain ignored in `.tools/`. The ABI adapter copies outputs before the next native call and serializes runtime access.

The search record includes normalized source hashes, dependency lock, renderer pin and driver hashes. Changes to these inputs require preparation and a new search; the publisher refuses stale results. Publishing replays the saved candidates but does not silently launch a new optimization. Test the C adapter in Linux; Windows pytest explicitly skips that adapter test file while still comparing saved compiled results against native interpretation. Read [the search method and limitations](../docs/design-search.md) before interpreting numerical feasibility as design evidence.

### Hull-length sensitivity

`hull-length-study.sysml` removes only the exploratory length cap, using the mass-implied ceiling while retaining the original physics and other bounds. Its saved subjects and native document are loaded explicitly by the publisher; they do not change baseline search inputs.

After preparing the base C kernel, run the study preparation with the native CLI, the search in Linux/GCC, then publication with the native CLI:

```sh
uv run python -m scripts.study_hull_length --prepare
uv run python -m scripts.study_hull_length --starts 5 --sweep-starts 3 --budget 350
uv run python -m scripts.study_hull_length --publish
uv run python scripts/render_requirements.py
```

The free-length studies minimize length only if a numerically feasible candidate exists; otherwise they retain the best progress found. Fixed-length cases vary the remaining design and trim values. Both the original result hash and the study sources are checked before publishing the comparison.

# SV Blue Dog

Named after my blue heeler, Ozzy, Blue Dog is an autonomous sailboat project exploring sailing, desktop manufacturing and complete-system design. The hope is a small, dog-sized vessel puttering independently around the surface of a river or the ocean. The current design mission is one finite Trans-Gorge round trip. Hawaii remains a separate future mission with its own constraints.

Start with the [project journey](docs/restarting-sv-blue-dog.md), [development series](docs/index.md), and [focused requirements](docs/requirements.md).

The [development plan](docs/development-plan.md) connects mission intent, simulation, physical evidence and lightweight review gates across successive prototypes.

## Repository

- `models/`: authoritative requirements, architecture, rationale, analysis contracts and configurations; reusable physics under `models/libraries/`.
- `tools/boat_analysis/`: numerical search, geometry adapters, VSP integration and evidence handling.
- `docs/`: authored method and journey pages with inline SysML views.
- `tools/publishing/`: native-view orchestration and website generation.
- `evidence/`: immutable recorded runs with provenance.
- `tests/`: model semantics and numerical/software regression checks.
- [CAD](cad/): the earlier manufacturing and wing-sail prototype, distinct from the challenge vessel.

## Work locally

```sh
uv sync --locked
uv run python -m tools.boat_analysis.cli install
uv run python -m tools.boat_analysis.cli validate
uv run python -m tools.boat_analysis.cli prepare
uv run python -m tools.publishing.build
uv run pytest -q
```

Python uses the package-free uv project. The Python client, CLI, service and MCP server use upstream development revision `62b904178c1c8281439f6b0445c739547c89ae9a`. Install Go 1.25+ for the source installer and a GNU-compatible C compiler for numerical preparation. The installer verifies the upstream source archive before building the three native executables. See [modeling conventions](models/README.md), [publishing](docs/publishing.md), and [sizing methods](docs/sizing.md).

This pin includes the native runtime MCP tools. The later upstream short-name-resolution merge `b8e897e0e` caused a severe validation slowdown on the complete Blue Dog model during migration. Update the pin only after checking full-model validation, numerical regressions and document rendering together; the Python client and native executables must use the same revision.

For an agent host, register `.tools/develop-62b904178/sysml-mcp` (Windows: `sysml-mcp.exe`) with `-root` pointing to this repository's `models` directory. Prefer its native model queries, verification, execution and rendering tools. The blog retains its authored Markdown, scoped views and existing navigation; OpenSysML supplies model semantics and diagram/report rendering.

Generated pages belong in build artifacts. The model owns design facts; documentation explains how we reason about them. Current sizing uses explicit conservative aerodynamic assumptions and refined scenario replay; VSPAERO supplies exploratory finite-wing trends. Recorded outcomes are conditional evidence, not a qualified vessel design.

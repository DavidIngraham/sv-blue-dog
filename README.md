# SV Blue Dog

An autonomous sailboat project exploring sailing, desktop manufacturing and complete-system design. The independent Trans-Gorge challenge is the proving ground for a longer-term Hawaii objective.

Start with the [project journey](docs/restarting-sv-blue-dog.md), [design methods](docs/index.md), and [focused requirements](docs/requirements.md).

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
uv run python -m tools.publishing.build
uv run pytest -q
```

Python uses the package-free uv project. The native OpenSysML renderer is pinned separately. See [modeling conventions](models/README.md), [publishing](docs/publishing.md), and [sizing methods](docs/sizing.md).

Generated pages belong in build artifacts. The model owns design facts; documentation explains how we reason about them. Recorded exploratory outcomes are conditional evidence, not a qualified vessel design.

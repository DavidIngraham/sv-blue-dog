# Authoring and publishing

Our Markdown describes methods and design reasoning. Engineering definitions, assumptions and rationale belong in `models/`. Each page imports those definitions into a small native view; the publisher resolves the view with OpenSysML and inserts its diagram and requirement statements.

## Inline views

Use a fenced `sysml-view Package::viewName direction=BT` block containing a uniquely named package, imports, and a scoped view. Expose existing model elements and provide layout metadata to keep the diagram focused. Do not declare requirements or calculations in a documentation fence. For a view exposing requirement usages, add `statements=true` to include their authoritative statements below the diagram. Omit that option for mixed architecture/verification views. See [the modeling method](methods/modeling.md) for a working example.

The direction follows the semantic arrows. Derivation arrows point from derived requirements toward their source, so `BT` places source requirements above their children. Keep one engineering question per diagram.

Use an empty `sysml-report Package::Document` fence to include a native document query. Reports should support a specific discussion rather than repeat the entire model.

## Local build

From the repository root:

```sh
uv sync --locked
uv run python -m tools.boat_analysis.cli install
uv run python -m tools.publishing.build
```

The generated site is written to `build/site`; rendered Markdown for the blog is under `build/site/imports/docs`. Generated files are build artifacts. Author the source pages and models, then rebuild them together. Raw GitHub Markdown displays the view source; the published site displays the resolved diagrams.

A documentation build never runs optimization or VSP. Recorded analysis evidence is retained with its original provenance, and current results must identify their inputs and source revision. See [the sizing method](sizing.md) and [recorded outcomes](results.md).

## GitHub Actions

The model-and-documentation workflow validates and prepares native calculations, checks recorded provenance, runs pytest and builds the site. Pull requests produce a Pages artifact; a successful main-branch run deploys it. Action revisions, uv and the native tool are pinned. Full history is fetched because archived evidence is checked against its original source revision.

The personal blog keeps its existing article identifiers and reads rendered Markdown from the project site's `imports/` directory. Authored pages stay in this repository. Legacy page paths redirect to current methods; superseded numerical studies remain available through Git history rather than masquerading as current results.

Aerodynamic plots are regenerated from hash-checked archived JSON by `tools.boat_analysis.evidence.aerodynamics` and published under `assets/vsp`. Native geometry screenshots and the corresponding VSP model are retained as evidence. The plot build does not launch OpenVSP.

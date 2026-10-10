# SV Blue Dog

An autonomous sailing project exploring sailing, desktop manufacturing and complete-system design. The model connects the independent Trans-Gorge challenge to the longer-term Hawaii objective.

- [Design process and current model](docs/design-guide.md)
- [Generated challenge brief](docs/challenge-brief.md)
- [Focused requirement views](docs/requirements-views.md)
- [Modeling and publishing](models/README.md)
- [Project article](docs/restarting-sv-blue-dog.md)

## Repository

`models/` holds the authoritative SysML. `docs/` contains a short design guide, analysis methods and generated reports. `scripts/` publishes with native OpenSysML; `tests/` exercises model behavior and documentation consistency. Python dependencies use the package-free uv project.

The [CAD files](cad/) are a manufacturing and wing-sail prototype, separate from the challenge-vessel design. Assemblies, parts and exchange files remain together to preserve references. Start with [SV Bluedog.SLDASM](cad/SV%20Bluedog.SLDASM); physical build status and geometry qualification are not established by this model.

The GitHub Pages blog imports Markdown from this repository. Requirement statements, model counts and numerical results belong in generated artifacts, not duplicated prose. Publishing commands and source conventions are in the modeling guide.

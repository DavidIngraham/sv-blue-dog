# SV Blue Dog

A small sailing-robot project balancing efficiency, reliability, and ease of manufacture.

The recovered December 2023 brief describes a one-metre monohull with a printable hull, ballasted fin keel, low-power electronics, and self-righting and failure-recovery goals. These are design intentions; build and test status still need documenting.

- [Project status and restart checklist](docs/project-status.md)
- [Article: picking up a small sailing robot again](docs/restarting-sv-blue-dog.md)

## Folder layout

- `cad/`: SolidWorks assemblies and parts, plus manufacturing and exchange files.
- `docs/`: project status, restart checklist, and the website article.

## CAD

The SolidWorks files and their STEP, IGES, and 3MF exports live together in [`cad/`](cad/) to preserve relative assembly paths. Start with [`cad/SV Bluedog.SLDASM`](cad/SV%20Bluedog.SLDASM); the mast assembly is [`cad/BluedogMast.SLDASM`](cad/BluedogMast.SLDASM). Assembly dependencies and geometry have not yet been validated. STEP, IGES, and 3MF files are retained as supplied.

SolidWorks lock files are ignored. CAD files are stored as ordinary Git binary files in this initial snapshot; the largest is approximately 7.4 MB. Avoid committing automatic backups or repeated export copies.

## Publishing

The GitHub Pages site reads `docs/restarting-sv-blue-dog.md` from this repository through its publication manifest. Article edits belong here alongside the project work.

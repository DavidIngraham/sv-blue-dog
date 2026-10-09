# SV Blue Dog

A small sailing-robot project balancing efficiency, reliability, and ease of manufacture.

The recovered December 2023 brief describes a one-metre monohull with a printable hull, ballasted fin keel, low-power electronics, and self-righting and failure-recovery goals. These are design intentions; build and test status still need documenting.

- [Project status and restart checklist](docs/project-status.md)
- [Article: picking up a small sailing robot again](docs/restarting-sv-blue-dog.md)

## CAD

The original SolidWorks files remain at the repository root to preserve their relative assembly paths. The primary assembly filename is `SV Bluedog.SLDASM`; `BluedogMast.SLDASM` is also included. Assembly dependencies and geometry have not yet been validated. STEP, IGES, and 3MF files are retained as supplied.

SolidWorks lock files are ignored. CAD files are stored as ordinary Git binary files in this initial snapshot; the largest is approximately 7.4 MB. Avoid committing automatic backups or repeated export copies.

## Publishing

The GitHub Pages site reads `docs/restarting-sv-blue-dog.md` from this repository through its publication manifest. Article edits belong here alongside the project work.

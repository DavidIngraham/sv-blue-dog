"""Portable identities for prepared models and the runtime that executes them."""
import hashlib
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def runtime_sources():
    root = Path(__file__).parent
    return {path.relative_to(root).as_posix(): digest(path)
            for path in sorted(root.rglob('*.py'))}


def project_root(manifest, contract):
    if contract.get('schemaVersion') != 2:
        raise ValueError('Unsupported prepared manifest; prepare the project again')
    return (manifest.parent / contract['projectRoot']).resolve()

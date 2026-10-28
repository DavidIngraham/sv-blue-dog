"""Read and update exact generated sections in the canonical project document.

Markers are an authoring boundary, not a SysML parser. Native OpenSysML owns the
model's package hierarchy and semantics; generators own only their marked bytes.
"""
from pathlib import Path
import tempfile

from ..model.runtime import ROOT


SECTIONS = {
    'coupled-2026-10-10': 'BlueDog::Evidence::RecordedSizing',
    'current-sizing': 'BlueDog::Evidence::CurrentSizing',
    'finite-passage-sizing': 'BlueDog::Evidence::FinitePassageSizing',
    'gorge-wind': 'BlueDog::Evidence::WindObservations',
    'sizing-continuation': 'BlueDog::Evidence::SizingContinuation',
    'srr-current': 'BlueDog::Evidence::SRRCurrent',
    'srr-frontier': 'BlueDog::Evidence::SRRFrontier',
}
INDENT = b'        '
BEGIN = b'// BEGIN GENERATED PROJECTION: '
END = b'// END GENERATED PROJECTION: '


def projection_path() -> Path:
    return ROOT/'models/blue-dog.sysml'


def projection_package(name: str) -> str:
    """Accept retained generator arguments without treating aliases as model IDs."""
    for canonical in SECTIONS.values():
        leaf = canonical.rsplit('::', 1)[-1]
        if name in (canonical, leaf, 'BlueDog'+leaf):
            return canonical
    # Standalone exports historically accepted a caller-chosen package. This
    # label is authoring intent, never a discovery rule or an executable value.
    if not all(part.isidentifier() for part in name.split('::')):
        raise ValueError('Expected a package identifier for standalone projection export')
    return name


def _bounds(content: bytes, key: str) -> tuple[int, int]:
    if key not in SECTIONS:
        raise ValueError('Unknown generated projection section: '+str(key))
    begin = INDENT+BEGIN+key.encode('ascii')
    end = INDENT+END+key.encode('ascii')
    starts = []
    stops = []
    offset = 0
    for line in content.splitlines(keepends=True):
        literal = line.rstrip(b'\r\n')
        if literal == begin:
            starts.append(offset+len(line))
        if literal == end:
            stops.append(offset)
        offset += len(line)
    if len(starts) != 1 or len(stops) != 1:
        raise ValueError(f'{key}: expected one begin/end generated projection marker pair; found {len(starts)}/{len(stops)}')
    if starts[0] > stops[0]:
        raise ValueError(f'{key}: generated projection end marker precedes begin marker')
    if BEGIN in content[starts[0]:stops[0]] or END in content[starts[0]:stops[0]]:
        raise ValueError(f'{key}: nested or overlapping generated projection markers')
    return starts[0], stops[0]


def _render(source: str) -> bytes:
    content = source.encode('utf-8')
    if BEGIN in content or END in content:
        raise ValueError('Generated projection content must not contain projection markers')
    if b'\r' in content:
        raise ValueError('Generated projection content must use LF newlines')
    if content and not content.endswith(b'\n'):
        content += b'\n'
    return b''.join(INDENT+line if line.strip() else line for line in content.splitlines(keepends=True))


def read_projection(key: str, *, path: str | Path | None = None) -> str:
    path = projection_path() if path is None else Path(path)
    content = path.read_bytes()
    start, stop = _bounds(content, key)
    lines = []
    for line in content[start:stop].splitlines(keepends=True):
        if line.strip() and not line.startswith(INDENT):
            raise ValueError(f'{path}: {key}: generated projection content lacks its fixed indentation')
        lines.append(line[len(INDENT):] if line.startswith(INDENT) else line)
    return b''.join(lines).decode('utf-8')


def check_projection(key: str, source: str, *, path: str | Path | None = None) -> None:
    path = projection_path() if path is None else Path(path)
    content = path.read_bytes()
    start, stop = _bounds(content, key)
    if content[start:stop] != _render(source):
        raise ValueError(f'{path}: stale generated projection section: {key}')


def write_projection(key: str, source: str, *, path: str | Path | None = None) -> Path:
    path = projection_path() if path is None else Path(path)
    content = path.read_bytes()
    start, stop = _bounds(content, key)
    replacement = _render(source)
    if content[start:stop] == replacement:
        return path
    updated = content[:start]+replacement+content[stop:]
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name+'.', suffix='.tmp', delete=False) as stream:
        staged = Path(stream.name)
        stream.write(updated)
    try:
        if path.read_bytes() != content:
            raise ValueError(f'{path}: canonical model changed while updating generated projection: {key}')
        staged.replace(path)
    finally:
        staged.unlink(missing_ok=True)
    return path

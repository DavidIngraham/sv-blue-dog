"""Generated evidence updates must preserve the surrounding authored model."""
from pathlib import Path

import pytest

from tools.boat_analysis.evidence.projection import (
    SECTIONS, check_projection, projection_package, read_projection, write_projection,
)


def block(key, source='package Previous {}\n'):
    indented = ''.join('        '+line if line.strip() else line
                       for line in source.splitlines(keepends=True))
    return (f'        // BEGIN GENERATED PROJECTION: {key}\n'+indented
            +f'        // END GENERATED PROJECTION: {key}\n').encode()


def test_each_declared_projection_updates_only_its_own_bytes(tmp_path):
    path = tmp_path/'blue-dog.sysml'
    keys = list(SECTIONS)
    original = b'// authored prefix with CRLF\r\npackage BlueDog {\n    package Evidence {\n'
    original += b''.join(block(key) for key in keys)
    original += b'    }\n    package Authored { /* preserve exactly */ }\n}\n'
    path.write_bytes(original)
    for key in keys:
        before = path.read_bytes()
        source = 'package '+SECTIONS[key].rsplit('::', 1)[-1]+' {\n    attribute recorded = 1.2345678901234567;\n}\n'
        old = block(key)
        new = block(key, source)
        write_projection(key, source, path=path)
        assert path.read_bytes() == before.replace(old, new, 1)
        assert read_projection(key, path=path) == source
        check_projection(key, source, path=path)
        first = path.read_bytes()
        modified_at = path.stat().st_mtime_ns
        write_projection(key, source, path=path)
        assert path.read_bytes() == first
        assert path.stat().st_mtime_ns == modified_at


@pytest.mark.parametrize('content', [
    b'package BlueDog {}\n',
    block('current-sizing')+block('current-sizing'),
    b'        // END GENERATED PROJECTION: current-sizing\n'
    b'        // BEGIN GENERATED PROJECTION: current-sizing\n',
    b'        // BEGIN GENERATED PROJECTION: current-sizing\n'
    +block('srr-current')+
    b'        // END GENERATED PROJECTION: current-sizing\n',
])
def test_missing_duplicate_reversed_or_overlapping_markers_cannot_overwrite_model(tmp_path, content):
    path = tmp_path/'blue-dog.sysml'
    path.write_bytes(content)
    with pytest.raises(ValueError, match='marker'):
        write_projection('current-sizing', 'package Replacement {}\n', path=path)
    assert path.read_bytes() == content


@pytest.mark.parametrize('marker', ['// BEGIN GENERATED PROJECTION: nested', '// END GENERATED PROJECTION: nested'])
def test_projection_content_cannot_inject_section_boundaries(tmp_path, marker):
    path = tmp_path/'blue-dog.sysml'
    original = block('current-sizing')
    path.write_bytes(original)
    with pytest.raises(ValueError, match='must not contain'):
        write_projection('current-sizing', marker+'\n', path=path)
    assert path.read_bytes() == original


def test_freshness_check_reports_section_without_modifying_canonical_document(tmp_path):
    path = tmp_path/'blue-dog.sysml'
    original = block('current-sizing')
    path.write_bytes(original)
    with pytest.raises(ValueError, match='stale.*current-sizing'):
        check_projection('current-sizing', 'package Changed {}\n', path=path)
    assert path.read_bytes() == original


def test_unknown_section_and_damaged_indentation_are_explicit(tmp_path):
    path = tmp_path/'blue-dog.sysml'
    content = block('current-sizing').replace(b'        package Previous', b'package Previous')
    path.write_bytes(content)
    with pytest.raises(ValueError, match='Unknown'):
        read_projection('not-a-declared-section', path=path)
    with pytest.raises(ValueError, match='indentation'):
        read_projection('current-sizing', path=path)
    assert path.read_bytes() == content


def test_generator_package_arguments_preserve_legacy_identity_without_qualified_declarations():
    for canonical in SECTIONS.values():
        leaf = canonical.rsplit('::', 1)[-1]
        assert projection_package(canonical) == canonical
        assert projection_package(leaf) == canonical
        assert projection_package('BlueDog'+leaf) == canonical
    assert projection_package('StandaloneExport') == 'StandaloneExport'
    with pytest.raises(ValueError):
        projection_package('Export {} package Injected')

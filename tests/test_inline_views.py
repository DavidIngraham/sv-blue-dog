from pathlib import Path
import pytest

from tools.boat_analysis.model.runtime import ROOT
from tools.publishing.build import render_page
from tools.publishing.views import ViewBlock


def test_view_blocks_cannot_redeclare_requirements():
    with pytest.raises(ValueError, match="engineering elements"):
        ViewBlock.parse("sysml-view Page::view", "package Page { requirement copied; }")


def test_bad_view_options_fail():
    with pytest.raises(ValueError):
        ViewBlock.parse("sysml-view Page::view direction=sideways", "")


def test_inline_view_resolves_actual_refinement_and_statements(tmp_path):
    source = (ROOT / "docs/methods/modeling.md").read_text(encoding="utf-8")
    result = render_page(source, tmp_path)
    assert 'class="mermaid"' in result
    assert 'refine' in result
    assert 'The vessel shall cross the configured The Dalles departure' in result
    assert 'flowchart BT' in result
    assert 'BlueDogRequirements::communications' not in result
    assert 'sysml-view' not in result


def test_unresolved_model_reference_fails_build(tmp_path):
    source = '''```sysml-view MissingPage::view
package MissingPage {
 private import StandardViewDefinitions::*;
 view view : GeneralView { expose Missing::requirement; }
}
```'''
    with pytest.raises(RuntimeError, match="OpenSysML"):
        render_page(source, tmp_path)


def test_ordinary_code_fence_is_preserved(tmp_path):
    result = render_page('```python\nprint("test")\n```', tmp_path)
    assert '<code class="language-python">' in result
    assert '</code></pre>' in result


def test_rebuild_removes_stale_pages_and_exports_blog_markdown(tmp_path):
    from tools.publishing.build import build
    source, output = tmp_path / 'authored', tmp_path / 'site'
    source.mkdir()
    (source / 'first.md').write_text('# First\n')
    build(source, output)
    (source / 'first.md').unlink()
    (source / 'second.md').write_text('# Second\n')
    build(source, output)
    assert not (output / 'first.html').exists()
    assert not (output / 'imports/docs/first.md').exists()
    assert (output / 'imports/docs/second.md').read_text() == '# Second\n'


def test_failed_build_preserves_last_complete_site(tmp_path):
    from tools.publishing.build import build
    source, output = tmp_path / 'authored', tmp_path / 'site'
    source.mkdir()
    page = source / 'index.md'
    page.write_text('# Complete\n')
    build(source, output)
    before = (output / 'index.html').read_bytes()
    page.write_text('# Broken\n[missing](not-a-real-source-file.md)\n')
    with pytest.raises(ValueError, match='Broken source link'):
        build(source, output)
    assert (output / 'index.html').read_bytes() == before

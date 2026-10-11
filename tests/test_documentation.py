"""Keep reader navigation valid when documents are consolidated or regenerated."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def test_repository_markdown_links_resolve():
    pages = [ROOT / 'README.md', *ROOT.joinpath('docs').rglob('*.md'),
             *ROOT.joinpath('models').rglob('*.md')]
    missing = []
    for page in pages:
        text = re.sub(r'```.*?```', '', page.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\]\((<[^>]+>|[^\s)]+)\)', text):
            target = target.strip('<>')
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = (page.parent / unquote(url.path)).resolve()
            if not path.exists():
                missing.append(f'{page.relative_to(ROOT)} -> {target}')
    assert not missing, '\n'.join(missing)


def test_generated_index_links_every_focused_requirement_page():
    index = (ROOT / 'docs/requirements.md').read_text(encoding='utf-8')
    links = set(re.findall(r'requirements/(requirements-[a-z]+\.md)', index))
    pages = {p.name for p in (ROOT / 'docs/requirements').glob('requirements-*.md')}
    assert links == pages
    assert len(pages) == 6


def test_legacy_requirement_links_reach_topic_sections(rendered_site):
    import json
    redirects = json.loads((ROOT / 'tools/publishing/redirects.json').read_text())
    legacy = {old: new for old, new in redirects.items() if old.startswith('requirements/')}
    assert len(legacy) == 50
    for old, new in legacy.items():
        destination = urlsplit(new)
        assert destination.fragment
        html = (rendered_site / Path(destination.path).with_suffix('.html')).read_text()
        assert f'id="{destination.fragment}"' in html
        redirect = (rendered_site / Path(old).with_suffix('.html')).read_text()
        assert '#' + destination.fragment in redirect

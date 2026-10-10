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
    index = (ROOT / 'docs/requirements-views.md').read_text(encoding='utf-8')
    links = set(re.findall(r'figures/(requirements-[a-z]-[0-9]+\.md)', index))
    pages = {p.name for p in (ROOT / 'docs/figures').glob('requirements-*.md')}
    assert links == pages

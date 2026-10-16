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


def test_rendered_internal_links_and_fragments_resolve(rendered_site):
    from html.parser import HTMLParser

    class Links(HTMLParser):
        def __init__(self, text):
            super().__init__()
            self.links, self.ids = [], set()
            self.feed(text)

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'id' in attrs:
                self.ids.add(attrs['id'])
            if tag == 'a' and 'href' in attrs:
                self.links.append(attrs['href'])

    pages = {p.resolve(): Links(p.read_text()) for p in rendered_site.rglob('*.html')}
    missing = []
    for page, parsed in pages.items():
        for link in parsed.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            if target not in pages or (url.fragment and unquote(url.fragment) not in pages[target].ids):
                missing.append(f'{page.relative_to(rendered_site)} -> {link}')
    assert not missing, '\n'.join(missing)

"""Build authored Markdown, native views and reports into Pages and blog imports."""
import argparse
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit, unquote

from markdown_it import MarkdownIt
from tools.boat_analysis.model.runtime import ROOT
from .views import ViewBlock, render_blocks

PARSER = MarkdownIt("commonmark", {"html": True}).enable("table")
KINDS = {"sysml-view", "sysml-report"}
REPOSITORY = "https://github.com/DavidIngraham/sv-blue-dog"


def blocks(source):
    return [t for t in PARSER.parse(source) if t.type == "fence" and t.info.split()[:1] and t.info.split()[0] in KINDS]


def materialize(source, outputs):
    lines = source.splitlines(keepends=True)
    tokens = blocks(source)
    if len(tokens) != len(outputs):
        raise ValueError("Every native block must produce exactly one output")
    for token, output in reversed(list(zip(tokens, outputs))):
        start, end = token.map
        if token.info.startswith("sysml-report"):
            output = readable_report(output)
            output = re.sub(r"(?m)^# (.+)$", r"### \1", output)
        # Native exports do not supply accessible names. Use the authored context,
        # keeping the semantic graph itself entirely tool-generated.
        preceding = "".join(lines[:start])
        headings = re.findall(r"(?m)^#{1,6} (.+)$", preceding)
        title = headings[-1] if headings else "Model relationships"
        paragraphs = re.sub(r"```.*?```", "", preceding, flags=re.S).split("\n\n")
        prose = [p.strip() for p in paragraphs if p.strip() and not p.lstrip().startswith(("#", "<", "|"))]
        description = prose[-1] if prose else "Follow the named model elements and labeled relationships."
        description = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", description)
        description = re.sub(r"\s+", " ", description).replace("{", "(").replace("}", ")")
        output = re.sub(r"(?m)^(flowchart (?:TB|BT|LR|RL|TD))\s*$",
                        lambda m: m[1] + "\n    accTitle: " + title + "\n    accDescr: " + description, output)
        lines[start:end] = [re.sub(r"(?m)^#\s*$\n?", "", output).strip() + "\n"]
    return "".join(lines)


def readable_report(output):
    """Format native Markdown tables for readers without changing model/evidence data."""
    def cell(value):
        clean = value.strip()
        if clean in {"true", "false"}:
            return " " + {"true": "Yes", "false": "No"}[clean] + " "
        if re.fullmatch(r"-?\d+\.\d{5,}(?:[eE][+-]?\d+)?", clean):
            return f" {float(clean):.4g} "
        return re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    return "\n".join("|".join(cell(c) for c in line.split("|")) if line.startswith("|") else line
                     for line in output.splitlines())


def body_html(markdown, link=None):
    tokens = PARSER.parse(markdown)
    used = set()
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            label = tokens[index + 1].content
            base = re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", label.lower().strip())) or "section"
            slug, suffix = base, 1
            while slug in used:
                slug, suffix = f"{base}-{suffix}", suffix + 1
            used.add(slug)
            token.attrSet("id", slug)
    def visit(items):
        for token in items:
            key = "href" if token.type == "link_open" else "src" if token.type == "image" else None
            if key and link:
                token.attrSet(key, link(token.attrGet(key), token.type == "image"))
            if token.children:
                visit(token.children)
    visit(tokens)
    body = PARSER.renderer.render(tokens, PARSER.options, {})
    body = body.replace('<pre><code class="language-mermaid">', '<pre class="mermaid">')
    return re.sub(r'(<pre class="mermaid">.*?)</code></pre>', r'\1</pre>', body, flags=re.S)


def render_page(source, directory):
    selected = [ViewBlock.parse(t.info, t.content) for t in blocks(source)]
    return body_html(materialize(source, render_blocks(selected, directory)))


def revision():
    return os.environ.get("GITHUB_SHA") or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def page_link(page, target, image, redirects, rev):
    url = urlsplit(target)
    if url.scheme or url.netloc or not url.path:
        return target
    path = posixpath.normpath(posixpath.join("docs", page.parent.as_posix(), unquote(url.path)))
    suffix = ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")
    if path.startswith("docs/"):
        relative = path[5:]
        relative = redirects.get(relative, relative)
        if '#' in relative:
            relative, anchor = relative.split('#', 1)
            suffix = '#' + anchor
        if relative.endswith(".md") and (ROOT / "docs" / relative).is_file():
            return posixpath.relpath(str(PurePosixPath(relative).with_suffix(".html")), page.parent.as_posix()) + suffix
    local = (ROOT / path).resolve()
    if not local.is_relative_to(ROOT) or not local.exists():
        raise ValueError(f"Broken source link in {page}: {target}")
    if image:
        return f"https://raw.githubusercontent.com/DavidIngraham/sv-blue-dog/{rev}/{path}" + suffix
    return f"{REPOSITORY}/{'tree' if local.is_dir() else 'blob'}/{rev}/{path}" + suffix


def document(title, body, home, source):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · SV Blue Dog</title>
<style>body{{font:17px/1.65 system-ui;max-width:1120px;margin:2rem auto;padding:0 1.2rem;color:#183047}}nav,footer{{font-size:.9rem;padding:1rem 0;border-bottom:1px solid #ccd}}footer{{border-top:1px solid #ccd;border-bottom:0;margin-top:3rem}}h1,h2,h3{{line-height:1.25}}pre{{overflow:auto;background:#f4f7fa;padding:1rem}}table{{border-collapse:collapse;display:block;overflow:auto}}td,th{{border:1px solid #bbc;padding:.45rem;text-align:left}}img{{max-width:100%;height:auto}}a{{color:#145b90}}.mermaid{{background:white;text-align:center}}.mermaid svg{{max-width:none;height:auto}}.diagram-viewport{{overflow:auto;border:1px solid #dde;max-height:85vh}}.diagram-controls{{display:flex;gap:.5rem;margin:.4rem 0}}button{{font:inherit;padding:.2rem .7rem}}dt{{font-weight:600}}dd{{margin-bottom:1rem}}.diagram-error{{color:#8b2315}}</style></head>
<body><nav><a href="{escape(home)}">SV Blue Dog</a> · <a href="{escape(source)}">Edit this page</a></nav><main>{body}</main>
<footer>Views and statements are generated from SysML. Numerical evidence is conditional; design allocations are not verification verdicts.</footer>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false,securityLevel:'strict'}});
try {{
  await mermaid.run();
  for (const drawing of document.querySelectorAll('.mermaid svg')) {{
    const viewport = drawing.closest('.mermaid');
    viewport.classList.add('diagram-viewport'); viewport.tabIndex = 0;
    viewport.setAttribute('aria-label', 'Model diagram; scroll to explore');
    const controls = document.createElement('div'); controls.className = 'diagram-controls';
    viewport.before(controls);
    const width = drawing.viewBox.baseVal.width; let scale = 1;
    const resize = next => {{ scale = Math.max(.05, Math.min(3, next)); drawing.style.width = `${{width * scale}}px`; }};
    for (const [label, action] of [
      ['Zoom in', () => resize(scale * 1.5)], ['Zoom out', () => resize(scale / 1.5)],
      ['Fit', () => resize(viewport.clientWidth / width)], ['Actual size', () => resize(1)]
    ]) {{ const button = document.createElement('button'); button.textContent = label; button.onclick = action; controls.append(button); }}
    if (!drawing.querySelector('title')) {{
      const title = document.createElementNS('http://www.w3.org/2000/svg','title');
      title.id = `diagram-title-${{[...document.querySelectorAll('.mermaid svg')].indexOf(drawing)}}`;
      title.textContent = 'Development plan: design, simulation and physical evidence';
      drawing.prepend(title); drawing.setAttribute('aria-labelledby',title.id);
      const desc = document.createElementNS('http://www.w3.org/2000/svg','desc');
      desc.id = title.id + '-description';
      desc.textContent = 'Read down the left from mission through criteria, subsystems and detail to build, then up the right through component and subsystem tests to vessel and mission validation. The virtual vessel checks requirements early and supplies physical test scenarios. Cross-V links pair intent with evidence.';
      drawing.prepend(desc); drawing.setAttribute('aria-describedby',desc.id);
    }}
    drawing.setAttribute('role','img');
    const fit = () => resize(Math.min(1, (viewport.clientWidth || document.querySelector('main').clientWidth) / width));
    fit(); viewport.closest('details')?.addEventListener('toggle', fit);
    window.addEventListener('resize', fit);
  }}
  const reveal = () => {{
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    for (let parent = target?.parentElement; parent; parent = parent.parentElement) {{
      if (parent.tagName === 'DETAILS') parent.open = true;
    }}
    target?.scrollIntoView();
  }};
  reveal(); window.addEventListener('hashchange', reveal);
  document.documentElement.dataset.diagrams='ready';
}}
catch (error) {{ document.documentElement.dataset.diagrams='failed'; console.error(error); }}
</script></body></html>'''


def _build(source_dir, output_dir):
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()
    if output_dir == source_dir or output_dir.is_relative_to(source_dir):
        raise ValueError("Build output must be outside authored documentation")
    pages = sorted(source_dir.rglob("*.md"))
    sources = [p.read_text(encoding="utf-8") for p in pages]
    selected = [ViewBlock.parse(t.info, t.content) for s in sources for t in blocks(s)]
    (ROOT / ".tools").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="site-", dir=ROOT / ".tools") as scratch:
        outputs = iter(render_blocks(selected, Path(scratch)))
    output_dir.mkdir(parents=True, exist_ok=True)
    redirects = json.loads((ROOT / "tools/publishing/redirects.json").read_text(encoding="utf-8")) if source_dir == (ROOT / "docs").resolve() else {}
    if source_dir == (ROOT / "docs").resolve():
        from tools.boat_analysis.evidence.aerodynamics import render
        render(output_dir / "assets/vsp")
        from .concepts import render as render_concepts
        render_concepts(output_dir / "assets/concepts")
        from .design_explorer import render as render_explorer
        render_explorer(output_dir / "assets/design-explorer")
        from .risk_cube import render as render_risk_cube
        render_risk_cube(output_dir / "assets/risk")
        from .development_v import render as render_development_v
        render_development_v(output_dir / "assets/development")
    rev = revision()
    rendered = {}
    for path, source in zip(pages, sources):
        relative = PurePosixPath(path.relative_to(source_dir).as_posix())
        text = materialize(source, [next(outputs) for _ in blocks(source)])
        rendered[relative.as_posix()] = text
        body = body_html(text, lambda target, image: page_link(relative, target, image, redirects, rev))
        title = next((t.children[0].content for t in PARSER.parse(source) if t.type == "inline" and t.children), path.stem)
        target = output_dir / relative.with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(document(title, body, posixpath.relpath("index.html", relative.parent.as_posix()), f"{REPOSITORY}/blob/{rev}/docs/{relative}"), encoding="utf-8")
        imported = output_dir / "imports/docs" / relative
        imported.parent.mkdir(parents=True, exist_ok=True)
        imported.write_text(text, encoding="utf-8")
    for old, new in redirects.items():
        destination = urlsplit(new)
        if destination.path not in rendered:
            raise ValueError(f"Redirect target absent: {old} -> {new}")
        target = output_dir / PurePosixPath(old).with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        href = posixpath.relpath(str(PurePosixPath(destination.path).with_suffix(".html")), PurePosixPath(old).parent.as_posix())
        if destination.fragment:
            href += '#' + destination.fragment
        target.write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={escape(href)}"><a href="{escape(href)}">This page moved</a>', encoding="utf-8")
        imported = output_dir / "imports/docs" / old
        imported.parent.mkdir(parents=True, exist_ok=True)
        imported.write_text("# This page moved\n\n[Continue to the current method](" + posixpath.relpath(new, PurePosixPath(old).parent.as_posix()) + ").\n", encoding="utf-8")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "build.json").write_text(json.dumps({"revision": rev, "pages": sorted(rendered), "viewCount": len(selected)}, indent=2) + "\n", encoding="utf-8")
    return pages



def build(source_dir, output_dir):
    """Publish a complete build atomically enough to avoid stale partial page sets."""
    source_dir, output_dir = source_dir.resolve(), output_dir.resolve()
    if output_dir == ROOT or source_dir == output_dir or source_dir.is_relative_to(output_dir) or output_dir.is_relative_to(source_dir):
        raise ValueError("Output must not contain or replace authored source")
    if output_dir.exists() and any(output_dir.iterdir()):
        marker = output_dir / 'build.json'
        if not marker.is_file():
            raise ValueError("Refusing to replace an output directory without a site build manifest")
        manifest = json.loads(marker.read_text(encoding='utf-8'))
        if not {'revision', 'pages', 'viewCount'} <= manifest.keys():
            raise ValueError("Output does not identify a generated site")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='site-stage-', dir=output_dir.parent) as scratch:
        staged = Path(scratch) / 'site'
        pages = _build(source_dir, staged)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        staged.rename(output_dir)
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "docs")
    parser.add_argument("--output", type=Path, default=ROOT / "build/site")
    args = parser.parse_args()
    print(f"Built {len(build(args.source, args.output))} pages in {args.output}")


if __name__ == "__main__":
    main()

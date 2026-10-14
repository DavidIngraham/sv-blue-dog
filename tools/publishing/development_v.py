"""Render the development method, without inventing evidence or gate status.

The SVG is a presentation template, not a second engineering/process model.
Native SysML views and evidence reports remain authoritative for project facts.
"""
from html import escape
from pathlib import Path
from string import Template


def render(directory: Path, *, title: str = "Blue Dog · mission-led development V") -> Path:
    """Write an accessible, standalone vector figure for Markdown publication."""
    template = Template(Path(__file__).with_suffix(".svg").read_text(encoding="utf-8-sig"))
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "development-v.svg"
    output.write_text(template.substitute(title=escape(title)), encoding="utf-8")
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="Blue Dog · mission-led development V")
    args = parser.parse_args()
    print(render(args.output, title=args.title))

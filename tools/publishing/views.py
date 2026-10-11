"""Compile explicitly scoped Markdown view blocks through OpenSysML."""
from dataclasses import dataclass
import re

from tools.boat_analysis.model.runtime import ROOT, model_files, native, validate

QUALIFIED = r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)+"


@dataclass(frozen=True)
class ViewBlock:
    target: str
    source: str
    direction: str = "BT"
    report: bool = False
    statements: bool = False

    @classmethod
    def parse(cls, info, source):
        parts = info.split()
        statements = "statements=true" in parts
        parts = [part for part in parts if part != "statements=true"]
        if len(parts) not in (2, 3) or not re.fullmatch(QUALIFIED, parts[1]):
            raise ValueError("Use: sysml-view Package::view [direction=BT|TB|LR|RL]")
        if parts[0] == "sysml-report":
            if source.strip() or len(parts) != 2:
                raise ValueError("A report fence references one native document and has no body")
            return cls(parts[1], "", report=True)
        direction = "BT" if len(parts) == 2 else parts[2].removeprefix("direction=")
        if direction not in {"BT", "TB", "LR", "RL"}:
            raise ValueError("Invalid view direction")
        # This is an authoring restriction, not a SysML parser. The native parser
        # resolves the model and checks actual syntax/semantics below.
        code = re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"', '', source, flags=re.S)
        if re.search(r'\b(requirement|part|calc|analysis|verification|action|connection|dependency|constraint|port)\s+(def\s+)?\w', code):
            raise ValueError("Inline blocks may scope views, not define engineering elements")
        return cls(parts[1], source, direction, statements=statements)

    def document(self, index):
        """Wrap native views in a native document for layout and statement queries."""
        names = re.findall(r'\bexpose\s+(' + QUALIFIED + r')\s*;', self.source)
        statements = ""
        if names and self.statements:
            quoted = ', '.join('"' + name + '"' for name in names)
            statements = f'''
    calc def Statements :> Query {{
        Project(source = RelatedElements(source = Named(qualifiedName = ({quoted})),
            relationshipKind = "typing", direction = "outgoing", maxDepth = 1),
            properties = ("documentation"), columns = (Column(name = "Label", cell = {{
                in row : KerML::Root::Element; row.declaredShortName + " " + row.declaredName }})))
    }}
'''
        details = '''part statements : Definitions {
            attribute redefines term = "Label";
            attribute redefines description = "documentation";
            calc rows : Statements;
        }''' if statements else ""
        return self.source + f'''
package PageBuild{index} {{
    private import DocumentQueries::*;
    {statements}
    part def Content :> Document {{
        attribute redefines title = "";
        part diagram : Diagram {{
            attribute redefines direction = "{self.direction}";
            ref redefines source = {self.target};
        }}
        {details}
    }}
}}
'''


def render_blocks(blocks, directory):
    if not blocks:
        return []
    paths = []
    for index, block in enumerate(blocks):
        if block.report:
            continue
        path = directory / f"view-{index}.sysml"
        path.write_text(block.document(index), encoding="utf-8")
        paths.append(path)
    models = (*model_files(), ROOT / "tools/publishing/reference.sysml", *paths)
    validate(models)
    output = directory / "rendered"
    native("-render-documents", output, "-diagram-form", "mermaid", models=models)
    return [(output / ((block.target.replace('::', '-') if block.report else f"PageBuild{i}-Content") + ".md")).read_text(encoding="utf-8")
            for i, block in enumerate(blocks)]

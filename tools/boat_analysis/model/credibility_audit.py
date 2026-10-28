"""Native analysis intended-use and limitation inventory, without acceptance claims."""
from collections import Counter
from dataclasses import asdict
import hashlib,json
from pathlib import Path
from .runtime import ROOT,connection,model_files
from .install import REVISION


def native_credibility_audit(sources=None):
    sources=tuple(sources) if sources is not None else tuple((str(p),p.read_text()) for p in model_files())
    q=ROOT/'tools/publishing/reference.sysml'
    m=connection().parse_sources((*sources,(str(q),q.read_text())),strict=True)
    roots=sorted({c.id for r in m.roots for c in r.children()})
    inventory=m.query(scope=roots,select=['@type','owner','type'],where={
        '@type':'PrimitiveConstraint','property':'@type','operator':'=','value':['AnalysisCaseDefinition','AnalysisCaseUsage']})
    table=m.run_document_query('BlueDogAnalysisDocuments::Uses')
    rows={r.element.id:r for r in table}
    errors=[]
    for case in inventory:
        row=rows.get(case.id)
        if row is None:errors.append('A03 Analysis absent from use register: '+case.id)
        elif any(len(c)!=1 or not isinstance(c[0],str) or not c[0].strip() for c in row.cells):
            errors.append('A05 Missing/ambiguous use or limitation: '+case.id)
    if set(rows)-{c.id for c in inventory}:errors.append('A03 Register contains non-analysis rows')
    return dict(runtimeRevision=REVISION,modelHash=m.hash,
        sourceHashes={str(Path(p).relative_to(ROOT)):hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in (q,Path(__file__))},
        diagnostics=[str(d) for d in m.diagnostics],errors=errors,
        summary=dict(analysisCases=len(inventory),registeredCases=len(rows),
            nativeTypes=dict(Counter(c.get('@type') for c in inventory)),
            useCategories=dict(Counter(r.cells[1][0] for r in table if r.cells[1]))),
        table=asdict(table),
        interpretation='Use/limitation coverage only. Category annotations neither execute analyses nor demonstrate validation, credibility ratings or acceptance.')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args()
    r=native_credibility_audit()
    if a.output:a.output.write_text(json.dumps(r,default=str,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('summary','errors','diagnostics')},indent=2))
    raise SystemExit(bool(r['errors'] or r['diagnostics']))


if __name__=='__main__':main()

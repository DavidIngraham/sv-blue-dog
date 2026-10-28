"""Native hazard/control/disposition audit; no risk acceptance or probability inference."""
from dataclasses import asdict
import hashlib,json
from pathlib import Path
from .runtime import ROOT,connection,model_files
from .install import REVISION


def native_safety_audit(sources=None):
    sources=tuple(sources) if sources is not None else tuple((str(p),p.read_text()) for p in model_files())
    q=ROOT/'tools/publishing/reference.sysml'
    m=connection().parse_sources((*sources,(str(q),q.read_text())),strict=True)
    tables={n:m.run_document_query('BlueDogSafetyDocuments::'+n) for n in ('Hazards','Basis','Dispositions','FailureModes')}
    hazards={r.element.id:r for r in tables['Hazards']}
    modes={r.element.id:r for r in tables['FailureModes']}
    support={h:dict(contributors=[],controls=[],verificationPlans=[]) for h in hazards}
    errors=[]
    for row in hazards.values():
        if any(not c or c==('',) for c in (*row.cells[:5],row.cells[6])):
            errors.append('S01 Incomplete hazard context: '+row.element.id)
        if [x.id for x in row.cells[5]]!=['BlueDogIC01::design']:
            errors.append('S01 Wrong hazard configuration: '+row.element.id)
    for row in tables['Basis']:
        for client in row.cells[1]:
            if client.id not in support:continue
            for supplier in row.cells[2]:
                category=('contributors' if supplier.id in modes else 'controls' if supplier.type=='RequirementUsage'
                    else 'verificationPlans' if supplier.type=='VerificationCaseDefinition' else None)
                if category:support[client.id][category].append(supplier.id)
    for h,links in support.items():
        for category,values in links.items():
            if not values:errors.append('S02 Missing '+category+': '+h)
    mapped={x for links in support.values() for x in links['contributors']}
    for name,row in modes.items():
        if row.cells[1]==(True,) and name not in mapped:errors.append('S02 Unmapped critical failure: '+name)
    open_records=[dict(hazard=r.element.id,missing=[name for name,cell in zip(tables['Dispositions'].columns[5:8],r.cells[5:8]) if not cell],
        closed=r.cells[8][0]) for r in tables['Dispositions']]
    safety=m.run_analysis('BlueDogSafety::SafetyReview',subject='BlueDogSafety::gorge').outputs
    fmea=m.run_analysis('FailureAnalysis::DesignFailureReview',subject='BlueDogDFMEA::starter').outputs
    return dict(runtimeRevision=REVISION,modelHash=m.hash,
        sourceHashes={str(Path(p).relative_to(ROOT)):hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in (q,Path(__file__))},
        diagnostics=[str(d) for d in m.diagnostics],errors=errors,safetyReview=safety,fmeaReview=fmea,
        support=support,openRecords=open_records,tables={n:asdict(t) for n,t in tables.items()},
        interpretation='Initial current-Gorge argument only. Native review readiness is a supplied-evidence precondition, '
        'not accepted physical effectiveness, completeness, quantified risk or actual risk acceptance.')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);args=p.parse_args()
    r=native_safety_audit()
    if args.output:args.output.write_text(json.dumps(r,default=str,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('errors','diagnostics','safetyReview','fmeaReview','openRecords')},indent=2))
    raise SystemExit(bool(r['errors'] or r['diagnostics']))


if __name__=='__main__':main()

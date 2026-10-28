"""Audit V&V plans using native methods, objectives and configuration facts.

This inventory executes no verification and makes no acceptance decision.
"""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from .runtime import ROOT,connection,model_files
from .install import REVISION


def native_verification_audit(sources=None):
    sources=tuple(sources) if sources is not None else tuple((str(p),p.read_text()) for p in model_files())
    query_file=ROOT/'tools/publishing/reference.sysml'
    m=connection().parse_sources((*sources,(str(query_file),query_file.read_text())),strict=True)
    roots=sorted({child.id for root in m.roots for child in root.children()})
    definitions={r.id for r in m.query(scope=roots,select=[],where={'@type':'PrimitiveConstraint',
        'property':'@type','operator':'=','value':['VerificationCaseDefinition']})}
    tables=dict(Plans=m.run_document_query('BlueDogVerificationDocuments::Plans',{'roots':roots}),
        PlannedVerdicts=m.run_document_query('BlueDogVerificationDocuments::PlannedVerdicts'),
        IntegrationConfigurations=m.run_document_query('BlueDogVerificationDocuments::IntegrationConfigurations'))
    errors=[]
    expected_methods={'VerificationCases::VerificationMethodKind::'+kind for kind in ('inspect','analyze','demo','test')}
    planned={row.element.id for row in tables['Plans']}
    for name in sorted(definitions-planned):errors.append('V01 Unlisted verification definition: '+name)
    for row in tables['Plans']:
        methods=row.cells[1]
        if not methods:errors.append('V04 Missing planned method: '+row.element.id)
        if any(method.id not in expected_methods for method in methods):
            errors.append('V04 Unsupported planned method: '+row.element.id)
        if not row.cells[2]:errors.append('V01 Missing verification objective: '+row.element.id)
    open_evidence=[]
    for row in tables['IntegrationConfigurations']:
        if [r.id for r in row.cells[1]]!=['BlueDog::Configurations::IC01::design']:
            errors.append('V02 Wrong planned design: '+row.element.id)
        if [r.id for r in row.cells[2]]!=['BlueDog::Architecture::Physical::ic01']:
            errors.append('V02 Wrong planned assembly: '+row.element.id)
        open_evidence.append(dict(plan=row.element.id,missing=[name for name,cell in
            zip(tables['IntegrationConfigurations'].columns[4:],row.cells[4:]) if not cell]))
    return dict(runtimeRevision=REVISION,modelHash=m.hash,
        sourceHashes={str(Path(p).relative_to(ROOT)):hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest()
            for p in (query_file,Path(__file__))},diagnostics=[str(d) for d in m.diagnostics],errors=errors,
        summary=dict(verificationDefinitions=len(definitions),withPlannedMethods=sum(bool(r.cells[1]) for r in tables['Plans']),
            declaredPlanResults=len(tables['PlannedVerdicts'].rows),integrationPlans=len(open_evidence)),
        openEvidence=open_evidence,tables={name:asdict(table) for name,table in tables.items()},
        executedByAudit=False,evidenceAcceptanceAssessed=False,
        interpretation='Native plan inventory only. Method tags are plans; declared plan results are not executions. '
        'Numerical verification definitions require bound subjects. Empty article/procedure/instrument fields remain '
        'evidence gaps. Eligibility calculations do not decide acceptance; historical artifacts keep their subjects.')


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=native_verification_audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,default=str,indent=2)+'\n')
    print(json.dumps(dict(summary=report['summary'],diagnostics=report['diagnostics'],errors=report['errors'],
        openEvidence=report['openEvidence']),indent=2))
    raise SystemExit(bool(report['errors'] or report['diagnostics']))


if __name__=='__main__':main()

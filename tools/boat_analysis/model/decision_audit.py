"""Native decision context, criterion applicability and current disposition audit."""
from dataclasses import asdict
from collections import Counter
import hashlib,json
from pathlib import Path
from .runtime import ROOT,connection,model_files
from .install import REVISION


def native_decision_audit(sources=None):
    sources=tuple(sources) if sources is not None else tuple((str(p),p.read_text()) for p in model_files())
    q=ROOT/'tools/publishing/reference.sysml'
    m=connection().parse_sources((*sources,(str(q),q.read_text())),strict=True)
    tables={n:m.run_document_query('BlueDogDecisionDocuments::'+n) for n in
        ('WorkingRecords','OpenRecords','BasisRecords','RecordStates','Criteria','Basis','DesignBasis')}
    tables['AllocationReviews']=m.run_document_query('BlueDogRequirementBasisDocuments::AllocationClosureRows')
    errors=[];missing_actual=[]
    required=('Record','Kind','Question','Scope','Responsible role','Mandatory basis','Comparison basis','Reopening trigger','Needed evidence')
    actual=('Actual disposition record','Actual authority','Actual decision date','Implementation evidence')
    for name in ('WorkingRecords','OpenRecords'):
        table=tables[name]
        for row in table:
            values=dict(zip(table.columns,row.cells))
            for field in required:
                if len(values[field])!=1 or not str(values[field][0]).strip():errors.append('D01 Missing decision context '+field+': '+row.element.id)
            if name=='WorkingRecords' and not values['Recorded disposition']:errors.append('D18 Missing working disposition: '+row.element.id)
            missing = [f for f in actual if len(values[f])!=1 or not str(values[f][0]).strip()]
            missing_actual.append(dict(decision=row.element.id,missing=missing))
            if name=='OpenRecords' and values['Open-question acceptance']==(True,) and any(f in missing for f in actual[:3]):
                errors.append('D19 Accepted question lacks actual disposition/authority/date identities: '+row.element.id)
    inventory=m.query(select=['type'],where={
        '@type':'PrimitiveConstraint','property':'type','operator':'=',
        'value':['EngineeringDecisions::DecisionRecord']})
    represented={r.element.id for n in ('WorkingRecords','OpenRecords','BasisRecords') for r in tables[n]}
    if represented!={r.id for r in inventory}:errors.append('D01 Native decision inventory differs from register')
    if any(r.type!='ItemUsage' for r in inventory):errors.append('D01 Decision records must be information items')
    for row in tables['BasisRecords']:
        if any(len(cell)!=1 or not str(cell[0]).strip() for cell in row.cells):
            errors.append('D18 Incomplete retained design basis: '+row.element.id)
    states=tables['RecordStates']
    if {r.element.id for r in states}!=represented:errors.append('D01 Record-state inventory differs from register')
    open_ids={r.element.id for r in tables['OpenRecords']}
    for row in states:
        values=dict(zip(states.columns,row.cells))
        expected='openQuestion' if row.element.id in open_ids else 'workingDisposition'
        if len(values['Record state'])!=1 or values['Record state'][0].id!='EngineeringDecisions::RecordState::'+expected:
            errors.append('D18 Record state disagrees with retained content: '+row.element.id)
        needed='Question' if expected=='openQuestion' else 'Recorded disposition'
        if not values[needed] or not values['Needed evidence']:
            errors.append('D18 Record lacks question/disposition or evidence needs: '+row.element.id)
    review_types=m.query(where={'@type':'PrimitiveConstraint','property':'general','operator':'=',
        'value':['EngineeringDecisions::AllocationReview']})
    if not any(r.id=='BlueDogRequirementBasis::AllocationDecision' for r in review_types):
        errors.append('D01 Allocation metadata lacks the shared review schema')
    annotations=m.query(where={'@type':'PrimitiveConstraint','property':'type','operator':'=',
        'value':['EngineeringDecisions::AllocationReview',*(r.id for r in review_types)]})
    if any(r.type!='MetadataUsage' for r in annotations):errors.append('D01 Allocation reviews must annotate their subjects')
    if {r.id for r in annotations}!={r.element.id for r in tables['AllocationReviews']}:
        errors.append('D01 Allocation-review inventory differs from register')
    criteria=tables['Criteria'];positions=[r.cells[0][0] for r in criteria if r.cells[0]]
    if sorted(positions)!=list(range(1,8)):errors.append('D07 Criterion positions must identify each of the seven evidence entries')
    basis={}
    for r in tables['Basis']:
        for client in r.cells[0]:basis.setdefault(client.id,set()).update(x.id for x in r.cells[1])
    for row in criteria:
        if any(not c for c in row.cells):errors.append('D07 Incomplete criterion: '+row.element.id);continue
        position=row.cells[0][0];kind=row.cells[2][0].id
        expected='comparativeStudy' if position==7 else 'mandatory'
        if kind!='BlueDogTradeCriteria::Kind::'+expected:errors.append('D08 Wrong mandatory/study classification: '+row.element.id)
        if not basis.get(row.element.id):errors.append('D07 Criterion lacks native requirement basis: '+row.element.id)
    expected_basis={'BlueDogTradeCriteria::progress':{'BlueDogRequirements::passageDuration','BlueDogRequirements::cruiseEvidence'},
        'BlueDogTradeCriteria::reliabilityStudy':{'BlueDogRequirements::missionSuccessProbability','BlueDogRequirements::reliabilityEvidence','BlueDogRequirements::missionReliability'}}
    for criterion,required_basis in expected_basis.items():
        if not required_basis<=basis.get(criterion,set()):errors.append('D07 Missing current criterion basis: '+criterion)
    design_basis={(a.id,b.id) for row in tables['DesignBasis'] for a in row.cells[0] for b in row.cells[1]}
    for req in ('launchEnergyAdmission','recoveryEnergy'):
        if ('BlueDogDesignDecisions::holdingDrive','BlueDogRequirements::'+req) not in design_basis:
            errors.append('D02 Holding-drive finite mission basis missing: '+req)
    assessments={name:m.run_analysis('BlueDogSailTrade::'+name).outputs for name in ('tailAssessment','camberAssessment','softAssessment')}
    return dict(runtimeRevision=REVISION,modelHash=m.hash,
        sourceHashes={str(Path(p).relative_to(ROOT)):hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in (q,Path(__file__))},
        diagnostics=[str(d) for d in m.diagnostics],errors=errors,
        summary=dict(workingDecisions=len(tables['WorkingRecords'].rows),openQuestions=len(tables['OpenRecords'].rows),
            designBasisRecords=len(tables['BasisRecords'].rows),totalDecisionRecords=len(inventory),
            allocationReviews=len(annotations),
            declaredCriteria=len(criteria.rows),criterionClasses=dict(Counter(r.cells[2][0].id.rsplit('::',1)[-1] for r in criteria if r.cells[2]))),
        missingActualRecords=missing_actual,assessments=assessments,
        tables={n:asdict(t) for n,t in tables.items()},
        interpretation='Native record/criterion and supplied-evidence assessment only. Missing actual identities remain open; six declared gate groups are not exhaustive system acceptance. No hardware ranking, selection or approval inferred.')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();r=native_decision_audit()
    if a.output:a.output.write_text(json.dumps(r,default=str,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('summary','errors','diagnostics','assessments')},indent=2))
    raise SystemExit(bool(r['errors'] or r['diagnostics']))


if __name__=='__main__':main()

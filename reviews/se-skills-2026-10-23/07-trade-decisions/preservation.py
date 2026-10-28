"""Compare native original dispositions/questions and actual rig development standing."""
import json
from tools.boat_analysis.model.runtime import ROOT,connection,model_files
stage=ROOT/'reviews/se-skills-2026-10-23/07-trade-decisions';q=ROOT/'tools/publishing/reference.sysml'
current=tuple((str(p),p.read_text()) for p in (*model_files(),q))
overrides={str(ROOT/p):(stage/n).read_text() for p,n in (
    ('models/vehicle/decisions.sysml','before-design-decisions.sysml'),
    ('models/vehicle/requirement-decisions.sysml','before-requirement-decisions.sysml'),
    ('models/analyses/sail-trade.sysml','before-sail-trade.sysml'))}
before=connection().parse_sources(tuple((p,overrides.get(p,t)) for p,t in current),strict=True)
after=connection().parse_sources(current,strict=True)
proof={}
for name,fields in [('WorkingRecords',('Recorded disposition','Needed evidence')),
                    ('OpenRecords',('Question','Responsible role','Needed evidence','Open-question acceptance'))]:
    def values(m):
        table=m.run_document_query('BlueDogDecisionDocuments::'+name)
        return {r.element.id:{f:r.cells[table.columns.index(f)] for f in fields} for r in table}
    original,actual=values(before),values(after)
    assert original==actual,name
    proof[name]=dict(preservedRecords=len(actual),fields=fields)
for case in ('tailAssessment','camberAssessment','softAssessment'):
    original=before.run_analysis('BlueDogSailTrade::'+case).outputs
    actual=after.run_analysis('BlueDogSailTrade::'+case).outputs
    fields=('candidateName','gateCount','knownFailure','evidenceComplete','qualified','developmentDecision')
    assert {f:original[f] for f in fields}=={f:actual[f] for f in fields},case
proof['actualCandidateDevelopmentStanding']='All3preserved; unknown evidence, equal contenders, no selection'
(stage/'preservation.json').write_text(json.dumps(proof,indent=2)+'\n')
print(proof)

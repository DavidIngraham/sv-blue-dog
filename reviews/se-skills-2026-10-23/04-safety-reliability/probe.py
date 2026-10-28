from tools.boat_analysis.model.runtime import ROOT,connection,model_files
p=ROOT/'reviews/se-skills-2026-10-23/04-safety-reliability/queries.sysml'
m=connection().parse_sources((*tuple((str(p),p.read_text()) for p in model_files()),(str(p),p.read_text())),strict=True)
for name in ('Hazards','Basis','Dispositions','FailureModes'):
    table=m.run_document_query('BlueDogSafetyDocuments::'+name)
    print(name,len(table.rows),table.columns)
    for row in list(table)[:1]:print(row.element.id,row.cells)


from tools.boat_analysis.model.runtime import ROOT,connection,model_files
p=ROOT/'reviews/se-skills-2026-10-23/03-verification-evidence/queries.sysml'
sources=tuple((str(p),p.read_text()) for p in model_files())
m=connection().parse_sources((*sources,(str(p),p.read_text())),strict=True)
for name in ('Plans','IntegrationConfigurations'):
    rows=m.run_document_query('BlueDogVerificationDocuments::'+name)
    print(name,len(rows.rows),rows.columns)
    for row in list(rows)[:3]:print(row.element.id,row.cells)

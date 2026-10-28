from tools.boat_analysis.model.runtime import ROOT,model_files,connection
stage=ROOT/'reviews/se-skills-2026-10-23/05-configuration-budgets'
p=ROOT/'tools/publishing/reference.sysml'
t=p.read_text()+'\n'+(stage/'queries.sysml').read_text()
assert 'package BlueDogConfigurationDocuments' not in p.read_text()
m=connection().parse_sources((*tuple((str(f),f.read_text()) for f in model_files()),(str(p),t)),strict=True)
for name in ('Contexts','Installation','Scopes','Allocations'):
    table=m.run_document_query('BlueDogConfigurationDocuments::'+name)
    print(name,len(table.rows),table.rows[0].cells)
p.write_text(t.rstrip()+'\n')

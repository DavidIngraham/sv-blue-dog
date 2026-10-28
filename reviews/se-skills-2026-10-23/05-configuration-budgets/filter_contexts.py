from tools.boat_analysis.model.runtime import ROOT,model_files,connection
p=ROOT/'tools/publishing/reference.sysml'
t=p.read_text()
old='''Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogConfigurationManagement")),
            type = "BlueDogConfigurationManagement::ContextRecord"),'''
new='''Project(source = WhereType(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogConfigurationManagement")),
            type = "PartUsage"), type = "BlueDogConfigurationManagement::ContextRecord"),'''
assert t.count(old)==1
t=t.replace(old,new)
m=connection().parse_sources((*tuple((str(f),f.read_text()) for f in model_files()),(str(p),t)),strict=True)
print([(r.element.id,r.cells[:3]) for r in m.run_document_query('BlueDogConfigurationDocuments::Contexts')])
p.write_text(t)

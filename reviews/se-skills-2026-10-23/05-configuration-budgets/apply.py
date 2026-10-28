from tools.boat_analysis.model.runtime import ROOT,model_files,connection
stage=ROOT/'reviews/se-skills-2026-10-23/05-configuration-budgets'
p=ROOT/'models/configurations/management.sysml'
sources=tuple((str(f),f.read_text()) for f in model_files())
assert not p.exists()
m=connection().parse_sources((*sources,(str(p),(stage/'model.sysml').read_text())),strict=True)
print(m.diagnostics)
print(m.run_analysis('BlueDogConfigurationManagement::AccountingReview',subject='BlueDogConfigurationManagement::ic01').outputs)
p.write_text((stage/'model.sysml').read_text())

from tools.boat_analysis.model.runtime import ROOT,connection
p=ROOT/'reviews/se-skills-2026-10-23/07-trade-decisions/skill/references/native-trade-example.sysml'
t=p.read_text().replace('part b : Option { attribute :>> metric = 10; }','part b : Option;')
m=connection().parse_sources(((str(p),t),),strict=True)
try:
    r=m.run_analysis('DecisionMechanismExample::compare')
    print(repr(r));print(r.evaluations)
except Exception as e:print(type(e).__name__,str(e))

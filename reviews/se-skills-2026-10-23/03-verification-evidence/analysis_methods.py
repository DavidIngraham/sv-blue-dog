from tools.boat_analysis.model.runtime import ROOT,connection,model_files
sources={p:p.read_text() for p in model_files()}
for relative,names in [('models/analyses/energy.sysml',('SustainedEnergyVerification',)),
                       ('models/analyses/reliability.sysml',('VoyageReliabilityVerification','PassageDurationVerification'))]:
    p=ROOT/relative
    for name in names:
        old='    verification def '+name+' {\n'
        assert sources[p].count(old)==1,name
        sources[p]=sources[p].replace(old,old+'        metadata plannedAnalyze : VerificationCases::VerificationMethod { kind = VerificationCases::VerificationMethodKind::analyze; }\n',1)
m=connection().parse_sources(tuple((str(p),t) for p,t in sources.items()),strict=True)
assert not m.diagnostics
for relative in ('models/analyses/energy.sysml','models/analyses/reliability.sysml'):
    p=ROOT/relative;p.write_text(sources[p])
print('Native candidate accepted: analysis methods on three additional executable verification definitions.')

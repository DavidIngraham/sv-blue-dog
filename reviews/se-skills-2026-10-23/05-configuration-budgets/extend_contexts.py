from tools.boat_analysis.model.runtime import ROOT,model_files,connection
p=ROOT/'models/configurations/management.sysml'
t=p.read_text()
old='''attribute :>> revisionBasis = "BlueDogCurrentSizing/BlueDogSRRCurrent preserve original record identity and source revision; current reanalysis requires its own input fingerprints.";
        ref part :>> representedSubject = BlueDogCurrentSizing::candidate;'''
new='''attribute :>> revisionBasis = "BlueDogSRRCurrent preserves the 440Wh record and original source revision; current reanalysis requires its own input fingerprints.";
        ref part :>> representedSubject = BlueDogSRRCurrent::candidate;'''
assert t.count(old)==1
t=t.replace(old,new)
rows=[
('searchReference','SearchReference','Numerical starting geometry','Reference geometry for preparation/search; not a selected vessel or accepted installed article','BlueDogConfigurations::reference','Current authored configuration fingerprint; original decimal precision is not measured accuracy.'),
('lowerSearchBracket','LowerBracket','Numerical/model-domain lower bracket','Define search bounds; not a complete feasible vessel, owner requirement or manufacturing tolerance','BlueDogConfigurations::lowerBracket','Current model-domain/search input fingerprint; bracket changes need applicability and search review.'),
('upperSearchBracket','UpperBracket','Numerical/model-domain upper bracket','Define search bounds; not a selected dimension, vessel requirement or manufacturing tolerance','BlueDogConfigurations::upperBracket','Current model-domain/search input fingerprint; do not transfer bracket status to physical feasibility.'),
('parameterBasis','ParameterBasis','Provisional shared analysis assumptions','Reusable physical/component assumptions overridden by identified candidate integration inputs where declared','BlueDogConfigurations::assumptions','Current model/driver fingerprints identify assumptions; numerical allocations are not measured equipment.'),
('recordedBaseline','RecordedBaseline','Historical exploratory sizing projection','Interpret the original October10 exploration; no silent substitution for current geometry or qualification','BlueDogRecordedSizing::candidate','models/evidence/coupled-2026-10-10.sysml and evidence/runs/2026-10-10-coupled/manifest.json retain original revision.'),
('bingenProjection','BingenProjection','Historical Bingen sizing projection','Interpret the October12 Bingen candidate; distinct from the later 440Wh retained replay and IC-01','BlueDogCurrentSizing::candidate','Despite the package name CurrentSizing, evidence/runs/2026-10-12-bingen/manifest.json owns this historical projection.'),
('continuationProjection','ContinuationProjection','Historical coarse sizing continuation','Interpret the recorded continuation subject; coarse feasibility and target status do not establish refinement or physical qualification','BlueDogSizingContinuation::candidate','models/evidence/sizing-continuation.sysml preserves its recorded stage/result context; retain the archived run lineage.'),
('finitePassageProjection','FinitePassageProjection','Historical finite-passage continuation','Interpret the recorded partial/coarse progression and unreached target; no global infeasibility or current-vessel claim','BlueDogFinitePassageSizing::candidate','evidence/runs/2026-10-12-finite-passage/manifest.json and native evidenceManifest retain the original scope/status.'),
('reliabilityIllustration','ReliabilityIllustration','Synthetic exposure/rate example','Exercise voyage-duration and constant-hazard arithmetic; not surveyed course geometry or collected vessel failure evidence','BlueDogReliabilityExamples::gorgeIllustration','Current illustrative source fingerprint; profile/rates, dependence and statistical applicability remain unaccepted.'),
]
addition=''
for name,identifier,role,use,subject,revision in rows:
    addition+='    part '+name+' : ContextRecord {\n'
    for k,v in [('identifier',identifier),('role',role),('intendedUse',use),('revisionBasis',revision)]:
        addition+='        attribute :>> '+k+' = "'+v+'";\n'
    addition+='        ref part :>> representedSubject = '+subject+';\n    }\n'
t=t.replace('    part def PlannedInstallation {',addition+'    part def PlannedInstallation {')
m=connection().parse_sources(tuple((str(f),t if f==p else f.read_text()) for f in model_files()),strict=True)
print(m.diagnostics)
p.write_text(t)

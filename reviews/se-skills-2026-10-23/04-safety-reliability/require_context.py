from tools.boat_analysis.model.runtime import ROOT,connection,model_files
p=ROOT/'models/analyses/safety.sysml'
text=p.read_text()
for field in ('identifier','condition','potentialMishap','modes','ownerRole','controlIntent'):
    old=f'attribute {field} : String;'
    assert text.count(old)==1,field
    text=text.replace(old,f'attribute {field} : String [1];')
text=text.replace('ref part failureReview : FailureAnalysis::Review;','ref part failureReview : FailureAnalysis::Review [1];')
text=text.replace('ref part configuration : MarineDesign::Design =','ref part configuration : MarineDesign::Design [1] =')
old='        attribute closed : Boolean = implementationEvidenceAccepted and effectivenessEvidenceAccepted and'
assert text.count(old)==1
text=text.replace(old,'''        attribute contextIdentified : Boolean = identifier != "" and condition != "" and potentialMishap != "" and
            modes != "" and ownerRole != "" and controlIntent != "";
        attribute closed : Boolean = contextIdentified and implementationEvidenceAccepted and effectivenessEvidenceAccepted and''')
sources=tuple((str(path),text if path==p else path.read_text()) for path in model_files())
connection().parse_sources(sources,strict=True)
p.write_text(text)
print('Native candidate accepted: required hazard context and explicit completeness precondition.')

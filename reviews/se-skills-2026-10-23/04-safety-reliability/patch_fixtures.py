from tools.boat_analysis.model.runtime import ROOT,connection,model_files
p=ROOT/'models/analyses/safety.sysml'
text=p.read_text()
for old in (
    'BlueDogDFMEA::starter.controlLockup, BlueDogDFMEA::starter.trafficMiss, BlueDogDFMEA::starter.commonSensingFault',
    'BlueDogDFMEA::starter.navigationFault, BlueDogDFMEA::starter.controlLockup, BlueDogDFMEA::starter.commonSensingFault'):
    assert text.count(old)==1,old
    text=text.replace(old,old.replace('BlueDogDFMEA::starter.commonSensingFault',
        'BlueDogDFMEA::starter.commandContextFault, BlueDogDFMEA::starter.commonSensingFault'))
sources=tuple((str(path),text if path==p else path.read_text()) for path in model_files())
connection().parse_sources(sources,strict=True)
p.write_text(text)
p=ROOT/'tests/test_reliability.py'
text=p.read_text()
text=text.replace("['modeCount'] == 12","['modeCount'] == 15").replace("['unresolvedCriticalCount'] == 10","['unresolvedCriticalCount'] == 13").replace("['openActionCount'] == 12","['openActionCount'] == 15")
flags='''attribute :>> criticalFunctionPartitionAccepted = true;
              attribute :>> dependenceTreatmentAccepted = true;
              attribute :>> commonCauseCoverageAccepted = true;'''
old='''attribute :>> constantHazardAccepted = true;
              attribute :>> zeroFailureTestHours = 100;'''
assert text.count(old)==1
text=text.replace(old,'attribute :>> constantHazardAccepted = true;\n              '+flags+'\n              attribute :>> zeroFailureTestHours = 100;')
old="attribute :>> constantHazardAccepted = true;'''"
assert text.count(old)==1
text=text.replace(old,"attribute :>> constantHazardAccepted = true;\n              "+flags+"'''")
p.write_text(text)
print('Added command-context contribution to motion hazards; synthetic accepted fixtures explicitly state new rate-basis reviews.')

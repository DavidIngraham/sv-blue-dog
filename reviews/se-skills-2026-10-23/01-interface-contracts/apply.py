from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT, connection, model_files

architecture = ROOT/'models/vehicle/architecture.sysml'
method = ROOT/'models/vehicle/method.sysml'
sources = {p:p.read_text() for p in model_files()}

def add(path, typename, content):
    old = f'item def {typename} {{\n'
    assert sources[path].count(old) == 1, (path,typename)
    sources[path] = sources[path].replace(old,old+content,1)

obs='        item context : BlueDogInterfaceContracts::ObservationContext;\n'
for name in ('NavigationEstimate','SafetyObservation','ReserveAssessment','TrafficAssessment',
             'BoundaryAssessment','TrafficTrack','TrafficObservation','MissionRecord','MonitoredBankState'):
    add(architecture,name,obs)
for name in ('WindEstimate','LinkObservation'):
    add(method,name,obs)
for name in ('ReserveAssessment','BoundaryAssessment','TrafficObservation'):
    add(architecture,name,'        attribute observedAt : ISQ::TimeValue;\n')
for name in ('SafetyObservation','TrafficObservation'):
    add(architecture,name,'        attribute valid : ScalarValues::Boolean;\n')
add(method,'LinkObservation','        attribute valid : ScalarValues::Boolean;\n')
for name in ('OperationPermission','RecoveryCommand'):
    add(architecture,name,'        item context : BlueDogInterfaceContracts::CommandContext;\n')
add(method,'SailingCommand','        item context : BlueDogInterfaceContracts::CommandContext;\n'
    '        attribute headingReference : ScalarValues::String;\n'
    '        attribute sailTrimReference : ScalarValues::String;\n')
add(architecture,'NavigationEstimate','        attribute coordinateReference : String;\n'
    '        attribute headingReference : String;\n')
add(architecture,'TrafficTrack','        attribute bearingReference : String;\n'
    '        attribute rangeReference : String;\n'
    '        attribute headingReference : String;\n')
add(method,'WindEstimate','        attribute frameIdentity : ScalarValues::String;\n')
# Keep all existing payload field identities; new context is additive.
model=connection().parse_sources(tuple((str(p),t) for p,t in sources.items()),strict=True)
assert not model.diagnostics, model.diagnostics
for path in (architecture,method):
    path.write_text(sources[path])
print('Native candidate parse accepted. Added context to 14 existing payload types; original fields retained.')

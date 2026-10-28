from tools.boat_analysis.model.runtime import ROOT,connection,model_files
sources={p:p.read_text() for p in model_files()}
behavior=ROOT/'models/vehicle/behavior-contracts.sysml'
method=ROOT/'models/vehicle/method.sysml'
sources[behavior]=sources[behavior].replace(': Boolean;',': Boolean [1];').replace(': TimeValue;',': TimeValue [1];')
for old,new in (
    ('in permission : BlueDogLogicalArchitecture::OperationPermission;','in permission : BlueDogLogicalArchitecture::OperationPermission [1];'),
    ('in command : SailingCommand;','in command : SailingCommand [1];'),
    ('in command : BlueDogLogicalArchitecture::RecoveryCommand;','in command : BlueDogLogicalArchitecture::RecoveryCommand [1];'),
    ('in authorizationStored : ScalarValues::Boolean;','in authorizationStored : ScalarValues::Boolean [1];'),
    ('out authorizationStored : ScalarValues::Boolean;','out authorizationStored : ScalarValues::Boolean [1];'),
    ('in navigationUsable : ScalarValues::Boolean;','in navigationUsable : ScalarValues::Boolean [1];'),
    ('out usable : ScalarValues::Boolean;','out usable : ScalarValues::Boolean [1];')):
    assert old in sources[method],old
    sources[method]=sources[method].replace(old,new)
m=connection().parse_sources(tuple((str(p),t) for p,t in sources.items()),strict=True)
assert not m.diagnostics
for p in (behavior,method):p.write_text(sources[p])
print('Native candidate accepted: critical gate and permission parameters explicitly required.')

"""Native interface schema and applicability checks, not physical qualification."""
import pytest
from opensysml.errors import ExecutionError
from tools.boat_analysis.model.runtime import load_model, model_files, connection


@pytest.fixture(scope='module')
def model():
    return load_model()


def fields(model, name):
    return {a.name:a.type for a in model.find(name).attribute_facts()}


def test_observation_timestamps_and_validity_are_explicit(model):
    for package,names in [
        ('BlueDogLogicalArchitecture',('NavigationEstimate','SafetyObservation','ReserveAssessment',
        'TrafficAssessment','BoundaryAssessment','TrafficTrack','TrafficObservation')),
        ('BlueDogMethod',('WindEstimate','LinkObservation')),
        ('BlueDogPhysicalArchitecture',('MonitoredBankState',))]:
        for name in names:
            actual=fields(model,package+'::'+name)
            assert actual['observedAt']=='ISQBase::DurationValue'
            assert actual['valid']=='ScalarValues::Boolean'
            context=model.find(package+'::'+name+'::context')
            assert context is not None
            assert 'ObservationContext' in str(context.type_facts)


def test_command_context_does_not_supply_default_authority_or_times(model):
    actual=model.find('BlueDogInterfaceContracts::CommandContext').attribute_facts()
    assert {'authorityIdentity','configurationIdentity','clockIdentity','authorityEpoch','sequence',
            'issuedAt','validUntil'} == {a.name for a in actual}
    assert all(a.value is None for a in actual)
    for name in ('BlueDogLogicalArchitecture::OperationPermission',
                 'BlueDogLogicalArchitecture::RecoveryCommand','BlueDogMethod::SailingCommand'):
        assert 'CommandContext' in str(model.find(name+'::context').type_facts)


def quantity(model, text):
    return model.eval(text,context_symbol_id='BlueDogInterfaceContracts')


@pytest.mark.parametrize('valid,context,clock,observed,now,age,expected',[
    (True,True,True,'9 [s]','10 [s]','1 [s]',True),
    (True,True,True,'0.15 [min]','10 [s]','1 [s]',True),
    (True,True,True,'8.999 [s]','10 [s]','1 [s]',False),
    (True,True,True,'10.001 [s]','10 [s]','1 [s]',False),
    (True,True,True,'10 [s]','10 [s]','0 [s]',True),
    (True,True,True,'10 [s]','10 [s]','-1 [s]',False),
    (False,True,True,'9 [s]','10 [s]','1 [s]',False),
    (True,False,True,'9 [s]','10 [s]','1 [s]',False),
    (True,True,False,'9 [s]','10 [s]','1 [s]',False),
])
def test_native_observation_acceptance(model,valid,context,clock,observed,now,age,expected):
    # Synthetic bounds exercise the contract; they do not select a vessel limit.
    result=model.calc('BlueDogInterfaceContracts::ObservationUsable',
        [valid,context,clock]+[quantity(model,x) for x in (observed,now,age)])
    assert result.value is expected


@pytest.mark.parametrize('authority,context,clock,ordered,issued,expiry,now,expected',[
    (True,True,True,True,9,11,10,True),
    (True,True,True,True,9,10,10,True),
    (True,True,True,True,9,10,10.001,False),
    (True,True,True,True,10.001,11,10,False),
    (True,True,True,True,11,9,10,False),
    (False,True,True,True,9,11,10,False),
    (True,False,True,True,9,11,10,False),
    (True,True,False,True,9,11,10,False),
    (True,True,True,False,9,11,10,False),
])
def test_native_command_applicability(model,authority,context,clock,ordered,issued,expiry,now,expected):
    result=model.calc('BlueDogInterfaceContracts::CommandApplicable',
        [authority,context,clock,ordered]+[quantity(model,f'{x} [s]') for x in (issued,expiry,now)])
    assert result.value is expected


def test_missing_freshness_criterion_is_not_success(model):
    with pytest.raises(ExecutionError, match="calc invocation failed"):
        model.calc('BlueDogInterfaceContracts::ObservationUsable',[True,True,True,
            quantity(model,'9 [s]'),quantity(model,'10 [s]')])


def test_future_time_guard_is_observable_in_native_negative_control():
    sources=tuple((str(p),p.read_text()) for p in model_files())
    old='and maximumAge >= 0 [s] and observedAt <= now and now - observedAt <= maximumAge;'
    assert sum(t.count(old) for _,t in sources)==1
    mutant=connection().parse_sources(tuple((p,t.replace(old,
        'and maximumAge >= 0 [s] and now - observedAt <= maximumAge;')) for p,t in sources),strict=True)
    assert mutant.calc('BlueDogInterfaceContracts::ObservationUsable',[True,True,True,
        quantity(mutant,'11 [s]'),quantity(mutant,'10 [s]'),quantity(mutant,'1 [s]')]).value is True


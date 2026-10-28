"""Execute consumer barriers and qualification restoration through native policy."""
import itertools
import pytest
from opensysml.errors import ExecutionError
from tools.boat_analysis.model.runtime import load_model,connection,model_files
from tools.boat_analysis.mission.logic import MissionLogic
from tests.native_edits import replace_unique


@pytest.fixture(scope='module')
def model():
    return load_model()


SAILING=dict(commandApplicable=True,permissionApplicable=True,sailingPermitted=True,
    abortLatched=False,qualificationLost=False,capsized=False,windUsable=True,
    navigationUsable=True,requiredSafetyConfirmed=True)
RECOVERY=dict(recoveryRequested=True,commandApplicable=True,recoveryAuthorized=True,
    qualificationStateKnown=True,qualifying=False,disqualificationStored=True,
    recoveryPathAvailable=True,inhibitActive=False)


def execute(model,name,inputs):
    return dict(model.execute_action('BlueDog::Behavior::Contracts::'+name,inputs=inputs))


@pytest.mark.parametrize('field',SAILING)
def test_each_sailing_barrier_independently_prevents_actuation(model,field):
    assert execute(model,'SailingActuationGate',SAILING)['actuate'] is True
    assert execute(model,'SailingActuationGate',SAILING|{field:not SAILING[field]})['actuate'] is False


@pytest.mark.parametrize('field',RECOVERY)
def test_each_recovery_barrier_independently_inhibits_motor(model,field):
    assert execute(model,'RecoveryActuationGate',RECOVERY)['motorEnable'] is True
    assert execute(model,'RecoveryActuationGate',RECOVERY|{field:not RECOVERY[field]})['motorEnable'] is False


def test_recovery_authority_does_not_imply_motor_permission(model):
    # A primary-loss recovery authorization must still respect unknown qualification
    # and durable recording, even when the independent path is explicitly supplied.
    authority=dict(model.execute_action('BlueDog::Behavior::MissionLogic::RecoveryAuthority',inputs=dict(
        eventKind='power_loss',ordinaryPermission=False,independentPath=True)))['permitted']
    assert authority is True
    assert execute(model,'RecoveryActuationGate',RECOVERY|dict(
        recoveryAuthorized=authority,qualificationStateKnown=False))['motorEnable'] is False
    assert execute(model,'RecoveryActuationGate',RECOVERY|dict(
        recoveryAuthorized=authority,disqualificationStored=False))['motorEnable'] is False


@pytest.mark.parametrize('record_valid,persisted,current',tuple(itertools.product((False,True),repeat=3)))
def test_restart_never_recovers_qualification_without_a_consistent_record(model,record_valid,persisted,current):
    result=execute(model,'RestoreQualification',dict(recordValid=record_valid,
        persistedQualificationLost=persisted,currentQualificationLost=current))['qualificationLostNext']
    if not record_valid or current or persisted:
        assert result is True
    else:
        assert result is False


def test_restored_observations_cannot_undo_restart_fallback():
    logic=MissionLogic()
    assert logic.restore_qualification(0,record_valid=False,persisted_qualification_lost=False) is True
    result=logic.cycle(1)
    assert result['qualificationLostNext'] is True
    assert result['sailingPermitted'] is False
    assert result['gateScoringPermitted'] is False
    assert logic.restore_qualification(2,record_valid=True,persisted_qualification_lost=False) is True
    assert logic.trace[0]['action']=='BlueDog::Behavior::Contracts::RestoreQualification'


def test_valid_restart_and_new_attempt_are_distinct_operations():
    logic=MissionLogic()
    assert logic.restore_qualification(0,record_valid=True,persisted_qualification_lost=False) is False
    assert logic.cycle(1)['sailingPermitted'] is True
    logic.event('motor_use',2)
    assert logic.restore_qualification(3,record_valid=True,persisted_qualification_lost=False) is True
    assert MissionLogic().cycle(0)['sailingPermitted'] is True


def test_unknown_restoration_is_not_coerced_to_valid():
    with pytest.raises(TypeError,match='must be Boolean'):
        MissionLogic().restore_qualification(0,record_valid=None,persisted_qualification_lost=False)


@pytest.mark.parametrize('field',('commandApplicable','permissionApplicable'))
def test_native_expired_context_blocks_otherwise_nominal_sailing(model,field):
    q=lambda x:model.eval(x,context_symbol_id='BlueDog::Architecture::Interfaces')
    expired=model.calc('BlueDog::Architecture::Interfaces::CommandApplicable',
        [True,True,True,True,q('9 [s]'),q('10 [s]'),q('11 [s]')]).value
    assert expired is False
    assert execute(model,'SailingActuationGate',SAILING|{field:expired})['actuate'] is False


def test_native_observation_action_reuses_the_interface_predicate(model):
    q=lambda x:model.eval(x,context_symbol_id='BlueDog::Architecture::Interfaces')
    result=execute(model,'AssessObservationUsability',dict(producerValid=True,
        contextApplicable=True,clockEstablished=True,observedAt=q('8 [s]'),now=q('10 [s]'),maximumAge=q('1 [s]')))
    assert result['usable'] is False
    assert execute(model,'SailingActuationGate',SAILING|dict(navigationUsable=result['usable']))['actuate'] is False


def test_missing_durability_acknowledgment_cannot_enable_motor(model):
    with pytest.raises(ExecutionError):
        execute(model,'RecoveryActuationGate',{k:v for k,v in RECOVERY.items() if k!='disqualificationStored'})


def test_removing_durability_barrier_changes_the_native_outcome():
    old='and qualificationStateKnown and not qualifying and disqualificationStored'
    sources=tuple((str(p),p.read_text()) for p in model_files())
    assert sum(t.count(old) for _,t in sources)==1
    mutant=connection().parse_sources(replace_unique(sources,old,
        'and qualificationStateKnown and not qualifying'),strict=True)
    assert execute(mutant,'RecoveryActuationGate',RECOVERY|dict(disqualificationStored=False))['motorEnable'] is True


def test_native_gate_parameters_are_required(model):
    import json
    for name in ('SailingActuationGate','RecoveryActuationGate','AssessObservationUsability','RestoreQualification'):
        graph=json.loads(model.export_graphs('BlueDog::Behavior::Contracts::'+name).content)
        action=next(a for a in graph['actions'] if a['name']=='BlueDog::Behavior::Contracts::'+name)
        assert action['parameters']
        assert all(not p.get('optional',False) for p in action['parameters'])


def test_native_recovery_graph_acknowledges_storage_before_actuation(model):
    import json
    graph=json.loads(model.export_graphs('BlueDog::Method::Scenarios::AbortAndRecover').content)
    action=next(a for a in graph['actions'] if a['name']=='BlueDog::Method::Scenarios::AbortAndRecover')
    nodes={n['name']:n['id'] for n in action['nodes']}
    edges={(e['source'],e['target']) for e in action['edges']}
    assert (nodes['recover'],nodes['persist']) in edges
    assert (nodes['persist'],nodes['actuate']) in edges
    assert (nodes['actuate'],nodes['record']) in edges
    flows={(f['source'],f.get('sourcePin'),f['target'],f.get('targetPin')) for f in action['flows']}
    assert (nodes['persist'],'authorizationStored',nodes['actuate'],'authorizationStored') in flows
    assert (nodes['actuate'],'record',nodes['record'],'record') in flows
    assert (nodes['recover'],'record',nodes['record'],'record') not in flows

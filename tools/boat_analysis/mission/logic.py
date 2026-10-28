"""Execute the model-owned mission supervisor through the pinned OpenSysML API."""
from tools.boat_analysis.model.runtime import load_model


class MissionLogic:
    """One simulation's explicit latch, model snapshot and decision evidence.

    Pure action results are memoized within this run; no state or result is shared
    between missions. The surrounding execution_session guards source changes.
    """

    def __init__(self):
        self.model = load_model()
        self.abort_latched = False
        self.qualification_lost = False
        self.trace = []
        self._cache = {}
        self._last_cycle = None

    def _execute(self, action, inputs):
        key = (action, tuple(inputs.items()))
        if key not in self._cache:
            self._cache[key] = dict(self.model.execute_action(action, inputs=inputs))
        return self._cache[key].copy()

    def restore_qualification(self, seconds, *, record_valid, persisted_qualification_lost):
        """Restore qualification only; this does not implement a hardware watchdog.

        An invalid/missing durable record follows the model's nonqualifying
        fallback. Restoring an older record cannot erase a live disqualification.
        Abort and other hardware restrictions need their own persisted state.
        """
        if type(record_valid) is not bool or type(persisted_qualification_lost) is not bool:
            raise TypeError('Qualification restoration inputs must be Boolean')
        action = 'BlueDog::Behavior::Contracts::RestoreQualification'
        inputs = dict(recordValid=record_valid,
                      persistedQualificationLost=persisted_qualification_lost,
                      currentQualificationLost=self.qualification_lost)
        result = self._execute(action, inputs)
        self.qualification_lost = result['qualificationLostNext']
        self.trace.append(dict(seconds=seconds, action=action, inputs=inputs, outputs=result.copy()))
        return self.qualification_lost

    def recovery_authority(self, seconds, event_kind, ordinary, independent):
        action='BlueDog::Behavior::MissionLogic::RecoveryAuthority'
        inputs=dict(eventKind=event_kind,ordinaryPermission=bool(ordinary),independentPath=bool(independent))
        result=self._execute(action,inputs)
        self.trace.append(dict(seconds=seconds,action=action,inputs=inputs,outputs=result.copy()))
        return result['permitted']

    def fallback(self, seconds, available, permitted):
        action='BlueDog::Behavior::MissionLogic::FallbackPolicy'
        inputs=dict(recoveryAvailable=bool(available),recoveryPermitted=bool(permitted))
        result=self._execute(action,inputs)
        self.trace.append(dict(seconds=seconds,action=action,inputs=inputs,outputs=result.copy()))
        return result

    def event(self, kind, seconds):
        action = 'BlueDog::Behavior::MissionLogic::HandleEvent'
        inputs = {'eventKind': kind, 'qualificationLost': self.qualification_lost}
        result = self._execute(action, inputs)
        directive = result['directive']
        if directive == 'unsupported':
            raise ValueError('Unknown mission event: ' + kind)
        if directive not in {'disqualify', 'communications_outage', 'retain_forecast',
                             'wind_outage', 'navigation_outage', 'abort', 'stop', 'assess_capsize'}:
            raise ValueError('Unsupported model event directive: ' + str(directive))
        self.qualification_lost = result['qualificationLostNext']
        self.trace.append(dict(seconds=seconds, action=action, inputs=inputs,
                               outputs=result.copy()))
        return result

    def capsize(self, seconds, currently_capsized, upright_observed, safety_confirmed):
        action = 'BlueDog::Behavior::MissionLogic::CapsizeDisposition'
        inputs = dict(currentlyCapsized=bool(currently_capsized),
                      uprightRecoveryObserved=bool(upright_observed),
                      requiredSafetyConfirmed=bool(safety_confirmed), abortLatched=self.abort_latched,
                      qualificationLost=self.qualification_lost)
        result = self._execute(action, inputs)
        self.qualification_lost = result['qualificationLostNext']
        self.trace.append(dict(seconds=seconds, action=action, inputs=inputs, outputs=result.copy()))
        return result['directive']

    def cycle(self, seconds, *, wind_valid=True, traffic_conflict=False,
              abort_requested=False, communications_available=True, capsized=False,
              navigation_valid=True, reserve_threatened=False, safety_confirmed=None):
        # Nominal simulations assume their declared upright observation baseline.
        # Inverted/backup safety must be supplied explicitly; no dynamics or sensor
        # capability is inferred from a primary observation loss.
        if safety_confirmed is None:
            safety_confirmed = not capsized and navigation_valid
        if type(safety_confirmed) is not bool:
            raise TypeError('Required safety confirmation must be Boolean')
        action = 'BlueDog::Behavior::MissionLogic::SupervisoryCycle'
        inputs = dict(windValid=bool(wind_valid), trafficConflict=bool(traffic_conflict),
                      abortRequested=bool(abort_requested), abortLatched=self.abort_latched,
                      qualificationLost=self.qualification_lost, capsized=bool(capsized),
                      navigationValid=bool(navigation_valid),
                      reserveThreatened=bool(reserve_threatened),
                      requiredSafetyConfirmed=bool(safety_confirmed),
                      communicationsAvailable=bool(communications_available))
        result = self._execute(action, inputs)
        for name in ('abortLatchedNext', 'qualificationLostNext', 'sailingPermitted',
                     'gateScoringPermitted', 'harvestPermitted'):
            if type(result[name]) is not bool:
                raise TypeError('Model supervisor output must be Boolean: ' + name)
        if result['mode'] not in {'sailing', 'degraded_drift', 'traffic_avoidance', 'abort_recovery',
                                 'capsized_drift', 'navigation_degraded', 'disqualified'}:
            raise ValueError('Unsupported supervisor mode: ' + str(result['mode']))
        if result['alert'] not in {'none', 'attempt', 'queue'}:
            raise ValueError('Unsupported supervisor alert: ' + str(result['alert']))
        self.abort_latched = result['abortLatchedNext']
        self.qualification_lost = result['qualificationLostNext']
        signature = (tuple(inputs.items()), tuple(result.items()))
        if signature != self._last_cycle:
            self.trace.append(dict(seconds=seconds, action=action, inputs=inputs, outputs=result.copy()))
            self._last_cycle = signature
        return result

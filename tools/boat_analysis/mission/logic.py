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
        self.trace = []
        self._cache = {}
        self._last_cycle = None

    def _execute(self, action, inputs):
        key = (action, tuple(inputs.items()))
        if key not in self._cache:
            self._cache[key] = dict(self.model.execute_action(action, inputs=inputs))
        return self._cache[key].copy()

    def event(self, kind, seconds):
        action = 'BlueDogMissionLogic::HandleEvent'
        result = self._execute(action, {'eventKind': kind})
        directive = result['directive']
        if directive == 'unsupported':
            raise ValueError('Unknown mission event: ' + kind)
        if directive not in {'disqualify', 'communications_outage', 'retain_forecast',
                             'wind_outage', 'abort', 'stop'}:
            raise ValueError('Unsupported model event directive: ' + str(directive))
        self.trace.append(dict(seconds=seconds, action=action, inputs={'eventKind': kind},
                               outputs=result.copy()))
        return result

    def cycle(self, seconds, *, wind_valid=True, traffic_conflict=False,
              abort_requested=False, communications_available=True):
        action = 'BlueDogMissionLogic::SupervisoryCycle'
        inputs = dict(windValid=bool(wind_valid), trafficConflict=bool(traffic_conflict),
                      abortRequested=bool(abort_requested), abortLatched=self.abort_latched,
                      communicationsAvailable=bool(communications_available))
        result = self._execute(action, inputs)
        for name in ('abortLatchedNext', 'sailingPermitted'):
            if type(result[name]) is not bool:
                raise TypeError('Model supervisor output must be Boolean: ' + name)
        if result['mode'] not in {'sailing', 'degraded_drift', 'traffic_avoidance', 'abort_recovery'}:
            raise ValueError('Unsupported supervisor mode: ' + str(result['mode']))
        if result['alert'] not in {'none', 'attempt', 'queue'}:
            raise ValueError('Unsupported supervisor alert: ' + str(result['alert']))
        self.abort_latched = result['abortLatchedNext']
        signature = (tuple(inputs.items()), tuple(result.items()))
        if signature != self._last_cycle:
            self.trace.append(dict(seconds=seconds, action=action, inputs=inputs, outputs=result.copy()))
            self._last_cycle = signature
        return result

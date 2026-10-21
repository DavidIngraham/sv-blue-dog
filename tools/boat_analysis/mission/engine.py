"""Point-mass sailing mission execution; no implicit station keeping or motor.

The controller selects sailing headings and depowering against a chart domain.
It is a conceptual guidance policy, not ArduSail or a validated collision system.
"""
from __future__ import annotations
from sysml_python import execution_session

from dataclasses import dataclass, field, asdict
import math

import numpy as np
from shapely import covers, linestrings, prepare, contains_xy
from shapely.geometry import Point, LineString

from tools.boat_analysis.environment.course import crossing_direction
from tools.boat_analysis.environment.trajectories import WeatherHistory
from tools.boat_analysis.model.runtime import analysis_values, load_model


def mission_inputs():
    return analysis_values('BlueDogMissionSimulation::Inputs')


@dataclass(frozen=True)
class Event:
    seconds: float
    kind: str
    duration: float = 0.
    # Explicit scenario observation; never inferred from static righting moment.
    # At capsize: safety retained while inverted. At righting: upright and
    # required control/safety restored without propulsion or outside assistance.
    # At navigation loss: a separately observed backup retains required safety.
    # A positive duration bounds that outage; zero denotes persistent loss.
    required_safety_confirmed: bool = False


@dataclass
class Result:
    outcome: str
    cause: str
    elapsed_seconds: float
    crossings: list
    history: list
    events: list
    minimum_energy_wh: float
    distance_m: float
    evidence_type: str = 'virtual'
    physically_validated: bool = False
    outside_performance_coverage_seconds: float = 0.
    surface_summary: dict = field(default_factory=dict)
    recovery_summary: dict = field(default_factory=dict)
    logic_trace: list = field(default_factory=list)
    observation_summary: dict = field(default_factory=dict)
    consequence_summary: dict = field(default_factory=dict)
    timing_trace: list = field(default_factory=list)
    energy_summary: dict = field(default_factory=dict)
    navigation_summary: dict = field(default_factory=dict)
    model_scope: str = 'Conceptual polar and point-mass guidance; wave dynamics and full navigation-rule compliance not verified'


def evaluate_outcome(*facts):
    """Execute the authoritative SysML classifier on observed simulation facts."""
    if len(facts) == 7:
        facts = (*facts, False)
    if len(facts) != 8:
        raise ValueError('MissionOutcome requires eight Boolean facts (legacy calls imply no safety abort)')
    if any(not isinstance(fact, (bool, np.bool_)) for fact in facts):
        raise TypeError('MissionOutcome facts must be Boolean')
    return load_model().calc('BlueDogMissionSimulation::MissionOutcome', arguments=[bool(fact) for fact in facts]).value


def direction(route, distance):
    a = route.interpolate(max(0, distance - 5))
    b = route.interpolate(min(route.length, distance + 5))
    vector = np.array(b.coords[0]) - a.coords[0]
    return vector / np.linalg.norm(vector)


@execution_session()
def simulate(inputs, route, water, gates, weather=None, events=(), traffic=(), seed=0,
             stochastic=False, save_every=10, classify=evaluate_outcome, recovery_planner=None, observations=None, recovery_observations=None, navigation=None):
    """Execute legacy kinematics unless inputs['maneuverDynamics'] is supplied.

    The opt-in map requires initialHeadingDeg and optionally initialSpeedMps,
    coefficients, and rudderFraction. Startup has no prior commanded motion, so
    it coasts during initial command latency. Later pending commands retain the
    previous target. Achieved headings query the same candidate/wave speed
    provider as the controller; maneuver loss is applied to that speed demand.
    Heading forecasts and powered recovery remain kinematic approximations.
    """
    if navigation is not None and observations is None:
        raise ValueError("Navigation integration requires delivered observations, not truth tracks")
    from .logic import MissionLogic
    logic = MissionLogic()
    dt, hours, forecast, lookahead, maneuver_time, _ = inputs['time']
    control_period = inputs['controlPeriodSeconds']
    if not math.isfinite(control_period) or control_period <= 0:
        raise ValueError('Control period must be positive and finite')
    from .command import CommandClock
    dynamics=None
    if 'maneuverDynamics' in inputs and (navigation is not None or inputs.get('piecewiseTrafficForecast',False)):
        raise ValueError('Navigation integration currently requires the declared kinematic maneuver model')
    if 'maneuverDynamics' in inputs:
        from .maneuver import ManeuverDynamics
        allocation=inputs['maneuverDynamics']
        dynamics=ManeuverDynamics(allocation['initialHeadingDeg'],allocation.get('coefficients'),allocation.get('initialSpeedMps',0.))
        rudder_fraction=allocation.get('rudderFraction',1.)
        if not math.isfinite(rudder_fraction) or not 0<=rudder_fraction<=1:raise ValueError('Rudder fraction must lie between zero and one')
    command_clock=CommandClock(inputs.get('commandLatencySeconds',0.),maneuver_time,dynamics=dynamics)
    continue_after_abort=inputs.get('continueAfterAbort',True)
    capacity, stored, reserve, load, maneuver_wh, solar, charging, discharge = inputs['energy']
    recovery_bank=inputs.get('recoveryBatteryWh')
    bank_standby=inputs.get('recoveryStandbyW',0.)
    if recovery_bank is not None and (not math.isfinite(recovery_bank) or recovery_bank<0 or not math.isfinite(bank_standby) or bank_standby<0):
        raise ValueError('Invalid independent recovery energy allocation')
    from .candidate import Performance
    performance = Performance(inputs['performance']) if 'performance' in inputs else None
    wave_performance=None
    if 'wavePerformance' in inputs:
        from .wave_performance import WavePerformance
        wave_performance=WavePerformance(inputs['wavePerformance']);performance=wave_performance
    outside_coverage = 0.
    wave_effects = None
    wave_summary = dict(maximumSignificantHeightM=0., maximumAddedResistanceN=0., minimumSpeedRetention=1., contactScreenSeconds=0., outsideWaveCoverageSeconds=0., outsideMotionCoverageSeconds=0., wakeEncounters=0, samples=[])
    def sailing_speeds(wind, angles):
        speeds = performance.speeds(wind,angles) if performance else np.minimum(inputs['dimensions'][2],wind*np.interp(np.abs(angles),inputs['angles'],inputs['speedRatios']))
        if wave_effects is not None and wave_performance is None:
            speeds=wave_effects.evaluate(wind,90-state.wind_from_deg+np.asarray(angles),speeds)
        return speeds
    if dt <= 0 or hours <= 0 or not 0 < stored <= capacity or (recovery_planner is None and not 0 < reserve < stored) or not 0 < discharge <= 1:
        raise ValueError('Invalid mission time or energy inputs')
    if not water.covers(route):
        raise ValueError('Reference route lies outside permitted analysis domain')
    weather = weather or WeatherHistory(inputs['weather'], hours, seed, stochastic)
    if 'surfaceEnvironment' in inputs:
        from tools.boat_analysis.environment.surface import WaveEffects
        wave_effects=WaveEffects(inputs,weather,traffic)
    first, last = direction(route,0), direction(route,route.length)
    approach = inputs['gateApproachM']
    start = np.array(route.coords[0]) - first * approach
    turnaround = np.array(route.coords[-1]) + last * approach
    if not water.covers(Point(start)) or not water.covers(Point(turnaround)):
        raise ValueError('Gate approach/turnaround extension outside chart domain')
    downstream = LineString([start, *route.coords, turnaround])
    upstream = LineString(list(downstream.coords)[::-1])
    legs = None
    if 'turnGate' in gates:
        from tools.boat_analysis.environment.routing import rounding_paths
        paths = rounding_paths(water,gates,route)
        # Extend each target beyond its checkpoint to establish a crossing.
        # Retain the real arc/return geometry for the following phase.
        legs = []
        for path in paths:
            end = np.array(path.coords[-1])+direction(path,path.length)*approach
            extended = LineString([*path.coords,end])
            if not water.covers(extended):
                raise ValueError('Rounding checkpoint extension outside chart domain')
            legs.append(extended)
        downstream = LineString([start,*legs[0].coords])
        legs[0] = downstream
    leg, position, heading = downstream, start, None
    phase, seconds, distance, minimum = 0, 0., 0., stored
    crossing_log, history, event_log = [], [], []
    recovery_summary = {'outcome':'not_exercised', 'modelAvailable':recovery_planner is not None}
    consequence_summary = {}
    truth_clearance_violation = False
    safety_abort = False
    awaiting_righting = False
    capsize_safety_confirmed = False
    navigation_safety_confirmed = False
    conflict = False
    reserve_protected = True
    traffic_seen = set()
    event_list = sorted(events, key=lambda e:e.seconds)
    event_index, comms_until, sensor_until = 0, -1., -1.
    navigation_until = -1.
    last_off_line = [position.copy() for _ in range(len(inputs['gateNames']))]
    sequence = list(zip(inputs['gateNames'],inputs['gateDirections']))
    prepare(water)
    def result(outcome, cause):
        kinds = {event['kind'] for event in event_log}
        facts = (phase == len(sequence), bool(kinds & {'operator_intervention', 'manual_weather_update'}),
                 'motor_use' in kinds, outcome == 'safety_violation' or truth_clearance_violation,
                 outcome == 'incomplete', reserve_protected, outcome == 'censored')
        verdict = classify(*facts, True) if safety_abort else classify(*facts)
        terminal = [seconds,*position,stored,cause,bool(seconds>=comms_until)]
        if history and history[-1][0] == seconds:
            history[-1] = terminal
        else:
            history.append(terminal)
        observed=Result(verdict,cause,seconds,crossing_log,history,event_log,minimum,distance)
        observed.recovery_summary = recovery_summary
        observed.logic_trace = list(logic.trace)
        observed.consequence_summary = consequence_summary.copy()
        observed.consequence_summary['truthClearanceViolated'] = truth_clearance_violation
        observed.timing_trace = list(command_clock.trace)
        if dynamics is not None:
            observed.timing_trace.append(dict(maneuverModel='bounded-rate-hypothesis',coefficients=dynamics.coefficients,
                                             physicalValidation=False,steps=dynamics.trace))
        if navigation is not None:observed.navigation_summary=navigation.summary()
        observed.energy_summary=dict(mainStoredWh=stored,recoveryStoredWh=recovery_bank,recoveryInitialWh=inputs.get('recoveryBatteryWh'),recoveryStandbyW=bank_standby)
        if recovery_observations is not None:observed.recovery_summary['observations']=recovery_observations.summary()
        observed.observation_summary = observations.summary() if observations is not None else {"mode":"perfect_truth_baseline"}
        observed.outside_performance_coverage_seconds=outside_coverage
        if performance:observed.model_scope=inputs['performance']['scope']
        if wave_effects is not None:
            wave_summary['wakeEncounters']=len(wave_effects.seen)
            observed.surface_summary=wave_summary
            observed.model_scope += ('; cached cycle-averaged sailing balance with linear wave response' if wave_performance is not None else '; directional wave resistance sensitivity and geometric contact screens')
        if dynamics is not None:observed.model_scope += '; unvalidated bounded-rate sailing maneuvers; kinematic heading forecast and point-mass recovery unchanged'
        return observed
    def current_at(point, time):
        return direction(route, route.project(Point(point)))*weather.at(time).current_mps

    def supervise(**overrides):
        observations = dict(wind_valid=seconds >= sensor_until,
                            navigation_valid=seconds >= navigation_until,
                            capsized=awaiting_righting, traffic_conflict=conflict,
                            communications_available=seconds >= comms_until,
                            safety_confirmed=(not awaiting_righting or capsize_safety_confirmed)
                            and (seconds >= navigation_until or navigation_safety_confirmed))
        observations.update(overrides)
        return logic.cycle(seconds, **observations)

    def abort(cause, capsized=None, recover=True, decision=None, reserve_threatened=False):
        nonlocal safety_abort, recovery_summary, consequence_summary, seconds, stored, position, minimum, distance, recovery_bank
        if capsized is None:
            capsized = awaiting_righting
        from .recovery import execute_recovery
        if decision is None:
            decision = supervise(abort_requested=not reserve_threatened,
                                 reserve_threatened=reserve_threatened)
        safety_abort = decision['abortLatchedNext']
        event_log.append({'seconds':seconds, 'kind':'safety_abort', 'cause':cause})
        if decision['alert'] != 'none':
            event_log.append({'seconds':seconds, 'kind':'abort_alert_attempt' if decision['alert'] == 'attempt' else 'abort_alert_queued'})
        def drift_after_failure(prior_clearance=False):
            nonlocal consequence_summary,seconds,stored,position,minimum,distance,recovery_bank
            from .recovery import execute_drift
            independent_active=recovery_bank is not None and inputs.get('independentRecovery',False)
            essential=0. if cause=='power_loss' and not independent_active else (recovery_planner.capability.essential_w if recovery_planner else load/discharge)
            drift_started=seconds
            drift=execute_drift(water,position,seconds,stored,current_at,dt=dt,
                horizon_seconds=max(0.,hours*3600-seconds),essential_w=essential if recovery_bank is None else 0.,
                traffic=traffic,dimensions=inputs['dimensions'])
            old=position.copy()
            for row in drift.history:
                distance+=float(np.linalg.norm(np.asarray(row[1:3])-old));old=np.asarray(row[1:3])
                history.append([*row,bool(row[0]>=comms_until)])
            seconds,stored,position=drift.seconds,drift.energy_wh,np.asarray(drift.position)
            minimum=min(minimum,stored)
            if recovery_bank is not None:recovery_bank=max(0.,recovery_bank-(seconds-drift_started)*essential/3600)
            consequence_summary=asdict(drift)
            if recovery_bank is not None:
                consequence_summary['recoveryEnergyExhausted']=recovery_bank<=0
            consequence_summary['clearance_violated'] |= prior_clearance
            violation=drift.collision or drift.termination=='shore_contact' or consequence_summary['clearance_violated']
            return result('safety_violation' if violation else 'disqualified',cause)
        fallback=logic.fallback(seconds,recovery_planner is not None,recover)
        if not fallback['attemptRecovery'] and not fallback['continueDrift']:
            return result('disqualified',cause)
        if not fallback['attemptRecovery'] and recover and recovery_planner is not None:
            return drift_after_failure() if continue_after_abort else result('disqualified',cause)
        if not recover:
            recovery_summary = {'outcome': 'recovery_unavailable_common_cause' if cause in {'steering_loss','power_loss'} else 'awaiting_operator_retrieval_or_relocation'}
            return drift_after_failure() if continue_after_abort and fallback['continueDrift'] else result('disqualified', cause)
        if recovery_planner is None:
            recovery_summary = {'outcome':'recovery_model_unavailable'}
            return drift_after_failure() if continue_after_abort and fallback['continueDrift'] else result('disqualified', cause)
        start_position = position.copy()
        recovery = execute_recovery(recovery_planner, position, seconds, stored if recovery_bank is None else recovery_bank, current_at,
                                    capsized=capsized, dt=dt,
                                    horizon_seconds=max(dt, hours*3600-seconds),
                                    traffic=traffic, dimensions=inputs['dimensions'],observations=recovery_observations)
        recovery_summary = asdict(recovery)
        recovery_summary['energySource']='main' if recovery_bank is None else 'independent_recovery_bank'
        if recovery.history:
            event_log.append({'seconds':seconds, 'kind':'motor_use'})
        for row in recovery.history:
            distance += float(np.linalg.norm(np.asarray(row[1:3])-start_position))
            start_position = np.asarray(row[1:3])
            history.append([*row[:3],row[3] if recovery_bank is None else stored,*row[4:],bool(row[0]>=comms_until)])
        seconds,position=recovery.seconds,np.asarray(recovery.position)
        if recovery_bank is None:stored=recovery.energy_wh
        else:recovery_bank=recovery.energy_wh
        minimum = min(minimum, stored)
        if continue_after_abort and not recovery.collision and recovery.outcome!='recovery_approach_reached':
            return drift_after_failure(recovery.clearance_violated)
        consequence_summary=dict(termination=recovery.outcome,clearance_violated=recovery.clearance_violated,collision=recovery.collision)
        return result('safety_violation' if recovery.collision or recovery.clearance_violated else 'disqualified', cause)

    step, next_control = 0, 0.
    previous_velocity = None
    while seconds < hours*3600:
        while event_index < len(event_list) and event_list[event_index].seconds <= seconds:
            event = event_list[event_index]; event_index += 1
            event_log.append({'seconds':seconds,'kind':event.kind})
            if event.kind in {'capsize', 'unassisted_righting', 'navigation_loss'}:
                event_log[-1]['requiredSafetyConfirmed'] = event.required_safety_confirmed
            decision = logic.event(event.kind, seconds)
            directive = decision['directive']
            if directive == 'disqualify':
                return result('disqualified',event.kind)
            if directive == 'communications_outage':
                comms_until = max(comms_until, seconds+event.duration)
            elif directive == 'retain_forecast':
                pass
            elif directive == 'wind_outage':
                sensor_until = max(sensor_until, seconds+event.duration)
            elif directive == 'navigation_outage':
                if type(event.required_safety_confirmed) is not bool:
                    raise TypeError('Backup navigation safety observation must be Boolean')
                navigation_until = max(navigation_until, seconds+event.duration if event.duration > 0 else math.inf)
                navigation_safety_confirmed = event.required_safety_confirmed
                command_clock.cancel(seconds,event.kind)
                heading = None
                next_control = seconds
                # Process each observation before another simultaneous event can
                # replace it. Restored backup status cannot erase observed loss.
                observation_decision = supervise()
                if observation_decision['abortLatchedNext']:
                    return abort('required_safety_unconfirmed', decision=observation_decision)
            elif directive == 'assess_capsize':
                if type(event.required_safety_confirmed) is not bool:
                    raise TypeError('Capsize safety observation must be Boolean')
                disposition = logic.capsize(seconds, awaiting_righting,
                    event.kind == 'unassisted_righting', event.required_safety_confirmed)
                if disposition == 'abort':
                    return abort(event.kind, capsized=event.kind == 'capsize' or awaiting_righting)
                if disposition == 'invalid_observation':
                    raise ValueError('Unassisted righting requires a preceding capsize')
                awaiting_righting = disposition == 'await_righting'
                capsize_safety_confirmed = event.required_safety_confirmed
                # A pre-capsize command must not be applied after recovery.
                command_clock.cancel(seconds,event.kind)
                if dynamics is not None:dynamics.speed=0.
                heading = None
                next_control = seconds
                last_off_line = [position.copy() for _ in range(len(inputs['gateNames']))]
                recovery_summary = dict(outcome='awaiting_unassisted_righting' if awaiting_righting else 'unassisted_righting_observed',
                    modelAvailable=False, scope='Explicit scenario observation; current-only drift, no righting dynamics')
            elif directive == 'abort':
                cause = 'forecast_no_longer_applicable' if event.kind == 'forecast_invalidated' else event.kind
                permission=logic.recovery_authority(seconds,event.kind,decision['recoveryPermitted'],inputs.get('independentRecovery',False) and recovery_bank is not None and recovery_bank>0)
                return abort(cause, capsized=decision['capsized'] or awaiting_righting, recover=permission)
            elif directive == 'stop':
                return result('incomplete','terminal_failure')
        supervisor = supervise()
        if supervisor['abortLatchedNext']:
            return abort('required_safety_unconfirmed', decision=supervisor)
        if command_clock.advance(seconds):
            stored-=maneuver_wh;minimum=min(minimum,stored)
        heading=command_clock.heading
        contacts = observations.observe(traffic, position, seconds) if observations is not None else traffic
        state = weather.at(seconds)
        nearest = route.project(Point(position))
        current = direction(route, nearest)*state.current_mps
        if recovery_planner is not None:
            plan = recovery_planner.plan(position, lambda p: current_at(p, seconds))
            if plan is None:
                return abort('no_modeled_recovery_route')
            if recovery_bank is None:reserve = plan.reserve_wh
            elif recovery_bank <= plan.reserve_wh+bank_standby*control_period/3600:
                return abort('independent_recovery_reserve_trigger', reserve_threatened=True)
            decision_allowance = (load/discharge)*control_period/3600 + maneuver_wh
            if stored <= reserve+decision_allowance:
                reserve_protected = stored >= reserve
                return abort('course_recovery_reserve_trigger', reserve_threatened=True)
        if wave_effects is not None:wave_effects.update(seconds,position,current)
        if wave_performance is not None:
            trains=wave_effects.components if wave_effects is not None else []
            if len(trains)>1:
                wave_summary['performanceCoverageReason']='mixed wave trains not in regular-wave cache'
                return result('incomplete','wave_performance_outside_coverage')
            if trains:
                height,period,propagation=trains[0]
                radians=np.deg2rad(90-propagation);along=float(np.dot(current,[np.cos(radians),np.sin(radians)]))
                geometry=inputs['surfaceEnvironment']['geometry']
                transformed=wave_effects.kernel([height,period,along,*geometry[:2],0.,1.,0.,*geometry[2:],9.80665,1000.])
                if transformed[4]<=0 or transformed[5]<0:return result('incomplete','wave_model_outside_coverage')
                period=2*np.pi/np.sqrt(9.80665*2*np.pi/transformed[1])
                height=2*transformed[0];wave_direction=(state.wind_from_deg-propagation)%360
            else:
                height=0.;period=wave_performance.axes[2][0];wave_direction=0.
            if not wave_performance.set_condition(state.wind_mps,height,period,wave_direction):
                wave_summary['performanceCoverageReason']=wave_performance.reason
                wave_summary['requestedPerformanceCondition']=dict(wind=state.wind_mps,height=height,period=period,direction=wave_direction)
                return result('incomplete','wave_performance_outside_coverage')
            load=wave_performance.power
        # The sampled controller has a fixed update period independent of the
        # integration step. Commands and maneuver delay persist between updates.
        if supervisor['mode'] not in {'capsized_drift', 'navigation_degraded'} and seconds >= next_control and not command_clock.busy(seconds):
            progress = leg.project(Point(position))
            target = np.array(leg.interpolate(min(leg.length,progress+lookahead)).coords[0])
            desired = math.degrees(math.atan2(*(target-position)[::-1]))
            if inputs.get('captureGateCenters',False) and phase<len(sequence):
                gate=gates[sequence[phase][0]]
                if gate.distance(Point(position))<lookahead:
                    target=np.asarray(gate.interpolate(.5,normalized=True).coords[0])
                    desired=math.degrees(math.atan2(*(target-position)[::-1]))
            # Cartesian heading east=0; meteorological wind-from north=0.
            headings = np.unique(np.r_[np.arange(0,360,10), desired % 360, *([] if not inputs.get("retainCurrentHeadingCandidate",False) or heading is None else [heading])])
            radians = np.deg2rad(headings)
            wind_angle = 90-state.wind_from_deg
            relative = (headings-wind_angle+180)%360-180
            speeds = sailing_speeds(state.wind_mps,relative)
            supervisor = supervise()
            if not supervisor['sailingPermitted']:
                speeds[:] = 0
            velocities = np.column_stack((np.cos(radians),np.sin(radians)))*speeds[:,None]+current
            # Explicit depowered choice still drifts with current.
            velocities = np.vstack((velocities,current));headings=np.r_[headings,np.nan]
            turn = np.zeros(len(headings),dtype=bool) if heading is None else np.abs((headings-heading+180)%360-180)>30
            planning_interval=max(inputs.get('planningHorizonSeconds',0.),control_period,command_clock.latency+maneuver_time+control_period)
            held_velocity=current.copy()
            if heading is not None and supervisor['sailingPermitted']:
                held_relative=(heading-wind_angle+180)%360-180
                held_velocity+=float(sailing_speeds(state.wind_mps,held_relative))*np.array([math.cos(math.radians(heading)),math.sin(math.radians(heading))])
            waiting=position+held_velocity*command_clock.latency
            pivots=waiting+np.where(turn,maneuver_time,0)[:,None]*current
            endpoints=pivots+velocities*(planning_interval-command_clock.latency-np.where(turn,maneuver_time,0))[:,None]
            before=LineString([position,waiting])
            drift_segments=linestrings(np.stack((np.tile(waiting,(len(endpoints),1)),pivots),axis=1))
            after=linestrings(np.stack((pivots,endpoints),axis=1))
            permitted=covers(water,before) & covers(water,drift_segments) & covers(water,after)
            # Forecast safety can rank choices but cannot override exact step safety.
            projected = position+velocities*forecast
            preview = contains_xy(water,projected[:,0],projected[:,1])
            cost = np.linalg.norm(endpoints-target,axis=1)+turn*10+(~preview)*lookahead
            if inputs.get('progressGuidance',False):
                desired_vector=target-position
                norm=float(np.linalg.norm(desired_vector))
                unit=desired_vector/norm if norm>1e-8 else direction(leg,progress)
                delta=endpoints-position;forward=delta@unit
                cross=np.linalg.norm(delta-forward[:,None]*unit,axis=1)
                cost=inputs['crossTrackWeight']*cross-forward+turn*inputs['maneuverPenaltyM']+(~preview)*lookahead

            conflict = False
            for actor_index,actor in enumerate(contacts):
                actor_index = actor.source_id if actor.source_id is not None else actor_index
                safe, penalty = actor.assess(position,endpoints,seconds,planning_interval,forecast,inputs['dimensions'])
                if inputs.get('piecewiseTrafficForecast',False):
                    from .navigation import trajectory_clear
                    for j in np.flatnonzero(safe):
                        safe[j] &= trajectory_clear(actor,position,seconds,
                            [(command_clock.latency,held_velocity),(maneuver_time if turn[j] else 0.,current),
                             (max(forecast,planning_interval)-command_clock.latency-(maneuver_time if turn[j] else 0.),velocities[j])],inputs['dimensions'])
                conflict |= bool(not safe.all() or np.any(penalty))
                if actor_index not in traffic_seen and (not safe.all() or np.any(penalty)):
                    traffic_seen.add(actor_index)
                    event_log.append({'seconds':seconds,'kind':'traffic_conflict_predicted','actor':actor.name,'actor_index':actor_index})
                permitted &= safe;cost += penalty
            supervisor = supervise()
            if 'minimumSailingSpeedMps' in inputs:
                permitted[:-1] &= speeds>=inputs['minimumSailingSpeedMps']
                cost[-1] += inputs.get('depowerPenaltyM',0.)
            baseline_cost=cost.copy();baseline_cost[~permitted]=math.inf
            original_choice=int(np.argmin(baseline_cost))
            if navigation is not None:
                permitted=navigation.assess(position=position,contacts=contacts,seconds=seconds,
                    interval=planning_interval,forecast=forecast,dimensions=inputs['dimensions'],
                    headings=headings,endpoints=endpoints,velocities=velocities,
                    held_velocity=held_velocity,heading=heading,permitted=permitted,
                    trajectories=[[(command_clock.latency,held_velocity),(maneuver_time if turning else 0.,current),
                        (max(forecast,planning_interval)-command_clock.latency-(maneuver_time if turning else 0.),v)]
                        for turning,v in zip(turn,velocities)])
            cost[~permitted] = math.inf
            choice = int(np.argmin(cost))
            if navigation is not None:navigation.selected(original_choice,choice)
            if not math.isfinite(cost[choice]):
                if performance and not performance.covered(state.wind_mps):
                    return result('incomplete','performance_model_outside_coverage')
                cause='navigation_obligation_unresolved_or_no_supported_candidate' if navigation is not None and math.isfinite(baseline_cost[original_choice]) else 'no_safe_control_in_controller_search'
                return abort(cause) if recovery_planner is not None or continue_after_abort else result('incomplete',cause)
            proposed=None if math.isnan(headings[choice]) else headings[choice]
            kind='turn'
            if dynamics is not None:
                from .maneuver import maneuver_kind
                kind=maneuver_kind(dynamics.heading,proposed,wind_angle)
            command_clock.select(seconds,proposed,turn[choice],kind=kind)
            if command_clock.advance(seconds):
                stored-=maneuver_wh;minimum=min(minimum,stored)
            heading=command_clock.heading
        elif (navigation is not None or inputs.get('piecewiseTrafficForecast',False)) and supervisor['mode'] not in {'capsized_drift', 'navigation_degraded'} and seconds >= next_control:
            # Reassess the remaining committed trajectory, not a new turn from
            # the temporarily depowered state. New/changed duties still fail.
            pending=command_clock.pending
            target_heading=pending['heading'] if pending is not None else command_clock.target_heading
            remaining_latency=max(0.,pending['appliedSeconds']-seconds) if pending is not None else 0.
            remaining_drift=(maneuver_time if pending is not None and pending['turn'] else max(0.,command_clock.ends-seconds))
            target_velocity=current.copy()
            if target_heading is not None:
                relative=(target_heading-(90-state.wind_from_deg)+180)%360-180
                speed=float(sailing_speeds(state.wind_mps,relative))
                target_velocity+=speed*np.array([math.cos(math.radians(target_heading)),math.sin(math.radians(target_heading))])
            horizon=max(forecast,remaining_latency+remaining_drift+control_period)
            prior_velocity=current.copy()
            if heading is not None and remaining_latency>0:
                relative=(heading-(90-state.wind_from_deg)+180)%360-180
                prior_velocity+=float(sailing_speeds(state.wind_mps,relative))*np.array([math.cos(math.radians(heading)),math.sin(math.radians(heading))])
            endpoint=position+prior_velocity*remaining_latency+current*remaining_drift+target_velocity*(horizon-remaining_latency-remaining_drift)
            from .navigation import trajectory_clear
            committed_segments=[(remaining_latency,prior_velocity),(remaining_drift,current),
                                (horizon-remaining_latency-remaining_drift,target_velocity)]
            if inputs.get('piecewiseTrafficForecast',False) and any(not trajectory_clear(actor,position,seconds,committed_segments,inputs['dimensions']) for actor in contacts):
                return abort('committed_maneuver_forecast_conflict')
            permitted=np.array([True]) if navigation is None else navigation.assess(position=position,contacts=contacts,seconds=seconds,
                interval=horizon,forecast=horizon,dimensions=inputs['dimensions'],
                headings=np.array([np.nan if target_heading is None else target_heading]),
                endpoints=np.array([endpoint]),velocities=np.array([target_velocity]),
                held_velocity=target_velocity,heading=target_heading,permitted=np.array([True]),committed=True,
                trajectories=[[(remaining_latency,prior_velocity),(remaining_drift,current),
                    (horizon-remaining_latency-remaining_drift,target_velocity)]],
                reference_trajectory=[(remaining_latency,prior_velocity),(remaining_drift,current),
                    (horizon-remaining_latency-remaining_drift,target_velocity)],
                motion_velocity=prior_velocity if remaining_latency>0 else current if remaining_drift>0 else target_velocity,
                assessment_heading=heading if remaining_latency>0 else target_heading)
            if not permitted[0]:
                return abort('navigation_obligation_during_occupied_maneuver')
        if seconds>=next_control:next_control=seconds+control_period
        if stored < reserve:
            reserve_protected = False
            return abort('course_recovery_reserve_trigger', reserve_threatened=True)
        boundaries = [dt, hours*3600-seconds, next_control-seconds,
                      (math.floor(seconds/3600)+1)*3600-seconds]
        if observations is not None:
            boundaries.append(observations.next_boundary(seconds)-seconds)
        if event_index < len(event_list):
            boundaries.append(event_list[event_index].seconds-seconds)
        boundaries.append(command_clock.next_boundary(seconds)-seconds)
        for expiry in (comms_until,sensor_until,navigation_until):
            if expiry > seconds:boundaries.append(expiry-seconds)
        interval = min(boundaries)
        if interval <= 0:
            raise ValueError('Non-progressing mission clock')
        mode = 'sailing'
        velocity = current.copy()
        if supervisor['mode'] in {'capsized_drift', 'navigation_degraded'}:
            mode = supervisor['mode']
        elif dynamics is not None:
            permitted=supervisor['sailingPermitted']
            target=command_clock.target_heading
            relative=(dynamics.heading-(90-state.wind_from_deg)+180)%360-180
            demand=float(sailing_speeds(state.wind_mps,relative)) if permitted and target is not None else 0.
            maneuver=dynamics.step(target if permitted else None,demand,interval,command_clock.kind,rudder_fraction)
            velocity+=np.asarray(maneuver['velocity'])
            command_clock.heading=dynamics.heading
            heading=dynamics.heading
            mode='maneuvering_bounded' if maneuver['turning'] else ('sailing' if permitted and target is not None else 'coasting_drift')
        elif command_clock.drifting(seconds):
            mode = 'maneuvering_drift'
        elif not supervisor['sailingPermitted']:
            mode = 'degraded_drift'
        elif heading is None:
            mode = 'depowered_drift'
        else:
            relative = (heading-(90-state.wind_from_deg)+180)%360-180
            speed = float(sailing_speeds(state.wind_mps,relative))
            radians = math.radians(heading)
            velocity += speed*np.array([math.cos(radians),math.sin(radians)])
        if wave_effects is not None:
            # Diagnose the executed heading, including drift, not rejected forecasts.
            actual_heading=float(heading) if heading is not None else math.degrees(math.atan2(current[1],current[0]))
            actual_speed=float(np.linalg.norm(velocity-current))
            wave_effects.evaluate(state.wind_mps,[actual_heading],[actual_speed],motion_diagnostics=True)
            diagnostic=wave_effects.diagnostics[0]
            if wave_performance is not None:
                diagnostic['speedRetention']=1.
                diagnostic['performanceSource']='wave-aware cache; diagnostic resistance not reapplied'
            wave_summary['maximumSignificantHeightM']=max(wave_summary['maximumSignificantHeightM'],diagnostic['significantHeightM'])
            wave_summary['maximumAddedResistanceN']=max(wave_summary['maximumAddedResistanceN'],diagnostic['addedResistanceN'])
            wave_summary['minimumSpeedRetention']=min(wave_summary['minimumSpeedRetention'],diagnostic['speedRetention'])
            wave_summary['outsideMotionCoverageSeconds']+=interval*(not diagnostic.get('motionCovered',True))
            wave_summary['contactScreenSeconds']+=interval*diagnostic['contactScreen']
            wave_summary['outsideWaveCoverageSeconds']+=interval*(not diagnostic['covered'])
            if step % save_every == 0:wave_summary['samples'].append(dict(seconds=seconds,**diagnostic))
            if not diagnostic['covered']:return result('incomplete','wave_model_outside_coverage')
        if previous_velocity is None or not np.allclose(velocity,previous_velocity,rtol=0,atol=1e-10):
            if not history or history[-1][0]!=seconds:
                history.append([seconds,*position,stored,mode,bool(seconds>=comms_until)])
        previous_velocity=velocity.copy()
        previous = position.copy(); endpoint = position+velocity*interval
        if not water.covers(LineString([previous,endpoint])):
            return abort('held_command_leaves_chart_domain') if recovery_planner is not None or continue_after_abort else result('incomplete','held_command_leaves_chart_domain')
        for actor in contacts:
            safe,_ = actor.assess(previous,np.array([endpoint]),seconds,interval,interval,inputs['dimensions'])
            if not safe[0]:
                return abort('held_command_exhausts_traffic_margin') if recovery_planner is not None or continue_after_abort else result('incomplete','held_command_exhausts_traffic_margin')
        position = endpoint
        if performance and not performance.covered(state.wind_mps):outside_coverage += interval
        if 'storage' in inputs:
            bus=(solar*state.solar_fraction if supervisor['harvestPermitted'] else 0.)-load
            net=(min(bus*charging,inputs['storage']['maxChargeW']) if bus>=0 else bus/discharge)-inputs['storage']['selfDischargeW']
        else:
            net = (solar*state.solar_fraction*charging if supervisor['harvestPermitted'] else 0.)-load/discharge
        stored = min(capacity,stored+net*interval/3600)
        if recovery_bank is not None:recovery_bank=max(0.,recovery_bank-bank_standby*interval/3600)
        minimum=min(minimum,stored);seconds+=interval;distance+=float(np.linalg.norm(position-previous))
        for actor in traffic:
            if actor.collides(previous,position,seconds-interval,interval,inputs['dimensions']):
                return result('safety_violation','weed_contact' if actor.target_kind == 'weed' else 'traffic_collision')
        if observations is not None:
            for actor in traffic:
                safe, _ = actor.assess(previous,np.array([position]),seconds-interval,interval,interval,inputs['dimensions'])
                if not safe[0]:
                    truth_clearance_violation = True
                    if not continue_after_abort:
                        return result('safety_violation','traffic_clearance_violation')
        if stored < reserve:
            reserve_protected = False
            return abort('course_recovery_reserve_trigger', reserve_threatened=True)
        if not supervisor['gateScoringPermitted']:
            last_off_line = [position.copy() for _ in range(len(inputs['gateNames']))]
        if supervisor['gateScoringPermitted'] and phase < len(sequence):
            name, expected = sequence[phase]
            actual = crossing_direction(gates[name],last_off_line[phase],position)
            if actual == expected:
                crossing_log.append({'gate':name,'direction':actual,'seconds':seconds})
                phase += 1
                last_off_line = [position.copy() for _ in range(len(inputs['gateNames']))]
                if legs is not None and 2 <= phase < len(sequence):
                    leg = legs[phase-1]
                elif legs is None and phase == 2:
                    leg = upstream
                if phase == len(sequence):
                    history.append([seconds,*position,stored,'finished',bool(seconds>=comms_until)])
                    return result('qualified_completion','ordered_gates_without_intervention')
            elif gates[name].distance(Point(position)) > 1e-6:
                last_off_line[phase]=position.copy()
        if step % save_every == 0:
            history.append([seconds,*position,stored,mode,bool(seconds>=comms_until)])
        step += 1
    return result('censored','computational_horizon')

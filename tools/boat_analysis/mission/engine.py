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
             stochastic=False, save_every=10, classify=evaluate_outcome, recovery_planner=None):
    from .logic import MissionLogic
    logic = MissionLogic()
    dt, hours, forecast, lookahead, maneuver_time, _ = inputs['time']
    control_period = inputs['controlPeriodSeconds']
    if not 0 <= maneuver_time <= control_period or control_period <= 0:
        raise ValueError('Maneuver delay must fit the positive control period')
    capacity, stored, reserve, load, maneuver_wh, solar, charging, discharge = inputs['energy']
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
    safety_abort = False
    conflict = False
    reserve_protected = True
    traffic_seen = set()
    event_list = sorted(events, key=lambda e:e.seconds)
    event_index, comms_until, sensor_until = 0, -1., -1.
    last_off_line = [position.copy() for _ in range(len(inputs['gateNames']))]
    sequence = list(zip(inputs['gateNames'],inputs['gateDirections']))
    prepare(water)
    def result(outcome, cause):
        kinds = {event['kind'] for event in event_log}
        facts = (phase == len(sequence), bool(kinds & {'operator_intervention', 'manual_weather_update'}),
                 'motor_use' in kinds, outcome == 'safety_violation',
                 outcome == 'incomplete', reserve_protected, outcome == 'censored')
        verdict = classify(*facts, True) if safety_abort else classify(*facts)
        terminal = [seconds,*position,stored,cause,seconds>=comms_until]
        if history and history[-1][0] == seconds:
            history[-1] = terminal
        else:
            history.append(terminal)
        observed=Result(verdict,cause,seconds,crossing_log,history,event_log,minimum,distance)
        observed.recovery_summary = recovery_summary
        observed.logic_trace = list(logic.trace)
        observed.outside_performance_coverage_seconds=outside_coverage
        if performance:observed.model_scope=inputs['performance']['scope']
        if wave_effects is not None:
            wave_summary['wakeEncounters']=len(wave_effects.seen)
            observed.surface_summary=wave_summary
            observed.model_scope += ('; cached cycle-averaged sailing balance with linear wave response' if wave_performance is not None else '; directional wave resistance sensitivity and geometric contact screens')
        return observed
    def current_at(point, time):
        return direction(route, route.project(Point(point)))*weather.at(time).current_mps

    def abort(cause, capsized=False, recover=True):
        nonlocal safety_abort, recovery_summary, seconds, stored, position, minimum, distance
        from .recovery import execute_recovery
        decision = logic.cycle(seconds, abort_requested=True,
                               communications_available=seconds >= comms_until)
        safety_abort = decision['abortLatchedNext']
        event_log.append({'seconds':seconds, 'kind':'safety_abort', 'cause':cause})
        if decision['alert'] != 'none':
            event_log.append({'seconds':seconds, 'kind':'abort_alert_attempt' if decision['alert'] == 'attempt' else 'abort_alert_queued'})
        if not recover:
            recovery_summary = {'outcome':'awaiting_operator_retrieval_or_relocation'}
            return result('disqualified', cause)
        if recovery_planner is None:
            recovery_summary = {'outcome':'recovery_model_unavailable'}
            return result('disqualified', cause)
        start_position = position.copy()
        recovery = execute_recovery(recovery_planner, position, seconds, stored, current_at,
                                    capsized=capsized, dt=dt,
                                    horizon_seconds=max(dt, hours*3600-seconds),
                                    traffic=traffic, dimensions=inputs['dimensions'])
        recovery_summary = asdict(recovery)
        if recovery.history:
            event_log.append({'seconds':seconds, 'kind':'motor_use'})
        for row in recovery.history:
            distance += float(np.linalg.norm(np.asarray(row[1:3])-start_position))
            start_position = np.asarray(row[1:3])
            history.append([*row, row[0]>=comms_until])
        seconds, stored, position = recovery.seconds, recovery.energy_wh, np.asarray(recovery.position)
        minimum = min(minimum, stored)
        return result('safety_violation' if recovery.collision else 'disqualified', cause)

    step, next_control, turn_remaining = 0, 0., 0.
    while seconds < hours*3600:
        while event_index < len(event_list) and event_list[event_index].seconds <= seconds:
            event = event_list[event_index]; event_index += 1
            event_log.append({'seconds':seconds,'kind':event.kind})
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
            elif directive == 'abort':
                cause = 'forecast_no_longer_applicable' if event.kind == 'forecast_invalidated' else event.kind
                return abort(cause, capsized=decision['capsized'], recover=decision['recoveryPermitted'])
            elif directive == 'stop':
                return result('incomplete','terminal_failure')
        state = weather.at(seconds)
        nearest = route.project(Point(position))
        current = direction(route, nearest)*state.current_mps
        if recovery_planner is not None:
            plan = recovery_planner.plan(position, lambda p: current_at(p, seconds))
            if plan is None:
                return abort('no_modeled_recovery_route')
            reserve = plan.reserve_wh
            decision_allowance = (load/discharge)*control_period/3600 + maneuver_wh
            if stored <= reserve+decision_allowance:
                reserve_protected = stored >= reserve
                return abort('course_recovery_reserve_trigger')
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
        if seconds >= next_control:
            progress = leg.project(Point(position))
            target = np.array(leg.interpolate(min(leg.length,progress+lookahead)).coords[0])
            desired = math.degrees(math.atan2(*(target-position)[::-1]))
            # Cartesian heading east=0; meteorological wind-from north=0.
            headings = np.unique(np.r_[np.arange(0,360,10), desired % 360])
            radians = np.deg2rad(headings)
            wind_angle = 90-state.wind_from_deg
            relative = (headings-wind_angle+180)%360-180
            speeds = sailing_speeds(state.wind_mps,relative)
            supervisor = logic.cycle(seconds, wind_valid=seconds >= sensor_until,
                                     traffic_conflict=conflict,
                                     communications_available=seconds >= comms_until)
            if not supervisor['sailingPermitted']:
                speeds[:] = 0
            velocities = np.column_stack((np.cos(radians),np.sin(radians)))*speeds[:,None]+current
            # Explicit depowered choice still drifts with current.
            velocities = np.vstack((velocities,current));headings=np.r_[headings,np.nan]
            turn = np.zeros(len(headings),dtype=bool) if heading is None else np.abs((headings-heading+180)%360-180)>30
            movement = velocities*control_period
            movement[turn] = velocities[turn]*max(0,control_period-maneuver_time)+current*min(control_period,maneuver_time)
            endpoints = position+movement
            segments = linestrings(np.stack((np.tile(position,(len(endpoints),1)),endpoints),axis=1))
            permitted = covers(water,segments)
            # A maneuver is drift followed by sailing, not a straight chord.
            # Check both pieces before choosing a command.
            pivots = position+np.where(turn,maneuver_time,0)[:,None]*current
            before = linestrings(np.stack((np.tile(position,(len(endpoints),1)),pivots),axis=1))
            after = linestrings(np.stack((pivots,endpoints),axis=1))
            permitted &= covers(water,before) & covers(water,after)
            # Forecast safety can rank choices but cannot override exact step safety.
            projected = position+velocities*forecast
            preview = contains_xy(water,projected[:,0],projected[:,1])
            cost = np.linalg.norm(endpoints-target,axis=1)+turn*10+(~preview)*lookahead
            conflict = False
            for actor_index,actor in enumerate(traffic):
                safe, penalty = actor.assess(position,endpoints,seconds,control_period,forecast,inputs['dimensions'])
                conflict |= bool(not safe.all() or np.any(penalty))
                if actor_index not in traffic_seen and (not safe.all() or np.any(penalty)):
                    traffic_seen.add(actor_index)
                    event_log.append({'seconds':seconds,'kind':'traffic_conflict_predicted','actor':actor.name,'actor_index':actor_index})
                permitted &= safe;cost += penalty
            supervisor = logic.cycle(seconds, wind_valid=seconds >= sensor_until,
                                     traffic_conflict=conflict,
                                     communications_available=seconds >= comms_until)
            cost[~permitted] = math.inf
            choice = int(np.argmin(cost))
            if not math.isfinite(cost[choice]):
                if performance and not performance.covered(state.wind_mps):
                    return result('incomplete','performance_model_outside_coverage')
                return abort('no_safe_control_in_controller_search') if recovery_planner is not None else result('incomplete','no_safe_control_in_controller_search')
            heading = None if math.isnan(headings[choice]) else headings[choice]
            if turn[choice]:
                turn_remaining = maneuver_time
                stored -= maneuver_wh
                minimum = min(minimum,stored)
            next_control = seconds+control_period
        if stored < reserve:
            reserve_protected = False
            return abort('course_recovery_reserve_trigger') if recovery_planner is not None else result('incomplete','recovery_reserve_reached')
        boundaries = [dt, hours*3600-seconds, next_control-seconds,
                      (math.floor(seconds/3600)+1)*3600-seconds]
        if event_index < len(event_list):
            boundaries.append(event_list[event_index].seconds-seconds)
        if turn_remaining > 0:
            boundaries.append(turn_remaining)
        for expiry in (comms_until,sensor_until):
            if expiry > seconds:boundaries.append(expiry-seconds)
        interval = min(boundaries)
        if interval <= 0:
            raise ValueError('Non-progressing mission clock')
        mode = 'sailing'
        velocity = current.copy()
        if turn_remaining > 0:
            mode = 'maneuvering_drift'
        elif not logic.cycle(seconds, wind_valid=seconds >= sensor_until,
                             traffic_conflict=conflict,
                             communications_available=seconds >= comms_until)['sailingPermitted']:
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
        previous = position.copy(); endpoint = position+velocity*interval
        if not water.covers(LineString([previous,endpoint])):
            return abort('held_command_leaves_chart_domain') if recovery_planner is not None else result('incomplete','held_command_leaves_chart_domain')
        for actor in traffic:
            safe,_ = actor.assess(previous,np.array([endpoint]),seconds,interval,interval,inputs['dimensions'])
            if not safe[0]:
                return abort('held_command_exhausts_traffic_margin') if recovery_planner is not None else result('incomplete','held_command_exhausts_traffic_margin')
        position = endpoint
        if performance and not performance.covered(state.wind_mps):outside_coverage += interval
        if 'storage' in inputs:
            bus=solar*state.solar_fraction-load
            net=(min(bus*charging,inputs['storage']['maxChargeW']) if bus>=0 else bus/discharge)-inputs['storage']['selfDischargeW']
        else:
            net = solar*state.solar_fraction*charging-load/discharge
        stored = min(capacity,stored+net*interval/3600)
        minimum=min(minimum,stored);seconds+=interval;distance+=float(np.linalg.norm(position-previous))
        turn_remaining=max(0.,turn_remaining-interval)
        for actor in traffic:
            if actor.collides(previous,position,seconds-interval,interval,inputs['dimensions']):
                return result('safety_violation','traffic_collision')
        if stored < reserve:
            reserve_protected = False
            return abort('course_recovery_reserve_trigger') if recovery_planner is not None else result('incomplete','recovery_reserve_reached')
        if phase < len(sequence):
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
                    history.append([seconds,*position,stored,'finished',seconds>=comms_until])
                    return result('qualified_completion','ordered_gates_without_intervention')
            elif gates[name].distance(Point(position)) > 1e-6:
                last_off_line[phase]=position.copy()
        if step % save_every == 0:
            history.append([seconds,*position,stored,mode,seconds>=comms_until])
        step += 1
    return result('censored','computational_horizon')

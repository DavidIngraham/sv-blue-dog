"""Chart-route recovery with native SysML current and reserve arithmetic.

Destinations are explicit assessed water approaches to shore retrieval sites.
An approach endpoint alone does not establish beaching or land access evidence.
"""
from sysml_python import execution_session
from dataclasses import dataclass
import math

import numpy as np
from shapely.geometry import LineString, Point

from tools.boat_analysis.environment.routing import reference_route
from tools.boat_analysis.generated import recovery_segment


@dataclass(frozen=True)
class RecoverySite:
    name: str
    approach: tuple[float, float]
    shore_access_evidence: str
    approach_evidence: str


@dataclass(frozen=True)
class RecoveryCapability:
    speed_mps: float
    motor_w: float
    essential_w: float
    uncertainty_factor: float
    arrival_allowance_wh: float
    capsized_speed_mps: float | None = None
    capsized_motor_w: float | None = None

    def __post_init__(self):
        values = (self.speed_mps, self.motor_w, self.essential_w,
                  self.uncertainty_factor, self.arrival_allowance_wh)
        if not all(math.isfinite(v) for v in values) or min(values[:3]) <= 0 or self.uncertainty_factor < 1 or self.arrival_allowance_wh < 0:
            raise ValueError('Invalid recovery capability')
        if (self.capsized_speed_mps is None) != (self.capsized_motor_w is None):
            raise ValueError('Capsized speed and power must be supplied together')
        if self.capsized_speed_mps is not None and (not all(math.isfinite(v) and v > 0 for v in (self.capsized_speed_mps, self.capsized_motor_w))):
            raise ValueError('Invalid capsized capability')


@dataclass(frozen=True)
class RecoveryPlan:
    site: RecoverySite
    route: LineString
    seconds: float
    reserve_wh: float
    capsized: bool


class RecoveryPlanner:
    def __init__(self, water, sites, capability, spacing=40, kernel=None):
        self.water, self.sites, self.capability = water, tuple(sites), capability
        if spacing <= 0 or not math.isfinite(spacing):
            raise ValueError('Positive routing spacing required')
        self.spacing = spacing
        if not self.sites or len({s.name for s in self.sites}) != len(self.sites):
            raise ValueError('Distinct named recovery sites required')
        for site in self.sites:
            if not site.shore_access_evidence or not site.approach_evidence or not water.covers(Point(site.approach)):
                raise ValueError('Recovery site requires evidence references and an in-domain approach')
        self.kernel = kernel or recovery_segment

    def segment(self, distance, unit, current, capsized=False):
        c = self.capability
        if capsized and c.capsized_speed_mps is None:
            return None
        current = np.asarray(current, dtype=float)
        if current.shape != (2,) or not np.isfinite(current).all():
            raise ValueError('Finite two-dimensional current required')
        along = float(np.dot(current, unit))
        cross = float(current[0]*unit[1]-current[1]*unit[0])
        values = self.kernel(x=[distance, c.capsized_speed_mps if capsized else c.speed_mps,
                              along, cross, c.capsized_motor_w if capsized else c.motor_w,
                              c.essential_w, c.uncertainty_factor]).as_array()
        return values if values[0] == 1 else None

    @execution_session()
    def plan(self, position, current, capsized=False, *, contacts=(), start_seconds=0., dimensions=(1.2,.5,1.), preferred_site=None):
        """Least reserve among chart-clear routes, under the supplied current field.

        current may be a vector or a spatial callable. None means no modeled
        recovery route; it must never become a zero-energy reserve.
        """
        if capsized and self.capability.capsized_speed_mps is None:
            return None
        candidates = []
        for site in self.sites:
            direct = LineString([position, site.approach])
            try:
                route = direct if self.water.covers(direct) else reference_route(self.water, position, site.approach, self.spacing)
            except ValueError:
                continue
            seconds, energy = 0., self.capability.arrival_allowance_wh
            for a, b in zip(route.coords, list(route.coords)[1:]):
                delta = np.asarray(b)-a; distance = float(np.linalg.norm(delta))
                if distance == 0:
                    continue
                flow = current((np.asarray(a)+b)/2) if callable(current) else current
                value = self.segment(distance, delta/distance, flow, capsized)
                if value is None:
                    break
                if any(not actor.assess(np.asarray(a),np.asarray([b]),start_seconds+seconds,value[2],value[2],dimensions)[0][0] for actor in contacts):
                    break
                seconds += value[2]; energy += value[3]
            else:
                candidates.append(RecoveryPlan(site, route, seconds, energy, capsized))
        return min(candidates, key=lambda p: (p.site.name!=preferred_site,p.reserve_wh,p.seconds,p.site.name), default=None)


@dataclass
class RecoveryResult:
    outcome: str
    destination: str | None
    seconds: float
    energy_wh: float
    position: list[float]
    history: list
    collision: bool = False
    clearance_violated: bool = False


def execute_recovery(planner, position, seconds, energy_wh, current_at, *,
                     capsized=False, dt=10., horizon_seconds=86400., traffic=(), dimensions=(1.2, .5, 1.), observations=None):
    """Execute a recovery route with time-varying current and no solar credit.

    Traffic here is truth for consequence assessment, not an assumed backup
    detector. Arrival means the mapped water approach, not proven shore capture.
    """
    if not math.isfinite(dt) or dt <= 0 or not math.isfinite(horizon_seconds) or horizon_seconds <= 0 or not math.isfinite(energy_wh) or energy_wh < 0:
        raise ValueError('Finite recovery time and energy required')
    point = np.asarray(position, dtype=float)
    if point.shape != (2,) or not np.isfinite(point).all():
        raise ValueError('Finite recovery start required')
    plan = planner.plan(point, lambda p: current_at(p, seconds), capsized)
    if plan is None:
        return RecoveryResult('no_modeled_recovery_route', None, seconds, energy_wh, point.tolist(), [])
    if observations is not None and observations.last_time<0:observations.activate(seconds)
    history = []; deadline = seconds+horizon_seconds
    clearance = False
    c = planner.capability
    power = (c.capsized_motor_w if capsized else c.motor_w)+c.essential_w
    targets=list(plan.route.coords)[1:]
    while targets:
        target = np.asarray(targets[0])
        while np.linalg.norm(target-point) > 1e-7:
            if seconds >= deadline:
                return RecoveryResult('recovery_censored', plan.site.name, seconds, energy_wh, point.tolist(), history, clearance_violated=clearance)
            contacts=[]
            if observations is not None:
                contacts=observations.observe(traffic,point,seconds)
                alternative=planner.plan(point,lambda p:current_at(p,seconds),capsized,contacts=contacts,start_seconds=seconds,dimensions=dimensions,preferred_site=plan.site.name)
                if alternative is None:
                    return RecoveryResult('recovery_observed_obstruction',plan.site.name,seconds,energy_wh,point.tolist(),history,clearance_violated=clearance)
                if alternative.reserve_wh>energy_wh:
                    return RecoveryResult('recovery_energy_insufficient',alternative.site.name,seconds,energy_wh,point.tolist(),history,clearance_violated=clearance)
                plan=alternative;targets=list(plan.route.coords)[1:];target=np.asarray(targets[0])
            delta = target-point; length = float(np.linalg.norm(delta)); unit = delta/length
            segment = planner.segment(length, unit, current_at(point, seconds), capsized)
            if segment is None:
                return RecoveryResult('recovery_current_exceeds_authority', plan.site.name, seconds, energy_wh, point.tolist(), history, clearance_violated=clearance)
            interval = min(dt, segment[2], deadline-seconds)
            if observations is not None:
                interval=min(interval,observations.next_boundary(seconds)-seconds)
                proposed=point+unit*segment[1]*interval
                if any(not actor.assess(point,np.array([proposed]),seconds,interval,interval,dimensions)[0][0] for actor in contacts):
                    return RecoveryResult('recovery_observed_obstruction',plan.site.name,seconds,energy_wh,point.tolist(),history,clearance_violated=clearance)
            available = max(0., energy_wh-c.arrival_allowance_wh)
            if power*interval/3600 > available:
                return RecoveryResult('recovery_energy_insufficient', plan.site.name, seconds, energy_wh, point.tolist(), history, clearance_violated=clearance)
            previous = point.copy(); point = point+unit*segment[1]*interval
            if not planner.water.covers(LineString([previous, point])):
                return RecoveryResult('recovery_outside_chart', plan.site.name, seconds, energy_wh, previous.tolist(), history, clearance_violated=clearance)
            collision = any(actor.collides(previous, point, seconds, interval, dimensions) for actor in traffic)
            for actor in traffic:
                safe,_=actor.assess(previous,np.array([point]),seconds,interval,interval,dimensions)
                clearance |= not bool(safe[0])
            seconds += interval; energy_wh -= power*interval/3600
            history.append([seconds, *point, energy_wh, 'powered_recovery'])
            if collision:
                return RecoveryResult('recovery_collision', plan.site.name, seconds, energy_wh, point.tolist(), history, True, clearance)
        else:
            targets.pop(0)
    return RecoveryResult('recovery_approach_reached', plan.site.name, seconds, energy_wh, point.tolist(), history, clearance_violated=clearance)


@dataclass
class DriftResult:
    termination: str
    seconds: float
    energy_wh: float
    position: list
    history: list
    collision: bool = False
    clearance_violated: bool = False
    energy_exhausted: bool = False


def execute_drift(water, position, seconds, energy_wh, current_at, *, dt, horizon_seconds,
                  essential_w, traffic=(), dimensions=(1.2,.5,1.)):
    """Post-abort consequence integration, with no station keeping or rescue credit.

    Water-current advection only; windage, capsize drift and shore impact physics
    are uncorrelated. Horizon expiry remains a censored consequence.
    """
    from shapely import get_coordinates
    if not all(math.isfinite(v) for v in (seconds,energy_wh,dt,horizon_seconds,essential_w)) or dt<=0 or min(energy_wh,horizon_seconds,essential_w)<0:
        raise ValueError('Invalid drift inputs')
    point=np.asarray(position,dtype=float)
    if point.shape!=(2,) or not np.isfinite(point).all():raise ValueError('Invalid drift position')
    history=[];deadline=seconds+horizon_seconds;clearance=False;exhausted=energy_wh<=0
    def result(termination,collision=False):
        return DriftResult(termination,seconds,energy_wh,point.tolist(),history,collision,clearance,exhausted)
    if not water.covers(Point(point)):return result('shore_contact')
    while seconds<deadline-1e-9:
        velocity=np.asarray(current_at(point,seconds),dtype=float)
        if velocity.shape!=(2,) or not np.isfinite(velocity).all():raise ValueError('Invalid current')
        interval=min(dt,deadline-seconds)
        if essential_w>0 and energy_wh>0:interval=min(interval,energy_wh*3600/essential_w)
        previous=point.copy();endpoint=point+velocity*interval
        segment=LineString([previous,endpoint]);grounded=not water.covers(segment)
        if grounded and segment.length>0:
            crossings=get_coordinates(segment.intersection(water.boundary))
            distances=[segment.project(Point(p)) for p in crossings]
            fraction=min(distances)/segment.length if distances else 0.
            interval*=fraction;endpoint=previous+velocity*interval
        collision=False
        if interval>0:
            for actor in traffic:
                collision |= actor.collides(previous,endpoint,seconds,interval,dimensions)
                safe,_=actor.assess(previous,np.array([endpoint]),seconds,interval,interval,dimensions)
                clearance |= not bool(safe[0])
        point=endpoint;seconds+=interval;energy_wh=max(0.,energy_wh-essential_w*interval/3600)
        if energy_wh<1e-10:energy_wh=0.;exhausted=True
        history.append([seconds,*point,energy_wh,'unpowered_drift'])
        if collision:return result('drift_collision',True)
        if grounded:return result('shore_contact')
    return result('drift_censored')

"""Chart-route recovery with native SysML current and reserve arithmetic.

Destinations are explicit assessed water approaches to shore retrieval sites.
An approach endpoint alone does not establish beaching or land access evidence.
"""
from dataclasses import dataclass
import math

import numpy as np
from shapely.geometry import LineString, Point

from tools.boat_analysis.environment.routing import reference_route
from tools.boat_analysis.model.surface import NativeCalculation


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
        self.kernel = kernel or NativeCalculation('MarineRecovery::Segment', 1)

    def segment(self, distance, unit, current, capsized=False):
        c = self.capability
        if capsized and c.capsized_speed_mps is None:
            return None
        current = np.asarray(current, dtype=float)
        if current.shape != (2,) or not np.isfinite(current).all():
            raise ValueError('Finite two-dimensional current required')
        along = float(np.dot(current, unit))
        cross = float(current[0]*unit[1]-current[1]*unit[0])
        values = self.kernel([distance, c.capsized_speed_mps if capsized else c.speed_mps,
                              along, cross, c.capsized_motor_w if capsized else c.motor_w,
                              c.essential_w, c.uncertainty_factor])
        return values if values[0] == 1 else None

    def plan(self, position, current, capsized=False):
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
                seconds += value[2]; energy += value[3]
            else:
                candidates.append(RecoveryPlan(site, route, seconds, energy, capsized))
        return min(candidates, key=lambda p: (p.reserve_wh, p.seconds, p.site.name), default=None)


@dataclass
class RecoveryResult:
    outcome: str
    destination: str | None
    seconds: float
    energy_wh: float
    position: list[float]
    history: list
    collision: bool = False


def execute_recovery(planner, position, seconds, energy_wh, current_at, *,
                     capsized=False, dt=10., horizon_seconds=86400., traffic=(), dimensions=(1.2, .5, 1.)):
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
    history = []; deadline = seconds+horizon_seconds
    c = planner.capability
    power = (c.capsized_motor_w if capsized else c.motor_w)+c.essential_w
    for target in list(plan.route.coords)[1:]:
        target = np.asarray(target)
        while np.linalg.norm(target-point) > 1e-7:
            if seconds >= deadline:
                return RecoveryResult('recovery_censored', plan.site.name, seconds, energy_wh, point.tolist(), history)
            delta = target-point; length = float(np.linalg.norm(delta)); unit = delta/length
            segment = planner.segment(length, unit, current_at(point, seconds), capsized)
            if segment is None:
                return RecoveryResult('recovery_current_exceeds_authority', plan.site.name, seconds, energy_wh, point.tolist(), history)
            interval = min(dt, segment[2], deadline-seconds)
            available = max(0., energy_wh-c.arrival_allowance_wh)
            if power*interval/3600 > available:
                return RecoveryResult('recovery_energy_insufficient', plan.site.name, seconds, energy_wh, point.tolist(), history)
            previous = point.copy(); point = point+unit*segment[1]*interval
            if not planner.water.covers(LineString([previous, point])):
                return RecoveryResult('recovery_outside_chart', plan.site.name, seconds, energy_wh, previous.tolist(), history)
            collision = any(actor.collides(previous, point, seconds, interval, dimensions) for actor in traffic)
            seconds += interval; energy_wh -= power*interval/3600
            history.append([seconds, *point, energy_wh, 'powered_recovery'])
            if collision:
                return RecoveryResult('recovery_collision', plan.site.name, seconds, energy_wh, point.tolist(), history, True)
    return RecoveryResult('recovery_approach_reached', plan.site.name, seconds, energy_wh, point.tolist(), history)

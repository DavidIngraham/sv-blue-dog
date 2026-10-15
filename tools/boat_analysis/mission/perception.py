"""Sampled hypothetical observations; future truth tracks never reach guidance."""
from dataclasses import dataclass
import math
import numpy as np
from shapely.geometry import LineString
from .traffic import Traffic


@dataclass(frozen=True)
class SensorEnvelope:
    craft_range_m: float
    low_range_m: float
    weed_range_m: float
    cooperative_range_m: float = 0.
    period_s: float = 1.
    latency_s: float = 0.
    miss_probability: float = 0.
    error_m: float = 0.
    expiry_s: float = 10.
    night_factor: float = 1.

    def __post_init__(self):
        values = tuple(self.__dict__.values())
        if not all(math.isfinite(v) and v >= 0 for v in values):
            raise ValueError('Finite nonnegative observation parameters required')
        if self.period_s <= 0 or self.expiry_s <= 0 or not 0 <= self.miss_probability <= 1 or not 0 <= self.night_factor <= 1:
            raise ValueError('Invalid observation probability or clock')


class Observations:
    def __init__(self, envelope, seed=0, *, night=False, dropouts=()):
        self.envelope, self.seed, self.night = envelope, seed, night
        self.dropouts = tuple(dropouts)
        if any(not (math.isfinite(a) and math.isfinite(b) and 0 <= a < b) for a,b in self.dropouts):
            raise ValueError('Invalid dropout interval')
        self.next_sample = 0.
        self.sample = 0
        self.pending, self.tracks, self.trace = [], {}, []
        self.last_time = -1.

    def next_boundary(self, seconds):
        times = [self.next_sample, *[p[0] for p in self.pending],
                 *[p[1]+self.envelope.expiry_s for p in self.tracks.values()]]
        return min((t for t in times if t > seconds+1e-9), default=math.inf)

    def observe(self, truth, own_position, seconds):
        if seconds < self.last_time:
            raise ValueError('Observation clock must be monotone')
        self.last_time = seconds
        e = self.envelope
        if seconds+1e-9 >= self.next_sample:
            # The integrator visits each sample boundary; do not fabricate past
            # ownship positions if a caller skipped a sample.
            if seconds-self.next_sample > 1e-7:
                raise ValueError('Missed observation sampling boundary')
            outage = any(a <= seconds < b for a,b in self.dropouts)
            for i, actor in enumerate(truth):
                if not actor.start_seconds <= seconds <= actor.end_seconds:
                    continue
                rng = np.random.default_rng(np.random.SeedSequence([self.seed,i,self.sample]))
                missed = rng.random() < e.miss_probability
                radius = {'low':e.low_range_m, 'weed':e.weed_range_m}.get(actor.target_kind,e.craft_range_m)
                radius *= e.night_factor if self.night and actor.target_kind != 'weed' else 1.
                if actor.ais_equipped:
                    radius = max(radius,e.cooperative_range_m)
                point = actor.position(seconds)
                # Circumscribed target extent is a conservative detection proxy.
                distance = max(0.,np.linalg.norm(point-own_position)-math.hypot(actor.length_m,actor.beam_m)/2)
                if outage or missed or radius <= 0 or distance > radius:
                    continue
                angle = rng.uniform(0,2*math.pi)
                observed = point+e.error_m*np.array([math.cos(angle),math.sin(angle)])
                earlier = max(actor.start_seconds,seconds-.01)
                velocity = (point-actor.position(earlier))/(seconds-earlier) if seconds>earlier else np.zeros(2)
                # Exact instantaneous speed is a stated hypothesis, not a peek at
                # future vertices. Later reversals cannot be forecast from truth.
                contact = (i,seconds,observed,velocity,actor)
                self.pending.append((seconds+e.latency_s,contact))
                self.trace.append(dict(sampleSeconds=seconds,deliverySeconds=seconds+e.latency_s,actor=actor.name,distanceM=float(distance)))
            self.sample += 1
            self.next_sample = self.sample*e.period_s
        for due,contact in self.pending:
            if due <= seconds+1e-9:
                i,sampled,point,velocity,actor = contact
                self.tracks[i] = (actor,sampled,point,velocity)
        self.pending = [(due,c) for due,c in self.pending if due > seconds+1e-9]
        self.tracks = {i:c for i,c in self.tracks.items() if seconds-c[1] < e.expiry_s}
        contacts = []
        for i,(actor,sampled,point,velocity) in self.tracks.items():
            position = point+velocity*(seconds-sampled)
            speed = float(np.linalg.norm(velocity))
            endpoint = position+velocity*3600 if speed else position+np.array([1.,0.])
            contacts.append(Traffic(actor.name,LineString([position,endpoint]),seconds,speed,
                actor.length_m+2*e.error_m,actor.beam_m+2*e.error_m,actor.clearance_m,
                stationary_seconds=3600.,target_kind=actor.target_kind,ais_equipped=actor.ais_equipped,source_id=i))
        return contacts

    def summary(self):
        return dict(mode='sampled_hypothesis',samples=self.sample,deliveredOrPendingDetections=len(self.trace),
                    trace=self.trace,physicalValidation=False,
                    scope='Range, Bernoulli misses, latency, bounded position error, expiry and scheduled outages; exact instantaneous velocity/extent; no false positives or measured sensor physics')

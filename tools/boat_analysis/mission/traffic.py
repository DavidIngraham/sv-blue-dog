"""Moving traffic envelopes with continuous relative-motion collision checks.

Tracks are scenario inputs. An AIS tug position must represent its whole tow;
small craft need independent non-AIS scenarios. These checks are geometric,
not a complete implementation or certification of the Navigation Rules.
"""
from dataclasses import dataclass
import math

import numpy as np
from shapely.geometry import LineString, box


@dataclass(frozen=True)
class Traffic:
    name: str
    track: LineString
    start_seconds: float
    speed_mps: float
    length_m: float
    beam_m: float
    clearance_m: float
    stationary_seconds: float = 0.
    target_kind: str = "craft"
    ais_equipped: bool = False
    source_id: int | None = None

    def __post_init__(self):
        if min(self.length_m,self.beam_m,self.track.length) <= 0 or self.clearance_m < 0 or self.speed_mps < 0 or (self.speed_mps == 0 and self.stationary_seconds <= 0):
            raise ValueError('Invalid traffic geometry or speed')

    @property
    def end_seconds(self):
        return self.start_seconds+(self.track.length/self.speed_mps if self.speed_mps else self.stationary_seconds)

    def position(self, seconds):
        return np.array(self.track.interpolate((seconds-self.start_seconds)*self.speed_mps).coords[0])

    def _conflict(self, previous, endpoint, seconds, interval, own_dimensions, clearance):
        if seconds+interval < self.start_seconds or seconds > self.end_seconds:
            return False
        low=max(seconds,self.start_seconds);high=min(seconds+interval,self.end_seconds)
        # Split exactly at all track vertices: each subinterval is linear motion.
        lengths=np.linalg.norm(np.diff(np.array(self.track.coords),axis=0),axis=1)
        turns=self.start_seconds+np.cumsum(lengths)/self.speed_mps if self.speed_mps else []
        boundaries=[low,*[v for v in turns if low<v<high],high]
        for a,b in zip(boundaries,boundaries[1:]):
            pa,pb=self.position(a),self.position(b)
            vector=pb-pa;norm=np.linalg.norm(vector)
            if norm==0:
                vector=np.array(self.track.coords[1])-np.array(self.track.coords[0]);norm=np.linalg.norm(vector)
            forward=vector/norm;lateral=np.array([-forward[1],forward[0]])
            own_a=previous+(endpoint-previous)*(a-seconds)/interval
            own_b=previous+(endpoint-previous)*(b-seconds)/interval
            ra,rb=own_a-pa,own_b-pb
            relative=LineString([(ra@forward,ra@lateral),(rb@forward,rb@lateral)])
            # Circumscribe own hull independent of its heading; never shrink a
            # broadside ownship footprint to its beam alone.
            radius=math.hypot(own_dimensions[0],own_dimensions[1])/2+clearance
            envelope=box(-self.length_m/2-radius,-self.beam_m/2-radius,
                         self.length_m/2+radius,self.beam_m/2+radius)
            if relative.intersects(envelope):return True
        return False

    def assess(self, previous, endpoints, seconds, interval, forecast, own_dimensions):
        if seconds+forecast < self.start_seconds or seconds > self.end_seconds:
            return np.ones(len(endpoints),dtype=bool),np.zeros(len(endpoints))
        reach=(np.linalg.norm(endpoints-previous,axis=1).max()/interval+self.speed_mps)*forecast
        reach+=self.length_m+self.beam_m+self.clearance_m+own_dimensions[0]
        if np.linalg.norm(self.position(max(seconds,self.start_seconds))-previous)>reach:
            return np.ones(len(endpoints),dtype=bool),np.zeros(len(endpoints))
        safe=np.array([not self._conflict(previous,p,seconds,interval,own_dimensions,self.clearance_m) for p in endpoints])
        future=previous+(endpoints-previous)*forecast/interval
        penalty=np.array([100000. if self._conflict(previous,p,seconds,forecast,own_dimensions,self.clearance_m) else 0. for p in future])
        return safe,penalty

    def collides(self, previous, endpoint, seconds, interval, own_dimensions):
        return self._conflict(previous,endpoint,seconds,interval,own_dimensions,0)

"""Local course geometry shared by mission execution and chart checks.

Use a fixed equirectangular frame over the Gorge, in meters. This approximation
is for mission analysis; it is not a hydrographic survey or a navigation system.
"""
from dataclasses import dataclass
import math

from shapely.geometry import LineString


@dataclass(frozen=True)
class LocalFrame:
    longitude: float = -121.55
    latitude: float = 45.67

    def project(self, longitude, latitude):
        scale = math.pi * 6371008.8 / 180
        return ((longitude - self.longitude) * scale * math.cos(math.radians(self.latitude)),
                (latitude - self.latitude) * scale)

    def unproject(self, x, y):
        scale = math.pi * 6371008.8 / 180
        return (self.longitude + x / (scale * math.cos(math.radians(self.latitude))),
                self.latitude + y / scale)


def marker_gate(values, frame=LocalFrame()):
    """Model tuple: nominal lon, lat, true bearing, near and far offsets."""
    lon, lat, bearing, near, far = values
    if not all(math.isfinite(v) for v in values) or not 0 < near < far:
        raise ValueError("Gate requires finite coordinates and 0 < near < far")
    x, y = frame.project(lon, lat)
    angle = math.radians(bearing)
    return LineString([(x + d * math.sin(angle), y + d * math.cos(angle)) for d in (near, far)])


def crossing_direction(gate, previous, current):
    """Return -1/+1 for a side-changing finite-segment crossing, else zero.

    Ordered endpoints define the positive side by their 2-D cross product.
    Merely reaching, following or starting on the line is not a crossing.
    The mission state machine must retain its last off-line point through a
    sample landing on the line, so the next sample can establish direction.
    """
    (ax, ay), (bx, by) = gate.coords
    def side(p):
        return (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)
    before, after = side(previous), side(current)
    if before * after >= 0:
        return 0
    if not LineString([previous, current]).intersects(gate):
        return 0
    return 1 if after > 0 else -1

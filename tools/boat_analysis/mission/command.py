"""Command delivery and non-restarting maneuver clocks, independent of integration."""
import math

class CommandClock:
    def __init__(self, latency, maneuver):
        if not all(math.isfinite(v) and v >= 0 for v in (latency,maneuver)):
            raise ValueError('Finite nonnegative command and maneuver times required')
        self.latency,self.maneuver=latency,maneuver
        self.heading=None
        self.pending=None
        self.ends=0.
        self.trace=[]

    def drifting(self, seconds):
        return seconds < self.ends-1e-9

    def busy(self, seconds):
        return self.pending is not None or self.drifting(seconds)

    def select(self, seconds, heading, turn):
        if self.busy(seconds):
            raise ValueError('Cannot overwrite an in-flight command or maneuver')
        self.pending=dict(selectedSeconds=seconds,appliedSeconds=seconds+self.latency,
                          heading=heading,turn=bool(turn))

    def advance(self, seconds):
        if self.pending is None or seconds+1e-9 < self.pending['appliedSeconds']:
            return False
        row=self.pending;self.pending=None
        self.heading=row['heading']
        self.ends=row['appliedSeconds']+(self.maneuver if row['turn'] else 0.)
        self.trace.append(dict(**row,maneuverCompleteSeconds=self.ends))
        return row['turn']

    def next_boundary(self, seconds):
        values=[self.ends]
        if self.pending is not None:values.append(self.pending['appliedSeconds'])
        return min((v for v in values if v>seconds+1e-9),default=math.inf)

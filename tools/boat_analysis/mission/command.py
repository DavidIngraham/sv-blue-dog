"""Command delivery and non-restarting maneuver clocks, independent of integration."""
import math

class CommandClock:
    def __init__(self, latency, maneuver, dynamics=None):
        if not all(math.isfinite(v) and v >= 0 for v in (latency,maneuver)):
            raise ValueError('Finite nonnegative command and maneuver times required')
        self.latency,self.maneuver=latency,maneuver
        self.dynamics=dynamics
        self.heading=None if dynamics is None else dynamics.heading
        self.target_heading=None
        self.kind="turn"
        self.pending=None
        self.ends=0.
        self.trace=[]

    def drifting(self, seconds):
        return self.dynamics is None and seconds < self.ends-1e-9

    def busy(self, seconds):
        return self.pending is not None or seconds < self.ends-1e-9 or (self.dynamics is not None and self.dynamics.turning(self.target_heading))

    def select(self, seconds, heading, turn, kind="turn"):
        if self.busy(seconds):
            raise ValueError('Cannot overwrite an in-flight command or maneuver')
        self.pending=dict(selectedSeconds=seconds,appliedSeconds=seconds+self.latency,
                          heading=heading,turn=bool(turn))
        if self.dynamics is not None:self.pending["kind"]=kind

    def advance(self, seconds):
        if self.dynamics is not None and self.trace and not self.busy(seconds) and self.trace[-1].get('status') not in {'interrupted','cancelled'}:
            self.trace[-1].setdefault('actualManeuverCompleteSeconds',seconds)
            self.trace[-1]['status']='completed'
        if self.pending is None or seconds+1e-9 < self.pending['appliedSeconds']:
            return False
        row=self.pending;self.pending=None
        self.target_heading=row['heading']
        self.kind=row.get('kind','turn')
        if self.dynamics is None:self.heading=row['heading']
        self.ends=row['appliedSeconds']+(self.maneuver if row['turn'] else 0.)
        if self.dynamics is None:
            self.trace.append(dict(**row,maneuverCompleteSeconds=self.ends))
        else:
            self.trace.append(dict(**row,earliestManeuverCompleteSeconds=self.ends,
                                   completionRequiresAchievedHeading=True,status="active"))
        return row['turn']

    def cancel(self, seconds, reason):
        """Invalidate motion without claiming an interrupted turn was achieved."""
        if self.dynamics is not None:
            if self.pending is not None:
                row=self.pending.copy()
                row['scheduledAppliedSeconds']=row.pop('appliedSeconds')
                self.trace.append(dict(**row,status='cancelled',cancelledSeconds=seconds,reason=reason))
            elif self.trace and self.trace[-1].get('status') not in {'completed','interrupted','cancelled'}:
                if self.busy(seconds):
                    self.trace[-1].update(status='interrupted',interruptedSeconds=seconds,reason=reason)
                else:
                    self.trace[-1].update(status='completed',actualManeuverCompleteSeconds=seconds)
        self.pending=None
        self.heading=None
        self.target_heading=None
        self.ends=seconds

    def next_boundary(self, seconds):
        values=[self.ends]
        if self.pending is not None:values.append(self.pending['appliedSeconds'])
        return min((v for v in values if v>seconds+1e-9),default=math.inf)

"""Opt-in low-order maneuver dynamics, with equations and defaults in SysML.

Python performs heading geometry and midpoint trajectory integration. Coefficients
are unvalidated scenario hypotheses; neither this adapter nor a completed turn
establishes a physical maneuver envelope. Legacy missions do not instantiate it.
"""
import math
from tools.boat_analysis.model.runtime import load_model, numerical_value


def angle_error(target, heading):
    return (target-heading+180.) % 360.-180.


def maneuver_kind(heading, target, wind_from):
    """Classify crossings of the wind-from/away rays on the shortest turn arc."""
    if target is None:
        return 'turn'
    delta=angle_error(target,heading)
    for ray,kind in ((wind_from,'tack'),(wind_from+180.,'gybe')):
        crossing=angle_error(ray,heading)
        if abs(crossing)>1e-9 and crossing*delta>0 and abs(crossing)<=abs(delta):
            return kind
    return 'turn'


class ManeuverDynamics:
    def __init__(self, initial_heading, coefficients=None, initial_speed=0.):
        if not all(math.isfinite(v) for v in (initial_heading,initial_speed)) or initial_speed<0:
            raise ValueError('Finite heading and nonnegative initial speed required')
        self.model=load_model()
        self.coefficients=numerical_value(self.model.run_analysis('BlueDog::Analyses::ManeuverDynamics::Defaults').outputs)
        if coefficients:
            if set(coefficients)-set(self.coefficients):raise ValueError('Unknown maneuver coefficient')
            self.coefficients.update(coefficients)
        c=self.coefficients
        if not all(math.isfinite(v) for v in c.values()) or min(c.values())<0:
            raise ValueError('Finite nonnegative maneuver coefficients required')
        if c['authoritySpeedMps']<=c['minimumSteerSpeedMps'] or min(c['maxTurnRateDegS'],c['accelerationMps2'],c['decelerationMps2'])<=0:
            raise ValueError('Positive turn/acceleration limits and ordered authority speeds required')
        if any(c[k]>1 for k in c if k.endswith('Retention')):
            raise ValueError('Speed retention must be between zero and one')
        self.heading=float(initial_heading)%360.;self.speed=float(initial_speed)
        self.trace=[]

    def turning(self, target):
        return target is not None and abs(angle_error(target,self.heading))>1e-7

    def step(self, target_heading, target_speed_mps, dt_seconds, kind='turn', rudder_fraction=1.):
        if kind not in {'turn','tack','gybe','recovery'}:raise ValueError('Unknown maneuver kind')
        values=[target_speed_mps,dt_seconds,rudder_fraction]
        if target_heading is not None:values.append(target_heading)
        if not all(math.isfinite(v) for v in values) or target_speed_mps<0 or dt_seconds<=0 or not 0<=rudder_fraction<=1:
            raise ValueError('Invalid maneuver step')
        turning=self.turning(target_heading)
        c=self.coefficients
        args={k:c[k] for k in ('maxTurnRateDegS','authoritySpeedMps','minimumSteerSpeedMps','accelerationMps2','decelerationMps2')}
        args.update(headingErrorDeg=angle_error(target_heading,self.heading) if turning else 0.,
                    speedMps=self.speed,targetSpeedMps=target_speed_mps,intervalS=dt_seconds,
                    rudderFraction=rudder_fraction,speedRetention=c[kind+'SpeedRetention'] if turning else 1.)
        result=numerical_value(dict(self.model.execute_action('BlueDog::Analyses::ManeuverDynamics::Advance',inputs=args)))
        midpoint=math.radians(self.heading+result['deltaHeadingDeg']/2)
        self.heading=(self.heading+result['deltaHeadingDeg'])%360.;self.speed=result['speedNextMps']
        result.update(headingDeg=self.heading,speedMps=self.speed,meanSpeedMps=result['speedMeanMps'],
                      kind=kind,turning=self.turning(target_heading),
                      velocity=[result['speedMeanMps']*math.cos(midpoint),result['speedMeanMps']*math.sin(midpoint)])
        self.trace.append(dict(inputs=args,outputs=result.copy()))
        return result

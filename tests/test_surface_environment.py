"""Physical limits and independent arithmetic oracles for surface screening."""
import math
import sys

import numpy as np
import pytest

pytestmark=pytest.mark.skipif(sys.platform!='linux',reason='Native C adapters require GCC')


@pytest.fixture(scope='module')
def kernels():
    from tools.boat_analysis.model.surface import NativeCalculation
    return {n:NativeCalculation('MarineSurface::'+n,1) for n in ('WindSample','StripLoad','WaveScreen','FetchSea','SpeedRetention')}


def test_log_profile_reference_height_and_near_surface(kernels):
    wind=kernels['WindSample']
    for height in (1.,2.,10.):
        actual=wind([10,10,.0002,height,0,0,0,1,.05])
        expected=math.log(height/.0002)/math.log(10/.0002)
        assert actual[0]==pytest.approx(expected)
        assert actual[3]==pytest.approx(10*expected)
    assert wind([10,10,.0002,.01,0,0,0,1,.05])[4]<0


def test_strip_force_direction_and_moment(kernels):
    # Existing body-frame wind-from convention: lift +x, side force +y.
    result=kernels['StripLoad']([1.2,2,0,5,0,3,1,.1,.5,.2])
    assert result==pytest.approx([30,3,9,3])


def test_calm_and_opposing_current_wave_limits(kernels):
    wave=kernels['WaveScreen'];x=[.4,3,0,1.4,.5,1,-1,1,.2,.3,.5,9.80665,1000]
    base=wave(x)
    assert base[0]==pytest.approx(.4)
    assert base[1]==pytest.approx(9.80665*9/(2*math.pi))
    against=x.copy();against[2]=-.4
    adverse=wave(against)
    assert adverse[0]>base[0] and adverse[1]<base[1]
    calm=x.copy();calm[0]=0
    assert wave(calm)[3]==0
    following=x.copy();following[6]=1
    assert wave(following)[3]<base[3]
    blocked=x.copy();blocked[2]=-2
    assert wave(blocked)[4]<0
    assert kernels['SpeedRetention']([0,10])[0]==1
    assert kernels['SpeedRetention']([20,10])[0]==0


def test_fetch_growth_and_persistent_reversal(kernels):
    growth=kernels['FetchSea']
    assert growth([8,15000,9.80665])[0]>growth([8,3000,9.80665])[0]
    assert growth([0,8000,9.80665])[0]==0
    from tools.boat_analysis.environment.trajectories import Weather
    from tools.boat_analysis.environment.surface import SeaHistory
    from types import SimpleNamespace
    weather=SimpleNamespace(rows=[Weather(270,8,.4,0),Weather(90,8,.4,0)])
    sea=SeaHistory(weather,[8000,2,1,.3,2,120,300])
    assert {r[2] for r in sea.at(3600)}=={90,270}


def test_uniform_strip_provider_matches_legacy_upright_loads():
    from tools.boat_analysis.model.vessel import CoupledModel
    from tools.boat_analysis.model.surface import SurfaceOperation
    model=CoupledModel();d=model.c['referenceDesign'];p=model.parameters
    state=[5,1,1,2,50,4,1,-2,0]
    hydro=[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]
    aero=model.polar.evaluate(d[5],d[6],4)
    mass=[1.]*21
    base=model.operation.evaluate(d,p,state,aero,mass,hydro)
    surface=SurfaceOperation(model.operation,model.polar,[10,.0002,.05,8],shear=False)
    actual=surface.evaluate(d,p,state,aero,mass,hydro)
    for key in ('surgeResidual','swayResidual','yawResidual','rollResidual','wingTorque','averagePower','wingRe'):
        assert actual[key]==pytest.approx(base[key],rel=1e-10,abs=1e-10)


def test_quadrature_refinement_and_shear_reduce_drive():
    from tools.boat_analysis.model.vessel import CoupledModel
    from tools.boat_analysis.model.surface import SurfaceOperation
    m=CoupledModel();d=m.c['referenceDesign'];s=[8,1,1,2,50,4,1,-2,0]
    a=m.polar.evaluate(d[5],d[6],4);h=[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]
    uniform=SurfaceOperation(m.operation,m.polar,[10,.0002,.05,8],shear=False).evaluate(d,m.parameters,s,a,[1.]*21,h)
    outputs=[SurfaceOperation(m.operation,m.polar,[10,.0002,.05,n]).evaluate(d,m.parameters,s,a,[1.]*21,h) for n in (8,16)]
    assert outputs[0]['drive']<uniform['drive']
    assert outputs[0]['drive']==pytest.approx(outputs[1]['drive'],rel=.01)
    assert outputs[0]['windRatioMin']<outputs[0]['windRatioMax']<1


def test_unsupported_wind_bracket_is_not_interpolated():
    from tools.boat_analysis.mission.candidate import Performance
    p=Performance(dict(winds=[5,8],validWinds=[True,False],velocities=[[[1,1],[1,-1],[-1,1],[-1,-1]]]*2))
    assert p.covered(5)
    assert not p.covered(6) and not p.covered(8)
    assert p.speeds(6,0)==0


def test_wake_is_triggered_once_and_expires():
    from types import SimpleNamespace
    from shapely.geometry import LineString
    from tools.boat_analysis.environment.surface import WaveEffects
    from tools.boat_analysis.environment.trajectories import Weather
    from tools.boat_analysis.mission.traffic import Traffic
    weather=SimpleNamespace(rows=[Weather(270,0,0,0)]*2)
    inputs={'surfaceEnvironment':dict(seaPolicy=[8000,2,1,.3,2,120,300],winds=[5,8],
            calmResistanceN=[10,20],geometry=[1.4,.5,.2,.2,.3])}
    actor=Traffic('recreational powerboat',LineString([(0,0),(1000,0)]),0,5,7,2.5,30)
    waves=WaveEffects(inputs,weather,[actor]);waves.update(0,[0,50],[0,0])
    reduced=waves.evaluate(5,[90],[1])[0]
    assert len(waves.seen)==1 and 0<=reduced<1
    waves.update(121,[500,50],[0,0])
    assert not waves.wakes and len(waves.seen)==1
    assert waves.evaluate(5,[90],[1])[0]==1
    assert np.ndim(waves.evaluate(5,90,1.))==0


def test_mission_executes_scalar_wave_adjusted_speed():
    from shapely.geometry import LineString,box
    from tools.boat_analysis.mission.engine import simulate
    inputs=dict(controlPeriodSeconds=10,gateNames=['gate'],gateDirections=[1],gateApproachM=20,
        time=[10,10/3600,10,20,0,1],energy=[100,80,10,1,0,0,.8,.9],dimensions=[1.4,.5,3],
        weather=[270,7,0,36,.2,.85,0,.15,.8,.08,0,6,18,8],angles=[0,180],speedRatios=[.2,.2],
        surfaceEnvironment=dict(motionPolicy=[1,1,32,.35],seaPolicy=[8000,2,1,.3,2,120,300],winds=[5,8],calmResistanceN=[10,20],geometry=[1.4,.5,.2,.2,.3]))
    route=LineString([(0,0),(-100,0)]);water=box(-200,-100,100,100)
    result=simulate(inputs,route,water,{'gate':LineString([(0,-100),(0,100)])},classify=lambda *facts:'censored')
    assert result.elapsed_seconds==10
    assert result.surface_summary['maximumSignificantHeightM']>0
    assert result.surface_summary['maximumAddedResistanceN']>0
    assert 'minimumWingClearanceM' in result.surface_summary['samples'][0]


def test_motion_point_velocity_matches_finite_difference():
    from tools.boat_analysis.environment.motion import point_motion
    pose=np.array([.2,.13,-.09,.4,-.3,.2]);point=[.3,.1,1.4]
    position,velocity,_=point_motion(point,pose)
    later=pose.copy();later[:3]+=pose[3:]*1e-7
    assert (point_motion(point,later)[0]-position)/1e-7==pytest.approx(velocity,abs=1e-7)


def test_wave_following_cancels_center_clearance_but_not_wind_height():
    from tools.boat_analysis.environment.motion import MotionResponse,point_motion
    train=[(.2,.3,1.,0.)]
    follow=MotionResponse([1,0,32,.35]);fixed=MotionResponse([0,0,32,.35])
    geometry=[1.4,.5,.1,.1,.4]
    assert follow.clearance(train,geometry)['minimumWingClearanceM']==pytest.approx(.1)
    assert fixed.clearance(train,geometry)['minimumWingClearanceM']==pytest.approx(-.1)
    heights=[point_motion([0,0,1],pose)[0][2] for pose,_ in follow.samples(train)]
    assert max(heights)-min(heights)==pytest.approx(.4)
    assert follow.clearance([],geometry)['minimumHullClearanceM']==pytest.approx(.1)


def test_harmonic_velocity_signed_encounter():
    from tools.boat_analysis.environment.motion import MotionResponse
    response=MotionResponse([1,1,32,.35]);kernel=response.kernel
    x=np.array([.2,.3,-1.2,.7,.4,1.,1.])
    state=kernel(x);later=x.copy();later[3]-=x[2]*1e-7
    assert (kernel(later)[:3]-state[:3])/1e-7==pytest.approx(state[3:],abs=1e-7)


def test_zero_motion_preserves_strip_solution():
    from tools.boat_analysis.model.vessel import CoupledModel
    from tools.boat_analysis.model.surface import SurfaceOperation
    m=CoupledModel();d=m.c['referenceDesign'];s=[8,1,1,2,50,4,1,-2,0]
    a=m.polar.evaluate(d[5],d[6],4);h=[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]
    provider=SurfaceOperation(m.operation,m.polar,[10,.0002,.05,8])
    args=(d,m.parameters,s,a,[1.]*21,h)
    baseline=provider.evaluate(*args);moving=provider.evaluate(*args,motion=np.zeros(6))
    assert moving==pytest.approx(baseline)
    heave=provider.evaluate(*args,motion=[.2,0,0,0,0,0])
    assert heave['windRatioMin']>baseline['windRatioMin']

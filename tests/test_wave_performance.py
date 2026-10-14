"""Independent limits for wave response, inertia, loads and mission caching."""
import sys
import numpy as np
import pytest
pytestmark=pytest.mark.skipif(sys.platform!='linux',reason='Native physics uses Linux GCC')


def test_uniform_tetrahedron_moments():
    from tools.boat_analysis.hydrodynamics.inertia import distribution
    vertices=np.array([[[0,0,0],[1,0,0],[0,1,0],[0,0,1]]],float)
    mass,first,second=distribution(vertices,[1],2)
    assert mass==2
    assert first==pytest.approx([.5,.5,.5])
    assert np.diag(second)==pytest.approx([.2,.2,.2])
    assert second[0,1]==pytest.approx(.1)


def test_native_wave_kinematics_and_damped_oscillator():
    from tools.boat_analysis.model.surface import NativeCalculation
    orbital=NativeCalculation('MarineWavePerformance::OrbitalVelocity',1)
    surface=orbital([.1,1,2,0,0,0,9.80665]);deep=orbital([.1,1,2,-1,0,0,9.80665])
    assert surface==pytest.approx([.2,0,0])
    assert deep[0]==pytest.approx(.2/np.e)
    assert orbital([.1,1,2,0,np.pi/2,0,9.80665])[2]==pytest.approx(.2)
    kernel=NativeCalculation('MarineWavePerformance::ImpedanceTerm',1)
    real,imag=kernel([2,2,0,8,4,0])
    # At resonance, amplitude = force/(damping*omega), response lags force.
    response=1/complex(real,imag)
    assert abs(response)==pytest.approx(1/8)
    assert response.real==pytest.approx(0)


def test_foil_limits_and_steady_force_oracle():
    from tools.boat_analysis.model.surface import NativeCalculation
    foil=NativeCalculation('MarineWavePerformance::FoilLoad',1)
    result=foil([1000,.1,.5,1,.05,0,.8,.01,1,1,.2,1])
    cl=2*np.pi/(1+2/(.8*2.5))*.05
    assert result[:2]==pytest.approx([50*cl,50*(.01+cl**2/(np.pi*.8*2.5))])
    assert foil([1000,.1,.5,1,.05,0,.8,.01,1,1,.2,0])[:2]==pytest.approx([0,0])


def cache(supported=True):
    nodes=[]
    for wind in (5.,8.):
        for height in (0.,.04):
            for direction in (0.,180.):
                speed=1-height*10
                nodes.append(dict(wind=wind,height=height,period=3.,direction=direction,
                    velocities=[[0,0],[speed,speed],[speed,-speed],[-speed,speed],[-speed,-speed]],
                    powerW=10.,supported=supported or height==0))
    return dict(nodes=nodes,scope='test')


def test_wave_cache_interpolates_and_never_crosses_unsupported_nodes():
    from tools.boat_analysis.mission.wave_performance import WavePerformance
    p=WavePerformance(cache());assert p.set_condition(6,.02,3,270)
    assert p.speeds(6,0)==pytest.approx(.8)
    assert not p.set_condition(6,.05,3,0)
    assert not p.set_condition(6,.02,2.9,0)
    assert p.speeds(6,0)==0
    p=WavePerformance(cache(False));assert not p.set_condition(6,.02,3,0)
    assert p.set_condition(6,0,3,0)


def test_mission_wave_cache_supplies_power_without_second_speed_penalty(monkeypatch):
    from shapely.geometry import LineString,box
    from tools.boat_analysis.mission.engine import simulate
    class NoWaves:
        def __init__(self,*args):self.components=[];self.seen=set();self.diagnostics=[]
        def update(self,*args):pass
        def evaluate(self,*args,**kwargs):
            self.diagnostics=[dict(significantHeightM=0.,addedResistanceN=0.,speedRetention=0.,contactScreen=False,covered=True)]
            return np.array([0.])
    monkeypatch.setattr('tools.boat_analysis.environment.surface.WaveEffects',NoWaves)
    inputs=dict(controlPeriodSeconds=10,gateNames=['gate'],gateDirections=[1],gateApproachM=20,
        time=[10,10/3600,10,20,0,1],energy=[100,80,10,1,0,0,.8,1.],dimensions=[1.4,.5,3],
        weather=[270,7,0,36,.2,.85,0,.15,.8,.08,0,6,18,8],angles=[0,180],speedRatios=[.2,.2],
        surfaceEnvironment={},wavePerformance=cache(),performance=dict(winds=[5,8],velocities=[[[0,0],[1,1],[1,-1],[-1,1],[-1,-1]]]*2,scope='test'))
    result=simulate(inputs,LineString([(0,0),(-100,0)]),box(-200,-100,100,100),{'gate':LineString([(0,-100),(0,100)])},classify=lambda *facts:'censored')
    assert result.distance_m>5
    assert result.minimum_energy_wh==pytest.approx(80-10*10/3600)


def test_motion_about_offset_origin_has_correct_point_velocity():
    from tools.boat_analysis.environment.motion import point_motion
    pose=np.array([.2,.13,-.09,.4,-.3,.2]);point=[.3,.1,1.4];origin=[-.1,0,-.3]
    position,velocity,_=point_motion(point,pose,origin);later=pose.copy();later[:3]+=pose[3:]*1e-7
    assert (point_motion(point,later,origin)[0]-position)/1e-7==pytest.approx(velocity,abs=1e-7)


def test_capytaine_long_wave_heave_follows_surface():
    import capytaine as cpt
    from capytaine.bem.airy_waves import froude_krylov_force
    # Half-submerged unit sphere: waterplane area pi, displaced mass 2*pi*rho/3.
    mesh=cpt.mesh_sphere(radius=1.,resolution=(12,24))
    body=cpt.FloatingBody(mesh=mesh,name='heave_limit');body.add_translation_dof(name='Heave');body=body.immersed_part()
    solver=cpt.BEMSolver();omega=.15;rho=1000.;g=9.80665
    radiation=solver.solve(cpt.RadiationProblem(body=body,omega=omega,radiating_dof='Heave',rho=rho,g=g),keep_details=False)
    diffraction=solver.solve(cpt.DiffractionProblem(body=body,omega=omega,wave_direction=0.,rho=rho,g=g),keep_details=False)
    force=diffraction.forces['Heave']+froude_krylov_force(diffraction.problem)['Heave']
    z=rho*g*np.pi-omega**2*(rho*2*np.pi/3+radiation.added_mass['Heave'])-1j*omega*radiation.radiation_damping['Heave']
    response=force/z
    assert response.real==pytest.approx(1.,abs=.05)
    assert abs(response.imag)<.05


@pytest.mark.parametrize('typed',[False,True])
def test_small_wave_limit_recovers_steady_balance_and_power(typed):
    from types import SimpleNamespace
    from tools.boat_analysis.model.vessel import CoupledModel
    from tools.boat_analysis.model.surface import SurfaceOperation
    from tools.boat_analysis.model.wave_performance import WaveAveragedOperation
    model=CoupledModel();design=model.c['referenceDesign'];state=[8,1,1,2,50,4,1,-2,0]
    hydro=[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727];mass=[1.]*21
    aero=model.polar.evaluate(design[5],design[6],4)
    class QuietResponse:
        policy=dict(settings=[16,.04,.2,.05,.05,.5,25,5,.15,.02],speeds=[0,3])
        meta=dict(cg=[0,0,0],draftM=.1)
        def mesh_error(self,*args):return 0.
        def samples(self,a,period,speed,direction,count):
            for i in range(count):yield np.zeros(6),-2*np.pi*i/count,(2*np.pi/period)**2/9.80665,2*np.pi/period
    if typed:
        from tools.boat_analysis.model.design_boundary import unpack
        from tools.boat_analysis.model.design_types import OperatingState,AeroCoefficients,MassProperties,HydroState
        state,aero,mass,hydro=(unpack(t,v,model.operating_contract[t.sysml_id+'Fields'])
            for t,v in zip((OperatingState,AeroCoefficients,MassProperties,HydroState),(state,aero,mass,hydro),strict=True))
        design=model.design_record(design)
    steady=SurfaceOperation(model.operating_contract,model.polar,[10,.0002,.05,8]).evaluate(design,model.parameters,state,aero,mass,hydro)
    dynamic=WaveAveragedOperation(model.operating_contract,model.polar,[10,.0002,.05,8],QuietResponse(),1e-9,3,0).evaluate(design,model.parameters,state,aero,mass,hydro)
    for key in ('surgeResidual','swayResidual','yawResidual','rollResidual','averagePower','rudderTorque'):
        assert dynamic[key]==pytest.approx(steady[key],rel=1e-7,abs=1e-7),key


def test_stored_wind_coordinate_matches_cartesian_lift_and_roll_velocity():
    from tools.boat_analysis.model.surface import NativeCalculation,SurfaceOperation
    from tools.boat_analysis.model.vessel import CoupledModel
    strip=NativeCalculation('MarineSurface::StripLoad',1)
    force=strip([1.2,1,3,4,0,1,1,0,1,0])
    assert np.dot(force[:2],[3,-4])==pytest.approx(0,abs=1e-12)
    m=CoupledModel();d=m.c['referenceDesign'];state=[8,1,1,2,50,4,1,-2,0]
    h=[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727];a=m.polar.evaluate(d[5],d[6],4)
    provider=SurfaceOperation(m.operating_contract,m.polar,[10,.0002,.05,8])
    quiet=provider.evaluate(d,m.parameters,state,a,[1.]*21,h,motion=np.zeros(6))
    rolling=provider.evaluate(d,m.parameters,state,a,[1.]*21,h,motion=[0,0,0,0,0,.1])
    assert rolling['localAlphaMin']>quiet['localAlphaMin']

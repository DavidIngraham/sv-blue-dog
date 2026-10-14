from tools.boat_analysis.evidence.records import baseline_record as input_record
"""Independent force/moment, submerged-surface and drive-energy checks."""
import itertools,json,sys
import numpy as np
import pytest
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.vessel import skin_triangles,wet_area
from tools.boat_analysis.geometry.vessel import ballast_geometry,metrics
from tools.boat_analysis.geometry.hydro import convex_tetrahedra


def test_wetted_surface_excludes_waterplane_cap():
    box=convex_tetrahedra(np.array(list(itertools.product([-1,1],repeat=3)),dtype=float))
    triangles=skin_triangles(box)
    assert wet_area(triangles,-2)==0
    assert wet_area(triangles,0)==pytest.approx(12)
    assert wet_area(triangles,2)==pytest.approx(24)
    assert wet_area(triangles+[0,0,8],8)==pytest.approx(12)


def test_ballast_volume_and_nonoverlap():
    for volume in [.0001,.001,.01]:
        body,center=ballast_geometry(volume,-.7)
        assert metrics(body)[4]==pytest.approx(volume,rel=1e-12)
        np.testing.assert_allclose(metrics(body)[5:8],center,atol=1e-12)
        assert body[:,:,2].max()==pytest.approx(-.7,abs=1e-12)


@pytest.fixture
def native_case():
    if sys.platform!='linux':pytest.skip('Native operation adapter uses Linux/GCC')
    from tools.boat_analysis.generated import operation
    k=operation;r=input_record('coupled-operation-audit.json');d,p,q,s,a,m,h=r['inputs']
    # Archived fixtures predate elevated equipment; preserve their original case.
    p = [*p, 0, 0, 0]
    return k,[np.array(v,dtype=float) for v in [d,p,s,a,m,h]],r


def test_compiled_operation_matches_interpreter(native_case):
    from tools.boat_analysis.evidence.records import input_record as current_record
    k,_,_=native_case
    r=current_record('coupled-operation-audit.json')
    d,p,q,s,a,m,h=r['inputs']
    args=[np.array(v,dtype=float) for v in [d,p,s,a,m,h]]
    np.testing.assert_array_equal(k.prepare_inputs(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)['environment'],q)
    result=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)))
    for name,value in r['outputs'].items():assert result[name]==pytest.approx(value,abs=1e-10,rel=1e-11)


def test_direct_aerodynamic_moment_is_independent_of_lift_credit(native_case):
    k,args,_=native_case
    d,p,s,a,m,h=[x.copy() for x in args]
    d[8]=.5  # Mast through the polar's midchord moment reference.
    original=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    p[16]*=.5
    lower_lift=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    assert lower_lift['wingTorque']==pytest.approx(original['wingTorque'])
    assert lower_lift['yawResidual']!=pytest.approx(original['yawResidual'])


def test_mast_reference_shift_conserves_total_yaw(native_case):
    k,args,_=native_case;d,p,s,a,m,h=args
    # Headwind, zero incidence/heel: chord points aft and positive lift is +Y.
    original=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)));change=.12;chord=np.sqrt(d[4]/d[5])
    d[8]+=change;d[9]-=change*chord/d[0]
    shifted=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)))
    assert shifted['yawResidual']==pytest.approx(original['yawResidual'],abs=1e-12)
    assert shifted['wingTorque']!=pytest.approx(original['wingTorque'])


def test_locked_drive_saves_holding_power_without_free_motion(native_case):
    k,args,_=native_case;d,p,s,a,m,h=args
    locked=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)));p[5]=2
    powered=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)))
    assert powered['averagePower']-locked['averagePower']==pytest.approx(2*p[7])
    p[5]=0;p[1]/=2
    inefficient=k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)))
    assert inefficient['averagePower']>locked['averagePower']
    p[7]=1
    with pytest.raises(ValueError,match='wingDuty'):k(**dict(zip(('design','parameters','state','aero','mass','hydro'),args,strict=True)))


def test_route_tack_weights_cancel_crosswind_velocity(native_case):
    from tools.boat_analysis.model.operating import RouteKernel
    k=RouteKernel();states=[]
    for up in [True,False,True,False]:
        angle=45 if up else 135
        states.extend([np.sqrt(2),angle,0,0,0,0])
        states.extend([3*np.sqrt(2),-angle,0,0,0,0])
    r=k.evaluate([1,3]*4,states)
    assert r[3]==pytest.approx(.95*1.5+.75)
    assert r[4]==pytest.approx(.95*1.5-.75)
    leg_length=k.contract['routeParameters'][3]
    assert r[5]==pytest.approx(leg_length/3600*(1/r[3]+1/r[4]))


def test_coupled_geometry_mass_and_hydrostatics_share_wing_pose(native_case):
    from tools.boat_analysis.model.vessel import CoupledModel
    model=CoupledModel();x=model.c['referenceDesign'];b1,m1,g1,_=model.configuration(x,0);b2,m2,g2,_=model.configuration(x,np.pi)
    assert m1['totalMass']==pytest.approx(m2['totalMass'])
    assert m1['cgY']==pytest.approx(-m2['cgY'])
    assert abs(m1['cgY'])>1e-4
    for bodies,m in [(b1,m1),(b2,m2)]:
        wing=next(b.tetrahedra for b in bodies if b.name=='wing')
        full=model.hydro.moments(wing,10)
        np.testing.assert_allclose(full[1:]/full[0],metrics(wing)[5:8],atol=1e-10)


def test_structural_stiffness_and_strength_respond_to_material_evidence(native_case):
    from tools.boat_analysis.generated import structure
    from tools.boat_analysis.model.vessel import CoupledModel
    model=CoupledModel();x=model.c['referenceDesign']
    _,m,g,_=model.configuration(x,0);p=model.parameters.copy()
    nominal=structure(design=x, parameters=p, mass=list(m.values()), geometry=g, loads=[50,60,10], waterline=0)
    # The CAD crescent's weak-axis stiffness invalidates the previous generic-box screen.
    assert nominal['wingDeflectionMargin']<0
    assert nominal['wingStressMargin']>0
    p[13]=.5
    weak=structure(design=x, parameters=p, mass=list(m.values()), geometry=g, loads=[50,60,10], waterline=0)
    for name in ['wingDeflectionMargin','keelDeflectionMargin','hullStressMargin','rudderStressMargin']:
        assert 1-weak[name]==pytest.approx(2*(1-nominal[name]))
    for name in ['bodyHandlingMargin','freeboardMargin','panelAreaMargin']:
        assert weak[name]==pytest.approx(nominal[name])


def test_generated_interfaces_are_homogeneous_real_sequences(native_case):
    import re
    for name in ['mass','operation','structure','route']:
        path = ROOT/'tools/boat_analysis/generated'/f'{name}.c' if name in ('mass','structure','operation') else ROOT/f'.tools/coupled-{name}.c'
        text=path.read_text()
        signature=re.search(r'int sysml_run\((.*?)\) \{',text,re.S)
        assert signature[1].endswith('sysml_seq_real *result')


def test_native_hull_resistance_is_in_force_balance_and_domain_outputs(native_case):
    from tools.boat_analysis.model.resistance import HullResistanceKernel
    k,args,_=native_case
    d,p,s,a,m,h=[x.copy() for x in args]
    base=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    bare=HullResistanceKernel().evaluate(h[3:],s[3],p[31],p[34])
    p[24]=1.3
    increased=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    assert increased['hullDrag']-base['hullDrag']==pytest.approx(.3*bare['resistance_N'])
    assert increased['resistance']-base['resistance']==pytest.approx(.3*bare['resistance_N'])
    h[10]=.65
    outside=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    assert outside['delftDomain9']<0


def test_loaded_waterline_does_not_move_hardware_lever_arms(native_case):
    k,args,_=native_case
    d,p,s,a,m,h=[x.copy() for x in args]
    s[4]=45.;s[6]=0.;s[7]=3.;d[9]=.1
    base=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    h[3]*=.9
    changed=k(design=d,parameters=p,state=s,aero=a,mass=m,hydro=h)
    assert changed['yawResidual']==pytest.approx(base['yawResidual'],abs=1e-12)
    assert changed['hullDrag']!=pytest.approx(base['hullDrag'])


def test_shared_search_jacobian_preserves_both_constraint_blocks():
    from tools.boat_analysis.optimization.search import Problem
    p=Problem.__new__(Problem);p.derivatives=None;calls=[]
    def constraints(z):
        calls.append(z.copy())
        return {'eq':np.array([2*z[0]+3*z[1]]),'ineq':np.array([4*z[0]-5*z[1],z[0]+z[1]])}
    p.evaluate=constraints;z=np.array([.3,1.])
    eq,ineq=p.jacobians(z)
    np.testing.assert_allclose(eq,[[2,3]],atol=1e-9)
    np.testing.assert_allclose(ineq,[[4,-5],[1,1]],atol=1e-9)
    assert len(calls)==3
    p.jacobians(z.copy())
    assert len(calls)==3


def test_panel_fit_uses_actual_deck_area(native_case):
    from tools.boat_analysis.generated import structure
    from tools.boat_analysis.model.vessel import CoupledModel
    model=CoupledModel();x=model.c['referenceDesign'];_,m,g,_=model.configuration(x,0)
    p=model.parameters
    before=structure(design=x, parameters=p, mass=list(m.values()), geometry=g, loads=[50,60,10], waterline=0)
    smaller=g.copy();smaller[51]*=.8
    after=structure(design=x, parameters=p, mass=list(m.values()), geometry=smaller, loads=[50,60,10], waterline=0)
    assert after['panelAreaMargin']+1==pytest.approx(.8*(before['panelAreaMargin']+1))
    assert after['bodyHandlingMargin']==before['bodyHandlingMargin']
    assert g[51]<np.pi*x[0]*x[1]/4


def test_design_cache_preserves_state_dependent_results(native_case):
    from tools.boat_analysis.optimization.search import Problem
    p=Problem(4);z=p.initial();initial=p.evaluate(z);cached=p.design_cache
    assert len(p.constraint_names)==len(initial['ineq'])==len(set(p.constraint_names))
    trial=z.copy();trial[29]+=.001
    used=p.evaluate(trial)
    assert p.design_cache is cached
    p.last=None;p.design_cache=None
    fresh=p.evaluate(trial)
    np.testing.assert_allclose(used['eq'],fresh['eq'],atol=1e-12)
    np.testing.assert_allclose(used['ineq'],fresh['ineq'],atol=1e-12)


def test_finite_search_keeps_peak_but_removes_daily_energy_constraints(native_case):
    from tools.boat_analysis.optimization.search import Problem
    p=Problem(4,route_profile='all-season');r=p.evaluate(p.initial())
    from tools.boat_analysis.optimization.operating import operating_margin_names
    names=operating_margin_names(p.model.operating_contract['outputNames'])[:12]
    assert 'peakMargin' in names
    assert 'cycleMargin' not in names and 'reserveMarginScaled' not in names
    assert not any('cycleMargin' in n or 'reserveMarginScaled' in n for n in p.constraint_names)
    assert p.route.contract['routeParameters'][4] == 0
    selected=r['ineq'][:8*len(names)].reshape(8,len(names))
    raw=np.array([[row[n] for n in names] for row in r['rows']])
    difference=raw-selected
    np.testing.assert_allclose(difference,0,atol=1e-12)
    for direction,raw_route in [('easterly',r['route']),('westerly',r['westerlyRoute'])]:
        for i,leg in enumerate(['downstream progress','upstream progress']):
            margin=r['ineq'][p.constraint_names.index(f'{direction} {leg}')]
            assert raw_route[i]-margin==pytest.approx(.005/p.route.contract['routeParameters'][5])
    assert p.route.contract['routeParameters'][5]==.5
    for row in r['rows']:
        assert row['cycleMargin']==pytest.approx(row['cycleEnergy']/100)


def test_route_assigns_easterly_upstream_to_windward(native_case):
    from tools.boat_analysis.model.operating import RouteKernel
    kernel=RouteKernel();states=[]
    for windward in [True,False,True,False]:
        speed=np.sqrt(2)*(1 if windward else 2)
        angle=45 if windward else 135
        for tack in [1,-1]:states.extend([speed,tack*angle,0,0,0,0])
    water=[1,1,2,2]*2
    east=kernel.evaluate(water,states)
    west=kernel.evaluate(water,states,wind_from='west')
    assert east[3]==pytest.approx(.95*2+.75)
    assert east[4]==pytest.approx(.95*1-.75)
    assert west[3]==pytest.approx(.95*1+.75)
    assert west[4]==pytest.approx(.95*2-.75)
    assert east[5]>west[5]


def test_native_structure_uses_finite_inertia_and_section_modulus(native_case):
    from tools.boat_analysis.generated import structure
    from tools.boat_analysis.model.vessel import CoupledModel
    model=CoupledModel();x=model.c['referenceDesign'];_,m,g,_=model.configuration(x,0)
    p=model.parameters;loads=[50,60,10]
    before=structure(design=x, parameters=p, mass=list(m.values()), geometry=g, loads=loads, waterline=0)
    stiffer=g.copy();stiffer[56]*=2
    after=structure(design=x, parameters=p, mass=list(m.values()), geometry=stiffer, loads=loads, waterline=0)
    assert 1-after['keelDeflectionMargin']==pytest.approx((1-before['keelDeflectionMargin'])/2)
    assert after['keelStressMargin']==before['keelStressMargin']
    stronger=g.copy();stronger[57]*=2
    after=structure(design=x, parameters=p, mass=list(m.values()), geometry=stronger, loads=loads, waterline=0)
    assert 1-after['keelStressMargin']==pytest.approx((1-before['keelStressMargin'])/2)
    assert after['keelDeflectionMargin']==before['keelDeflectionMargin']


def test_search_derivative_does_not_cross_a_polar_interpolation_breakpoint():
    from tools.boat_analysis.optimization.search import Problem
    p=Problem.__new__(Problem);p.derivatives=None;p.breakpoints={0:np.array([0.,.5,1.])}
    def constraints(z):
        value=2*z[0] if z[0]<.5 else 1+5*(z[0]-.5)
        return {'eq':np.array([value]),'ineq':np.array([value-2,3-value])}
    p.evaluate=constraints
    for point,expected in [(.5-1e-6,2.),(.5+1e-6,5.),(.5,5.)]:
        eq,ineq=p.jacobians(np.array([point]))
        np.testing.assert_allclose(eq,[[expected]],atol=1e-8)
        np.testing.assert_allclose(ineq,[[expected],[-expected]],atol=1e-8)
        np.testing.assert_allclose(p.residual_jacobian(np.array([point])),[[expected],[expected],[0]],atol=1e-8)

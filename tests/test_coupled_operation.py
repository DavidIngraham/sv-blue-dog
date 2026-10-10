"""Independent force/moment, submerged-surface and drive-energy checks."""
import itertools,json,sys
import numpy as np
import pytest
from scripts.native_design_kernel import ROOT
from scripts.coupled_model import skin_triangles,wet_area
from scripts.coupled_geometry import ballast_geometry,metrics
from scripts.hydro_geometry import convex_tetrahedra


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
    from scripts.native_coupled_operation import OperationKernel
    k=OperationKernel();r=json.loads((ROOT/'docs/analysis/coupled-operation-audit.json').read_text());d,p,q,s,a,m,h=r['inputs']
    return k,[np.array(v,dtype=float) for v in [d,p,s,a,m,h]],r


def test_compiled_operation_matches_interpreter(native_case):
    k,args,r=native_case
    result=k.evaluate(*args)
    for name,value in r['outputs'].items():assert result[name]==pytest.approx(value,abs=1e-10,rel=1e-11)


def test_mast_reference_shift_conserves_total_yaw(native_case):
    k,args,_=native_case;d,p,s,a,m,h=args
    # Headwind, zero incidence/heel: chord points aft and positive lift is +Y.
    original=k.evaluate(*args);change=.12;chord=np.sqrt(d[4]/d[5])
    d[8]+=change;d[9]-=change*chord/d[0]
    shifted=k.evaluate(*args)
    assert shifted['yawResidual']==pytest.approx(original['yawResidual'],abs=1e-12)
    assert shifted['wingTorque']!=pytest.approx(original['wingTorque'])


def test_locked_drive_saves_holding_power_without_free_motion(native_case):
    k,args,_=native_case;d,p,s,a,m,h=args
    locked=k.evaluate(*args);p[5]=2
    powered=k.evaluate(*args)
    assert powered['averagePower']-locked['averagePower']==pytest.approx(2*p[7])
    p[5]=0;p[1]/=2
    inefficient=k.evaluate(*args)
    assert inefficient['averagePower']>locked['averagePower']
    p[7]=1
    with pytest.raises(ValueError,match='duty'):k.evaluate(*args)


def test_route_tack_weights_cancel_crosswind_velocity(native_case):
    from scripts.native_coupled_operation import RouteKernel
    k=RouteKernel();states=[]
    for up in [True,False,True,False]:
        angle=45 if up else 135
        states.extend([np.sqrt(2),angle,0,0,0,0])
        states.extend([3*np.sqrt(2),-angle,0,0,0,0])
    r=k.evaluate([1,3]*4,states)
    assert r[3]==pytest.approx(.95*1.5+.75)
    assert r[4]==pytest.approx(.95*1.5-.75)
    assert r[5]==pytest.approx(100000/3600*(1/r[3]+1/r[4]))


def test_coupled_geometry_mass_and_hydrostatics_share_wing_pose(native_case):
    from scripts.coupled_model import CoupledModel
    model=CoupledModel();x=model.c['referenceDesign'];b1,m1,g1,_=model.configuration(x,0);b2,m2,g2,_=model.configuration(x,np.pi)
    assert m1['totalMass']==pytest.approx(m2['totalMass'])
    assert m1['cgY']==pytest.approx(-m2['cgY'])
    assert abs(m1['cgY'])>1e-4
    for bodies,m in [(b1,m1),(b2,m2)]:
        wing=next(b.tetrahedra for b in bodies if b.name=='wing')
        full=model.hydro.moments(wing,10)
        np.testing.assert_allclose(full[1:]/full[0],metrics(wing)[5:8],atol=1e-10)


def test_structural_stiffness_and_strength_respond_to_material_evidence(native_case):
    from scripts.native_coupled_operation import StructureKernel
    from scripts.coupled_model import CoupledModel
    k=StructureKernel();model=CoupledModel();x=model.c['referenceDesign']
    _,m,g,_=model.configuration(x,0);p=model.parameters.copy()
    nominal=k.evaluate(x,p,list(m.values()),g,[50,60,10],0)
    # The CAD crescent's weak-axis stiffness invalidates the previous generic-box screen.
    assert nominal['wingDeflectionMargin']<0
    assert nominal['wingStressMargin']>0
    p[13]=.5
    weak=k.evaluate(x,p,list(m.values()),g,[50,60,10],0)
    for name in ['wingDeflectionMargin','keelDeflectionMargin','hullStressMargin','rudderStressMargin']:
        assert 1-weak[name]==pytest.approx(2*(1-nominal[name]))
    for name in ['bodyHandlingMargin','freeboardMargin','panelAreaMargin']:
        assert weak[name]==pytest.approx(nominal[name])


def test_generated_interfaces_are_homogeneous_real_sequences(native_case):
    import re
    for name in ['mass','operation','structure','route']:
        text=(ROOT/f'.tools/coupled-{name}.c').read_text()
        signature=re.search(r'int sysml_run\((.*?)\) \{',text,re.S)
        assert signature[1].endswith('sysml_seq_real *result')

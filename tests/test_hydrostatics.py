"""Independent convex-hull oracle and analytic buoyancy/torque checks."""
import itertools,sys
import numpy as np
import pytest
from scipy.spatial import ConvexHull
from scripts.hydro_geometry import convex_tetrahedra,equilibrium,DisplacementBody,pose

@pytest.fixture(scope='module')
def kernel():
    if sys.platform!='linux':pytest.skip('Native compiled kernel requires Linux/GCC')
    from scripts.native_hydrostatics import HydroKernel
    return HydroKernel()


def oracle(points,height):
    vertices=[p for p in points if p[2]<=height]
    for a,b in itertools.combinations(points,2):
        if (a[2]<height<b[2]) or (b[2]<height<a[2]):vertices.append(a+(b-a)*(height-a[2])/(b[2]-a[2]))
    vertices=np.unique(np.round(vertices,12),axis=0)
    if len(vertices)<4:return np.zeros(4)
    hull=ConvexHull(vertices);center=vertices.mean(axis=0);result=np.zeros(4)
    for face in hull.simplices:
        tetra=np.vstack([center,vertices[face]])
        volume=abs(np.linalg.det((tetra[1:]-tetra[0]).T))/6
        result+=np.r_[volume,volume*tetra.mean(axis=0)]
    return result


def test_clipping_matches_independent_convex_hull_for_all_wet_counts(kernel):
    rng=np.random.default_rng(51)
    for _ in range(15):
        p=rng.normal(size=(4,3));heights=sorted(p[:,2]);cuts=[heights[0]-.1,*[(a+b)/2 for a,b in zip(heights,heights[1:])],heights[-1]+.1]
        for h in cuts:
            np.testing.assert_allclose(kernel.moments(p[None],h),oracle(p,h),atol=1e-10,rtol=1e-9)


def test_vertex_plane_and_vertex_permutation_invariance(kernel):
    p=np.array([[0.,0.,0.],[1,0,0],[0,1,0],[0,0,1]])
    for h in [0,.5,1]:
        for order in itertools.permutations(range(4)):
            np.testing.assert_allclose(kernel.moments(p[list(order)][None],h),oracle(p,h),atol=1e-12)


def test_box_displacement_translation_and_small_angle_metacentric_height(kernel):
    # Unit cube centered at origin, mass=half freshwater displacement, CG=-0.2.
    cube=convex_tetrahedra(list(itertools.product([-.5,.5],repeat=3)))
    upright=equilibrium(kernel,[DisplacementBody('cube',cube)],[0,0,-.2],500,0)
    assert upright['waterline_m']==pytest.approx(0,abs=1e-9)
    assert upright['righting_Nm']==pytest.approx(0,abs=1e-9)
    heeled=equilibrium(kernel,[DisplacementBody('cube',cube)],[0,0,-.2],500,.01)
    gm=-.25+1/6+.2
    assert heeled['righting_Nm']/(500*9.80665*np.sin(np.deg2rad(.01)))==pytest.approx(gm,rel=1e-6)
    shifted=equilibrium(kernel,[DisplacementBody('cube',cube+[2,3,4])],[2,3,3.8],500,0)
    assert shifted['waterline_m']==pytest.approx(4,abs=1e-9)
    assert shifted['righting_Nm']==pytest.approx(0,abs=1e-8)


def test_pitch_and_roll_are_distinct_and_sink_is_rejected(kernel):
    cube=convex_tetrahedra(list(itertools.product([-.5,.5],repeat=3)))
    pitched=equilibrium(kernel,[DisplacementBody('cube',cube)],[0,0,-.2],500,0,5)
    assert pitched['pitch_torque_Nm']<0
    assert abs(pitched['roll_torque_Nm'])<1e-8
    with pytest.raises(ValueError,match='Insufficient'):equilibrium(kernel,[DisplacementBody('cube',cube)],[0,0,0],1100,0)

def test_free_pitch_solves_offset_cg_and_reports_inverted_instability(kernel):
    from scripts.hydro_geometry import free_pitch_equilibrium
    cube=convex_tetrahedra(list(itertools.product([-.5,.5],repeat=3)))
    body=[DisplacementBody('cube',cube)]
    result=free_pitch_equilibrium(kernel,body,[.01,0,-.2],500,0)
    assert abs(result['pitch_torque_Nm'])<1e-6
    assert result['pitch_stable']
    assert abs(result['pitch_deg'])>0.01
    inverted=free_pitch_equilibrium(kernel,body,[0,0,-.2],500,180)
    assert not inverted['pitch_stable']


def test_geometry_changes_with_wing_camber_and_trim_without_changing_volume(kernel):
    from scripts.hydro_geometry import wing_geometry
    wing=wing_geometry(1,4,camber_scale=1,trim_deg=0)
    turned=wing_geometry(1,4,camber_scale=1,trim_deg=90)
    flatter=wing_geometry(1,4,camber_scale=.5,trim_deg=0)
    full=[kernel.moments(t,10) for t in [wing,turned,flatter]]
    assert full[0][0]==pytest.approx(full[1][0],rel=1e-12)
    assert full[0][0]==pytest.approx(full[2][0],rel=1e-12)
    assert not np.allclose(full[0][1:],full[1][1:])
    assert not np.allclose(full[0][1:],full[2][1:])

def test_saved_hydrostatics_report_is_current_and_preserves_balance():
    from scripts.publish_hydrostatics import report
    from scripts.native_design_kernel import ROOT
    r,text=report()
    assert r['qualified'] is False
    assert (ROOT/'docs/hydrostatics.md').read_text(encoding='utf-8')==text
    assert {c['density_kg_m3'] for c in r['cases']}=={1000,1025}
    for c in r['cases']:
        assert [p['heel_deg'] for p in c['points']]==list(np.linspace(-180,180,49))
        assert max(abs(p['mass_residual_kg']) for p in c['points'])<1e-5
        assert max(abs(p['pitch_torque_Nm']) for p in c['points'])<1e-5
        signed=[p['righting_Nm']*np.sign(p['heel_deg']) for p in c['points'] if 0<abs(p['heel_deg'])<180]
        assert min(signed)==pytest.approx(c['minimum_sampled_restoring_Nm'])


def test_native_actuator_accounting_keeps_idle_and_movement_losses():
    if sys.platform=='linux':pytest.skip('Pinned OpenSysML executable runs on Windows')
    import json
    from scripts.render_requirements import native,MODELS,ROOT
    result=json.loads(native('-analysis','BlueDogWingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/structure.sysml',ROOT/'models/wing-actuator.sysml')))
    assert result['status']=='holds' and not result.get('diagnostics')
    values={v['name']:json.loads(v['value']) for v in result['checks'][0]['values']}
    assert values['lockedWhPerDay']==pytest.approx(24*(.1+.02*(1+1*.2/(.8*.4))))
    assert values['poweredHoldWhPerDay']-values['lockedWhPerDay']==pytest.approx(24*.98*2)
    assert values['locked'][1]==pytest.approx(1.725)

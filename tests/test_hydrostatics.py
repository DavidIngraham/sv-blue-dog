"""Independent convex-hull oracle and analytic buoyancy/torque checks."""
import itertools,sys
import numpy as np
import pytest
from scipy.spatial import ConvexHull
from tools.boat_analysis.geometry.hydro import convex_tetrahedra, DisplacementBody, pose
from tools.boat_analysis.model.hydrostatic_mesh import equilibrium

@pytest.fixture(scope='module')
def kernel():
    if sys.platform!='linux':pytest.skip('Native compiled kernel requires Linux/GCC')
    from tools.boat_analysis.model.hydrostatic_mesh import MeshHydrostatics
    return MeshHydrostatics()


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
    from tools.boat_analysis.model.hydrostatic_mesh import free_pitch_equilibrium
    cube=convex_tetrahedra(list(itertools.product([-.5,.5],repeat=3)))
    body=[DisplacementBody('cube',cube)]
    result=free_pitch_equilibrium(kernel,body,[.01,0,-.2],500,0)
    assert abs(result['pitch_torque_Nm'])<1e-6
    assert result['pitch_stable']
    assert abs(result['pitch_deg'])>0.01
    inverted=free_pitch_equilibrium(kernel,body,[0,0,-.2],500,180)
    assert not inverted['pitch_stable']


def test_geometry_changes_with_wing_camber_and_trim_without_changing_volume(kernel):
    from tools.boat_analysis.geometry.hydro import wing_geometry
    wing=wing_geometry(1,4,camber_scale=1,trim_deg=0)
    turned=wing_geometry(1,4,camber_scale=1,trim_deg=90)
    flatter=wing_geometry(1,4,camber_scale=.5,trim_deg=0)
    full=[kernel.moments(t,10) for t in [wing,turned,flatter]]
    assert full[0][0]==pytest.approx(full[1][0],rel=1e-12)
    assert full[0][0]==pytest.approx(full[2][0],rel=1e-12)
    assert not np.allclose(full[0][1:],full[1][1:])
    assert not np.allclose(full[0][1:],full[2][1:])


def test_native_actuator_accounting_keeps_idle_and_movement_losses():
    import json
    from tests.native_cases import native,MODELS,ROOT
    result=json.loads(native('-analysis','BlueDogWingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/actuation.sysml')))
    assert result['status']=='holds' and not result.get('diagnostics')
    values={v['name']:json.loads(v['value']) for v in result['checks'][0]['values']}
    assert values['lockedWhPerDay']==pytest.approx(24*(.1+.02*(1+1*.2/(.8*.4))))
    assert values['poweredHoldWhPerDay']-values['lockedWhPerDay']==pytest.approx(24*.98*2)
    assert values['locked'][1]==pytest.approx(1.725)


def test_mesh_batch_matches_independent_sum_and_checks_inputs(kernel):
    rng = np.random.default_rng(71)
    tetrahedra = rng.normal(size=(9, 4, 3))
    expected = sum((oracle(points, .2) for points in tetrahedra), np.zeros(4))
    np.testing.assert_allclose(kernel.moments(tetrahedra, .2), expected, atol=1e-10)
    with pytest.raises(ValueError, match='Nonempty tetrahedra'):
        kernel.moments(np.empty((0, 4, 3)), 0)
    with pytest.raises(ValueError, match='finite'):
        kernel.moments(tetrahedra, np.nan)
    with pytest.raises(ValueError, match='positiveMassAndDensity'):
        kernel.balance([1, 0, 0, 0], [0, 0, 0], 0, 1000)

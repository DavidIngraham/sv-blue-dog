"""Independent geometry oracles and native material-accounting checks."""
import itertools,json,sys
import numpy as np
import pytest
from scripts.coupled_geometry import metrics,section_properties,build_geometry,ROOT
from scripts.hydro_geometry import convex_tetrahedra


def test_box_metrics_are_independent_of_tetrahedral_internal_faces():
    points=np.array(list(itertools.product([-1,1],[-2,2],[-3,3])),dtype=float)
    result=metrics(convex_tetrahedra(points))
    np.testing.assert_allclose(result,[88,0,0,0,48,0,0,0],atol=1e-12)
    shifted=metrics(convex_tetrahedra(points)+[2,3,4])
    np.testing.assert_allclose(shifted,[88,2,3,4,48,2,3,4],atol=1e-12)


def test_square_skin_section_matches_closed_form_and_rotation():
    square=np.array([[-1,-1],[1,-1],[1,1],[-1,1]],dtype=float)
    expected=[16/3,16/(3*np.sqrt(2)),4,8]
    np.testing.assert_allclose(section_properties(square),expected,rtol=1e-12)
    a=.4;rotation=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
    np.testing.assert_allclose(section_properties(square@rotation+[10,-2]),expected,rtol=1e-12)


def reference():
    r=json.loads((ROOT/'docs/analysis/coupled-mass-reference.json').read_text())
    return {'designNames':list(r['design']),'referenceDesign':list(r['design'].values())},r['design']


def test_shape_scaling_and_degenerate_foil_tip_cells():
    _,d=reference();g,v=build_geometry(d)
    assert all(np.isfinite(a).all() for a in v.values())
    d['wing_thickness_scale']*=1.2;g2,v2=build_geometry(d)
    assert v2['wing'][4]==pytest.approx(v['wing'][4]*1.2,rel=1e-10)
    for name in ['hull','keel','rudder']:np.testing.assert_array_equal(v2[name],v[name])
    for name in g:
        scaled=metrics(g[name]*2)
        assert scaled[0]==pytest.approx(v[name][0]*4)
        assert scaled[4]==pytest.approx(v[name][4]*8)
        np.testing.assert_allclose(scaled[1:4],v[name][1:4]*2,atol=1e-10)


@pytest.mark.skipif(sys.platform!='linux',reason='Native C adapter uses Linux/GCC')
def test_native_mass_derivatives_and_centroid_bookkeeping():
    from scripts.native_coupled import MassKernel
    k=MassKernel();c,d=reference();_,v=build_geometry(d);geometry=np.r_[np.concatenate(list(v.values())),json.loads((ROOT/'docs/analysis/coupled-mass-reference.json').read_text())['ballastCentroid']];x=np.array(c['referenceDesign'])
    base=k.evaluate(x,geometry);p=np.array(k.contract['parameterValues'])
    saved=json.loads((ROOT/'docs/analysis/coupled-mass-reference.json').read_text())
    for name,value in base.items():assert value==pytest.approx(saved['mass'][name],rel=1e-11,abs=1e-12)
    x[c['designNames'].index('ballast_kg')]+=1
    ballast=k.evaluate(x,geometry)
    assert ballast['totalMass']-base['totalMass']==pytest.approx(1)
    assert ballast['cgZ']*ballast['totalMass']-base['cgZ']*base['totalMass']==pytest.approx(geometry[-1])
    x=np.array(c['referenceDesign']);x[c['designNames'].index('wing_glass_kg_m2')]+=.1
    glass=k.evaluate(x,geometry)
    assert glass['totalMass']-base['totalMass']==pytest.approx(v['wing'][0]*.1*(1+p[0]))
    x=np.array(c['referenceDesign']);x[c['designNames'].index('battery_Wh')]+=p[12]
    battery=k.evaluate(x,geometry)
    assert battery['totalMass']-base['totalMass']==pytest.approx(1)
    assert battery['cgZ']*battery['totalMass']-base['cgZ']*base['totalMass']==pytest.approx(-d['bottom_depth_m']+(d['bottom_depth_m']+d['deck_height_m'])*d['battery_z_fraction'])
    assert base['totalMass']==pytest.approx(sum(base[k] for k in ['hullMass','wingMass','keelMass','rudderMass','batteryMass','panelMass','wingDriveMass','rudderDriveMass','equipmentMass'])+d['ballast_kg'])


def test_polar_nodes_provenance_and_no_extrapolation():
    from scripts.wing_polar import WingPolar
    polar=WingPolar();data=json.loads(polar.path.read_text())
    for row in data['cases']:
        if row['camberScale']==0:continue
        for i,a in enumerate(row['values']['Alpha']):
            sign=np.array([-1,1,-1]) if row['reverseChord'] else np.ones(3)
            np.testing.assert_allclose(polar.evaluate(row['aspect'],row['camberScale'],-a if row['reverseChord'] else a,reverse_flow=row['reverseChord']),np.array([row['values'][k][i] for k in ['CLtot','CDi','CMytot']])*sign,atol=1e-12)
    for point in [(1,1,0),(4,2,0),(4,1,17),(4,np.nan,0)]:
        with pytest.raises(ValueError):polar.evaluate(*point)
    zero=next(r for r in data['cases'] if r['camberScale']==0)
    i=zero['values']['Alpha'].index(0)
    assert abs(zero['values']['CLtot'][i])<1e-4
    assert abs(zero['values']['CMytot'][i])<1e-4


def test_mass_reference_provenance():
    from scripts.study_open_sizing import validate
    r=json.loads((ROOT/'docs/analysis/coupled-mass-reference.json').read_text())
    validate(r['sourceHashes'])
    assert not r['qualified']

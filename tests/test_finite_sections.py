"""Independent analytical checks of finite laminate section geometry."""
import numpy as np
import pytest
from tools.boat_analysis.geometry.laminate import finite_skin_properties
from tools.boat_analysis.geometry.vessel import section_properties,build_geometry


@pytest.mark.parametrize('thickness',[.01,.2,.8,2.])
def test_rectangular_skin_matches_exact_closed_form(thickness):
    b,h=4.,2.;t=thickness
    p=np.array([[-b/2,-h/2],[b/2,-h/2],[b/2,h/2],[-b/2,h/2]])
    bi,hi=max(0,b-2*t),max(0,h-2*t)
    ix=(b*h**3-bi*hi**3)/12;iy=(h*b**3-hi*bi**3)/12
    z=1/np.hypot((h/2)/ix,(b/2)/iy)
    np.testing.assert_allclose(finite_skin_properties(p,t),[min(ix,iy),z],rtol=1e-11)
    a=.63;rotation=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
    np.testing.assert_allclose(finite_skin_properties(p@rotation+[12,-7],t),[min(ix,iy),z],rtol=1e-10)


def test_circular_annulus_matches_closed_form():
    theta=np.linspace(0,2*np.pi,1440,endpoint=False)
    p=np.c_[np.cos(theta),np.sin(theta)]
    expected=np.pi*(1-.7**4)/4
    np.testing.assert_allclose(finite_skin_properties(p,.3),[expected,expected],rtol=2e-5)


def test_concavity_is_not_filled_by_a_convex_envelope():
    p=np.array([[0,0],[4,0],[4,1],[1,1],[1,3],[4,3],[4,4],[0,4]],dtype=float)
    # 4x4 square less the 3x2 rectangle cut from its right side.
    cx=(16*2-6*2.5)/10
    ix=4*4**3/12-3*2**3/12
    iy=4*4**3/3-2*(4**3-1)/3-10*cx**2
    assert finite_skin_properties(p,100)[0]==pytest.approx(min(ix,iy),rel=1e-12)
    assert finite_skin_properties(p,.2)[0]<min(ix,iy)


def test_thin_limit_and_solid_saturation():
    p=np.array([[-2,-1],[2,-1],[2,1],[-2,1]],dtype=float)
    thin=section_properties(p)[:2]
    np.testing.assert_allclose(finite_skin_properties(p,1e-5)/1e-5,thin,rtol=3e-5)
    values=[finite_skin_properties(p,t)[0] for t in [.001,.1,.5,1.,2.,10.]]
    assert np.all(np.diff(values)>=-1e-12)
    assert values[-1]==pytest.approx(4*2**3/12)
    assert values[-3:]==pytest.approx([values[-1]]*3)


def test_actual_cad_and_foil_sections_cannot_exceed_their_solid_inertia():
    import json
    from tools.boat_analysis.model.runtime import ROOT
    d=__import__('tools.boat_analysis.evidence.records',fromlist=['baseline_record']).baseline_record('coupled-mass-reference.json')['design']
    _,_,outlines=build_geometry(d)
    for p in outlines.values():
        size=float(np.ptp(p,axis=0).max());solid=finite_skin_properties(p,size)[0]
        for fraction in [.0001,.005,.02,.05,.2]:
            assert 0<finite_skin_properties(p,size*fraction)[0]<=solid*(1+1e-10)


@pytest.mark.parametrize('thickness',[0,-1,float('nan')])
def test_invalid_thickness_is_rejected(thickness):
    with pytest.raises(ValueError):finite_skin_properties([[0,0],[1,0],[0,1]],thickness)

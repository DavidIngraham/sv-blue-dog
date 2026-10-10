"""Independent regression arithmetic, similarity scaling and coverage checks."""
import json
import sys
import numpy as np
import pytest
from scripts.native_design_kernel import ROOT
from scripts.study_open_sizing import validate


def evidence():
    r=json.loads((ROOT/'docs/analysis/hull-resistance-audit.json').read_text(encoding='utf-8'))
    validate(r['sourceHashes'])
    return r


def test_published_equation_and_coefficient_row():
    r=evidence();h=r['hull'];L,B,T,V,Aw,LCB,LCF,Cp,Cm=h
    # Keuning/Katgert 2008 table 2, Fn .40; independent dimensional substitution.
    expected=(-.0064+V**(1/3)/L*(-.4034*LCB/L-.1250*Cp+.0273*V**(2/3)/Aw-.1341*B/L+.3578*LCB/LCF+.0045*B/T+.1115*Cm))
    assert r['cases'][1]['outputs']['resistance_weight_ratio']==pytest.approx(expected,abs=1e-14)
    assert r['cases'][1]['outputs']['resistance_N']==pytest.approx(expected*r['density']*r['gravity']*V)
    assert r['cases'][-1]['outputs']['froude_upper']<0
    assert not r['qualified']


@pytest.fixture
def kernel():
    if sys.platform!='linux':pytest.skip('Native adapter requires Linux/GCC')
    from scripts.native_hull_resistance import HullResistanceKernel
    return HullResistanceKernel()


def test_native_interpreter_parity(kernel):
    r=evidence()
    for c in r['cases']:
        result=kernel.evaluate(r['hull'],c['speed_m_s'],require_domain=False)
        for k,v in c['outputs'].items():assert result[k]==pytest.approx(v,abs=1e-12)


def test_froude_interpolation_and_geometric_similarity(kernel):
    r=evidence();h=np.array(r['hull']);g=r['gravity'];v=lambda fn:fn*(g*h[0])**.5
    f=lambda fn:kernel.evaluate(h,v(fn))['resistance_N']
    assert f(.425)==pytest.approx((f(.4)+f(.45))/2,rel=1e-12)
    scale=np.array([2,2,2,8,4,2,2,1,1])
    enlarged=kernel.evaluate(h*scale,v(.4)*2**.5)
    assert enlarged['resistance_N']==pytest.approx(8*f(.4))
    assert kernel.evaluate(h,v(.4),density=1025)['resistance_N']==pytest.approx(1.025*f(.4))


def test_domain_extrapolation_is_rejected(kernel):
    r=evidence();h=np.array(r['hull']);v=r['cases'][1]['speed_m_s']
    with pytest.raises(ValueError,match='froude_upper'):kernel.evaluate(h,r['cases'][-1]['speed_m_s'])
    broad=h.copy();broad[1]=1.7
    with pytest.raises(ValueError,match='beam_length_upper'):kernel.evaluate(broad,v)
    high_cp=h.copy();high_cp[7]=.67
    with pytest.raises(ValueError,match='cp_upper'):kernel.evaluate(high_cp,v)
    with pytest.raises(ValueError,match='Positive finite'):kernel.evaluate(h,0)
    with pytest.raises(ValueError,match='Positive finite'):kernel.evaluate(h[:-1],v)


def test_upright_hull_features_for_rectangular_prism():
    from itertools import product
    from scripts.hydro_geometry import convex_tetrahedra
    from scripts.hull_features import upright_hull_features
    box=convex_tetrahedra(np.array(list(product([-2.,2.],[-1.,1.],[-1.,1.]))))
    h=upright_hull_features(box,0.)
    np.testing.assert_allclose(h,[4,2,1,8,8,2,2,1,1],atol=1e-10)
    shifted=upright_hull_features(box+[7,3,5],5.)
    np.testing.assert_allclose(shifted,h,atol=1e-10)
    with pytest.raises(ValueError,match='Waterline'):upright_hull_features(box,2.)


def test_geometry_audit_preserves_out_of_domain_findings():
    r=json.loads((ROOT/'docs/analysis/hull-resistance-domain.json').read_text(encoding='utf-8'))
    validate(r['sourceHashes'])
    assert not r['qualified']
    assert r['cases'][0]['outsideEnvelope']==['cp_upper']
    assert set(r['cases'][1]['outsideEnvelope'])=={'cp_upper','beam_length_upper','volume_length_upper','cm_upper'}
    for c in r['cases']:assert c['nativeCanoeVolume_m3']==pytest.approx(c['hullFeatures'][3],rel=1e-9)


def test_resistance_publication_is_current():
    from scripts.publish_hull_resistance import publication
    assert (ROOT/'docs/hull-resistance.md').read_text(encoding='utf-8')==publication()

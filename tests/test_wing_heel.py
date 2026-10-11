"""Physical frame invariants for heel sweeps; independent of the VSP runtime."""
import numpy as np
import pytest
from tools.boat_analysis.aerodynamics.vsp.heel_sweep import inflow, orientation


@pytest.mark.parametrize('awa',[0,45,90,135])
def test_upright_incidence_recovers_original_sweep(awa):
    for alpha in [-12,0,16]:
        assert np.allclose(inflow(0,awa,alpha),(alpha,0),atol=1e-12)


def test_beam_wind_heel_is_spanwise_flow_not_a_cosine_rescale():
    for heel in [-40,-20,20,40]:
        assert np.allclose(inflow(heel,90,8),(8,-heel),atol=1e-12)
        assert np.allclose(inflow(heel,0,8),(8,0),atol=1e-12)


def test_rotation_preserves_wind_and_force_norms():
    for heel in [-40,0,40]:
        for awa in [45,90,135]:
            r=orientation(heel,awa,8)
            assert np.allclose(r.T@r,np.eye(3))
            assert np.isclose(np.linalg.det(r),1)
            a,b=np.radians(inflow(heel,awa,8))
            local=np.array([np.cos(a)*np.cos(b),-np.sin(b),np.sin(a)*np.cos(b)])
            assert np.allclose(r@local,[np.cos(np.radians(awa)),-np.sin(np.radians(awa)),0])


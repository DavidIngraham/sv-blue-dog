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


def test_archived_heel_run_has_complete_cases_and_reproducible_source():
    import hashlib
    import subprocess
    from tools.boat_analysis.evidence.heel import load
    from tools.boat_analysis.model.runtime import ROOT
    data=load()
    assert len(data['cases'])==15
    assert {(r['awa_deg'],r['heel_deg']) for r in data['cases']}=={(a,h) for a in [45,90,135] for h in [-40,-20,0,20,40]}
    for path,expected in data['sourceHashes'].items():
        content=subprocess.check_output(['git','show',f"{data['sourceRevision']}:{path}"],cwd=ROOT)
        assert hashlib.sha256(content.replace(b'\r\n',b'\n')).hexdigest()==expected
    zero=[r for r in data['cases'] if r['heel_deg']==0]
    for row in zero[1:]:
        for key in zero[0]['raw']:
            assert np.allclose(row['raw'][key],zero[0]['raw'][key],atol=1e-8)
    for row in data['cases']:
        assert len(row['points'])==8
        for key,values in row['raw'].items():
            assert len(values)==8 and np.isfinite(values).all()
        for i,p in enumerate(row['points']):
            a,b=inflow(row['heel_deg'],row['awa_deg'],p['nominalAlpha_deg'])
            assert np.isclose(row['raw']['Alpha'][i],a)
            assert np.isclose(row['raw']['Beta'][i],b)
            # Drag is the component of the inviscid world force along the wind.
            c=data['settings'];qs=.5*c['airDensity']*c['speedMps']**2*c['areaM2']
            awa=np.radians(row['awa_deg'])
            drag=-p['drive_N']*np.cos(awa)-p['starboard_N']*np.sin(awa)
            assert np.isclose(drag,qs*row['raw']['CDi'][i],atol=1e-8)

"""Joint sizing: boundary policy and independent native execution."""
import json
from copy import deepcopy
import numpy as np
import pytest
from scripts.study_open_sizing import boundary_hits, expanded_bounds, read_report, publication_outputs, ROOT


def test_search_brackets_expand_without_relaxing_physical_limits():
    c={'expandableLower':[True,False], 'expandableUpper':[True,False]}
    lo,hi=expanded_bounds(c,[1.,0.],[4.,15.],[{'index':0,'side':'lower'},{'index':0,'side':'upper'},{'index':1,'side':'upper'}])
    assert lo.tolist()==[.5,0.]
    assert hi.tolist()==[8.,15.]


def test_boundary_detection_includes_near_limits():
    hits=boundary_hits({'design':{'length':1.001,'ballast':14.999}},[1,0],[4,15],['length','ballast'])
    assert [(h['name'],h['side']) for h in hits]==[('length','lower'),('ballast','upper')]


def test_saved_search_has_fifteen_live_sizing_dimensions():
    r=read_report(); c=r['contract']
    assert len(c['designNames'])==15
    assert all(a<b for a,b in zip(c['lower'],c['upper']))
    assert {'freeboard_m','rudder_arm_fraction'} <= set(c['designNames'])
    for study in r['studies'].values():
        assert all(a<b for round_ in study['rounds'] for a,b in zip(round_['lower'],round_['upper']))
        assert study['best']['operatingFeasible']
        assert all(row['wing_height_unconstrained']==1 for row in study['best']['results'])


def test_native_replay_and_published_artifacts():
    for path, content in publication_outputs().items():
        assert path.read_text(encoding='utf-8')==content


@pytest.mark.skipif(__import__('sys').platform!='linux',reason='Compiled C adapter requires GCC/Linux')
def test_compiled_adapter_retains_rows_and_sizing_dependencies():
    from scripts.study_open_sizing import SizingKernel
    k=SizingKernel(); b=read_report()['studies']['nominal_5ms']['best'];c=k.contract
    d=np.array([b['design'][n] for n in c['designNames']]);s=np.r_[5,1,1,b['states'][0]]
    original=k.evaluate(d,s); saved=original.copy()
    changed=d.copy();changed[13]+=.1
    higher=k.evaluate(changed,s)
    np.testing.assert_array_equal(original,saved)
    assert higher[c['outputNames'].index('totalMass')]>original[c['outputNames'].index('totalMass')]
    changed=d.copy();changed[14]*=.8
    moved=k.evaluate(changed,s)
    assert moved[c['outputNames'].index('low_speed_yaw')]<original[c['outputNames'].index('low_speed_yaw')]
    with pytest.raises(ValueError):k.evaluate(d[:-1],s)


@pytest.mark.skipif(__import__('sys').platform!='linux',reason='Compiled C adapter requires GCC/Linux')
def test_adapter_rejects_boxed_native_sequence():
    from types import SimpleNamespace
    from scripts.study_open_sizing import SizingKernel
    # Exercise the guard without dereferencing a mismatched native pointer.
    k=object.__new__(SizingKernel)
    k.contract={'parameterNames':['p'],'outputNames':['x']}
    k.parameters=np.array([1.])
    k.lock=__import__('threading').Lock()
    def boxed(*args):
        output=args[-1]._obj
        output.shape=3
        output.length=1
        return 0
    k.lib=SimpleNamespace(sysml_run=boxed)
    with pytest.raises(ValueError,match='representation'):
        k.evaluate(np.ones(15),np.ones(9))


def test_saved_verdicts_follow_equilibrium_and_margin_outputs():
    r=read_report();c=r['contract']
    for study in r['studies'].values():
        b=study['best']
        rows=np.array([[row[n] for n in c['outputNames']] for row in b['results']])
        balanced=np.abs(rows[:,:4]).max()<=c['equilibrium_tolerance']
        operating=balanced and rows[:,5:29].min()>=-c['margin_tolerance']
        fit=operating and rows[:,4].min()>=-c['margin_tolerance']
        assert b['operatingFeasible']==bool(operating)
        assert b['numericalFeasible']==bool(fit)
        bounds=study['rounds'][-1]
        x=np.array([b['design'][n] for n in c['designNames']])
        assert np.all(x>=np.array(bounds['lower'])-1e-8)
        assert np.all(x<=np.array(bounds['upper'])+1e-8)

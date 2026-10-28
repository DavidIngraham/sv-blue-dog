"""Search layout and named numeric inputs follow native-export contracts."""
from dataclasses import fields
from types import SimpleNamespace

import numpy as np
import pytest

from tools.boat_analysis.generated import Design, OperatingState
from tools.boat_analysis.optimization import search


def fake_model():
    design_names=[field.name for field in fields(Design)]
    state_names=[field.name for field in fields(OperatingState)][3:]
    contract=dict(maximumOverallLengthM=2., progressSearchReserve=.005,
        challengeRequiresEastProgress=False, allSeasonRequiresEastProgress=True,
        windSpeeds=[3.,5.], designLower=[.1]*len(design_names),
        designUpper=[10.]*len(design_names), stateLower=[.1]*len(state_names),
        stateUpper=[80.]*len(state_names), leewardHeading=[90.,150.],
        coarseTrims=[0.], coarseHeels=[-20.,20.])
    # The parameter order intentionally differs from the current model. Values
    # are attached to exported names rather than their old vector positions.
    values=dict(gravity=10.,ballastDensity=8000.,waterDensity=1000.,panelCoverage=.8)
    mass=dict(totalMass=10.,cgX=0.,cgY=0.,cgZ=0.)
    return SimpleNamespace(c=dict(designNames=design_names,parameterNames=list(values)),
        parameters=np.array(list(values.values())), operating_contract=contract,
        polar=SimpleNamespace(axes=tuple(np.array([1.,2.]) for _ in range(3))),
        hydro=object(),configuration=lambda *args,**kwargs:([],mass,[],[]))


def test_reordered_native_parameters_retain_density_and_gravity(monkeypatch):
    model=fake_model()
    monkeypatch.setattr(search,'CoupledModel',lambda:model)
    densities=[]
    def equilibrium(*args,**kwargs):
        densities.append(kwargs['density'])
        return dict(righting_Nm=2.)
    monkeypatch.setattr(search,'equilibrium',equilibrium)
    problem=search.Problem()
    result=problem.design_data(np.ones(problem.design_count))
    assert densities == [1000.,1000.,1000.]
    np.testing.assert_array_equal(result[3],[-.2,.2])


@pytest.mark.parametrize('bound',['designLower','designUpper','stateLower','stateUpper'])
def test_search_rejects_bounds_without_a_native_field(monkeypatch,bound):
    model=fake_model()
    model.operating_contract[bound]=model.operating_contract[bound][:-1]
    monkeypatch.setattr(search,'CoupledModel',lambda:model)
    with pytest.raises(ValueError,match='bounds must match'):
        search.Problem()


def test_search_rejects_duplicate_native_parameter_names(monkeypatch):
    model=fake_model()
    model.c['parameterNames'][0]=model.c['parameterNames'][1]
    monkeypatch.setattr(search,'CoupledModel',lambda:model)
    with pytest.raises(ValueError,match='parameter names must be unique'):
        search.Problem()


def test_search_cannot_infer_an_empty_operating_coverage(monkeypatch):
    model=fake_model()
    model.operating_contract['windSpeeds']=[]
    monkeypatch.setattr(search,'CoupledModel',lambda:model)
    with pytest.raises(ValueError,match='at least one model wind speed'):
        search.Problem()

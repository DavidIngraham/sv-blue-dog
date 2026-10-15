"""Typed inputs must preserve the native numerical ABI exactly."""
import json
from dataclasses import fields, replace
import numpy as np
import pytest
from tools.boat_analysis.generated import Design, Parameters
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.vessel import CoupledModel


def test_records_preserve_model_vectors_and_reject_drift():
    c=json.loads((ROOT/'.tools/coupled-contract.json').read_text())
    for cls,names,values in [(Design,c['designNames'],c['referenceDesign']),
                             (Parameters,c['parameterNames'],c['parameterValues'])]:
        record=cls.from_array(values)
        np.testing.assert_array_equal(record.as_array(),values)
        assert [f.name for f in fields(record)]==names
        with pytest.raises(ValueError):cls.from_array(values[:-1])
        with pytest.raises(ValueError):cls.from_array([values])
        with pytest.raises(ValueError,match='finite'):cls.from_array([float('nan'),*values[1:]])
    design=Design.from_array(c['referenceDesign'])
    assert replace(design,length_m=1.2).length_m==1.2
    assert design.length_m!=1.2


def test_configuration_accepts_record_without_numerical_change():
    model=CoupledModel()
    x=model.c['referenceDesign']
    record=model.design_record(x)
    _,old_mass,old_geometry,_=model.configuration(x,0,resolution=4)
    _,new_mass,new_geometry,_=model.configuration(record,0,resolution=4)
    assert new_mass==old_mass
    np.testing.assert_array_equal(new_geometry,old_geometry)
    np.testing.assert_array_equal(model.assumptions.as_array(),model.parameters)


def test_mass_kernel_accepts_both_typed_inputs():
    model=CoupledModel()
    x=model.c['referenceDesign']
    _,mass,geometry,_=model.configuration(x,0,resolution=4)
    assert model.mass(design=model.design_record(x),geometry=geometry[:51],parameters=model.assumptions).to_mapping()==mass


def test_ballast_density_invalidates_geometry_cache():
    model=CoupledModel();design=model.design_record(model.c['referenceDesign'])
    state=[5,1,1,2,50,4,1,-2,0]
    model.at_state(design,state,pitch_equilibrium=False)
    original=model.candidate(design)
    density_index=list(model.assumptions).index('ballastDensity')
    model.parameters[density_index]*=.8
    changed=model.candidate(design)
    assert changed is not original
    assert not np.array_equal(changed[1]['ballast'],original[1]['ballast'])
    assert model.candidate(design) is changed
    cached=model.at_state(design,state,pitch_equilibrium=False)
    model.hull_reference=None
    assert model.at_state(design,state,pitch_equilibrium=False)==cached

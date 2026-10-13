"""Typed inputs must preserve the native numerical ABI exactly."""
import json
from dataclasses import fields, replace
import numpy as np
import pytest
from tools.boat_analysis.model.design_boundary import pack, unpack
from tools.boat_analysis.model.design_types import Design, Parameters
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.vessel import CoupledModel


def test_records_preserve_model_vectors_and_reject_drift():
    c=json.loads((ROOT/'.tools/coupled-contract.json').read_text())
    for cls,names,values in [(Design,c['designNames'],c['referenceDesign']),
                             (Parameters,c['parameterNames'],c['parameterValues'])]:
        record=unpack(cls,values,names)
        np.testing.assert_array_equal(pack(record,names),values)
        assert len(fields(record))==len(names)
        with pytest.raises(ValueError):pack(record,names[:-1])
        with pytest.raises(ValueError):unpack(cls,values[:-1],names)
    design=unpack(Design,c['referenceDesign'],c['designNames'])
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
    np.testing.assert_array_equal(pack(model.assumptions,model.c['parameterNames']),model.parameters)


def test_mass_kernel_accepts_both_typed_inputs():
    model=CoupledModel()
    x=model.c['referenceDesign']
    _,mass,geometry,_=model.configuration(x,0,resolution=4)
    assert model.mass(design=model.design_record(x),geometry=geometry[:51],parameters=model.assumptions).to_mapping()==mass

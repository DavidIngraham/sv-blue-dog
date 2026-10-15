"""Named records must preserve physical results and reject semantically wrong inputs."""
from sysml_python.records import from_array, as_array
from dataclasses import replace
import sys
import numpy as np
import pytest
from tools.boat_analysis.generated import (
    Design, Parameters, OperatingState, AeroCoefficients, HydroState, MassProperties)

pytestmark=pytest.mark.skipif(sys.platform!='linux',reason='Native runtime requires GCC')

@pytest.fixture(scope='module')
def case():
    from tools.boat_analysis.generated import operation
    from tools.boat_analysis.evidence.records import input_record
    kernel=operation
    values=input_record('coupled-operation-audit.json')['inputs']
    raw=dict(zip(('design','parameters','environment','state','aero','mass','hydro'),values,strict=True))
    raw.pop('environment')
    types=dict(design=Design,parameters=Parameters,state=OperatingState,
               aero=AeroCoefficients,mass=MassProperties,hydro=HydroState)
    import json
    from tools.boat_analysis.model.runtime import ROOT
    context=json.loads((ROOT/'.tools/coupled-operation-contract.json').read_text())
    typed={n:from_array(t, raw[n]) for n,t in types.items()}
    return kernel,raw,typed,context


def test_named_calls_and_shuffled_mass_match_vectors(case):
    kernel,raw,typed,context=case
    expected=kernel(**raw)
    assert kernel(**typed)==expected
    shuffled=dict(reversed(list(typed['mass'].to_mapping().items())))
    assert kernel(**{**typed,'mass':shuffled})==expected
    # Deliberately different same-width record is not silently accepted.
    with pytest.raises(TypeError,match='incompatible SysML record'):
        from tools.boat_analysis.generated import AppendageLoads
        kernel(**{**typed,'aero':AppendageLoads(wingResultant=1,keelResultant=2,rudderResultant=3)})


def test_typed_batch_scalar_parity_and_empty(case):
    kernel,raw,typed,context=case
    states=[typed['state'],replace(typed['state'],speed_m_s=1.5)]
    shared={k:v for k,v in typed.items() if k!='state'}
    batch=kernel.batch(shared=shared,cases={'state':states},chunk_size=1)
    expected=[list(kernel(**shared,state=s).values()) for s in states]
    np.testing.assert_allclose(batch.values,expected,rtol=1e-14)
    assert kernel.batch(shared=shared,cases={'state':[]}).values.shape==(0,len(expected[0]))
    with pytest.raises(ValueError,match='finite'):
        replace(states[0],windSpeed_m_s=float('nan'))


def test_typed_surface_provider_matches_vector_provider(case):
    from tools.boat_analysis.model.surface import SurfaceOperation
    from tools.boat_analysis.aerodynamics.polar import WingPolar
    kernel,raw,typed,context=case
    provider=SurfaceOperation(context,WingPolar(),[10,.0002,.05,8])
    assert provider.evaluate(**typed)==provider.evaluate(**raw)


def test_record_orders_match_physics_contract(case):
    kernel,raw,typed,context=case
    from tools.boat_analysis.generated import MassResult
    from dataclasses import fields
    assert [f.name for f in fields(MassProperties)]==[f.name for f in fields(MassResult)]
    for name,record in typed.items():
        np.testing.assert_array_equal(as_array(record),raw[name])
    assert typed['state'].windSpeed_m_s==raw['state'][0]
    assert typed['hydro'].waterplaneArea_m2==raw['hydro'][7]


def test_empty_batch_keeps_shape_validation(case):
    kernel,raw,typed,context=case
    with pytest.raises(ValueError,match='expected batch rows'):
        kernel.batch(shared={k:v for k,v in typed.items() if k!='state'},
                              cases={'state':np.empty((0,99))})


def test_coupled_state_and_mass_record_api(case):
    from tools.boat_analysis.model.vessel import CoupledModel
    model=CoupledModel()
    _,_,typed,_=case
    design=model.design_record(model.c['referenceDesign'])
    state=replace(typed['state'],windSpeed_m_s=8.,windFrom_deg=50.,incidence_deg=4.)
    vector=as_array(state)
    assert model.at_state(design,state,pitch_equilibrium=False)==model.at_state(design,vector,pitch_equilibrium=False)
    _,mass,geometry,_=model.configuration(design,0.)
    assert model.mass(design=design,geometry=geometry[:51]).to_mapping()==mass

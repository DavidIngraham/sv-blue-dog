"""Generated schemas and physical preconditions remain authoritative across APIs."""
import copy
import sys
import numpy as np
import pytest
from tools.boat_analysis.model.contracts import describe


def test_schema_follows_model_names_order_and_dimensions(tmp_path):
    path=tmp_path/'boundary.sysml'
    def model(width, label):
        return f"package BoundaryExample {{ private import ScalarValues::*; calc def Evaluate {{ in x : Real [{width}] ordered nonunique; in scale : Real; attribute {label} : Real = x#(1)*scale; attribute other : Real = x#(2); return result : Real [2] ordered nonunique; ({label},other) }} }}"
    path.write_text(model(3,'initialValue'),encoding='utf-8')
    args, outputs=describe(path,'BoundaryExample::Evaluate')
    assert args==[{'name':'x','shape':[3]},{'name':'scale','shape':[]}]
    assert outputs==['initialValue','other']
    path.write_text(model(5,'renamed'),encoding='utf-8')
    args, outputs=describe(path,'BoundaryExample::Evaluate')
    assert args[0]['shape']==[5] and outputs==['renamed','other']


def test_unsupported_schema_fails_preparation(tmp_path):
    path=tmp_path/'unsupported.sysml'
    path.write_text('package Unsupported { private import ScalarValues::*; calc def Evaluate { in x : String; return result : Real [2] ordered nonunique; (1.0,2.0) } }',encoding='utf-8')
    with pytest.raises(ValueError,match='Unsupported numerical input'):
        describe(path,'Unsupported::Evaluate')


@pytest.fixture(scope='module')
def mass_case():
    if sys.platform!='linux':pytest.skip('Native runtime requires Linux/GCC')
    from tools.boat_analysis.model.mass import MassKernel
    from tools.boat_analysis.evidence.records import input_record
    kernel=MassKernel();record=input_record('coupled-mass-reference.json')
    geometry=np.r_[np.concatenate(list(record['geometry'].values())),record['ballastCentroid']]
    return kernel,np.array(kernel.contract['referenceDesign']),geometry,np.array(kernel.contract['parameterValues'])


def test_mass_scalar_batch_defaults_and_typed_records(mass_case):
    from tools.boat_analysis.model.design_boundary import unpack
    from tools.boat_analysis.model.design_types import Design, Parameters
    k,d,g,p=mass_case
    typed_d=unpack(Design,d,k.contract['designNames'])
    typed_p=unpack(Parameters,p,k.contract['parameterNames'])
    expected=k.evaluate(typed_d,g,typed_p)
    assert k.evaluate(d,g)==expected
    batch=k.evaluate_batch(shared={'design':typed_d,'parameters':typed_p},cases={'geometry':np.stack([g,g])})
    np.testing.assert_allclose(batch.values,[list(expected.values())]*2,rtol=1e-14)
    assert k.kernel.schema['outputs']==list(expected)


@pytest.mark.parametrize('field,index,value,label',[
    ('design',0,0,'positiveDimensions'),('design',15,-1,'nonnegativeBallast'),
    ('parameters',12,0,'positiveBatterySpecificEnergy'),('parameters',0,-.01,'nonnegativeResinRatio')])
def test_mass_preconditions_apply_to_scalar_and_batch(mass_case,field,index,value,label):
    k,d,g,p=mass_case
    values={'design':d.copy(),'parameters':p.copy(),'geometry':g.copy()}
    invalid=values[field].copy();invalid[index]=value
    with pytest.raises(ValueError,match=label):
        k.evaluate(**{**values,field:invalid})
    cases={field:np.stack([values[field],invalid,values[field]])}
    with pytest.raises(ValueError,match='case 1.*'+label):
        k.evaluate_batch(shared={n:v for n,v in values.items() if n!=field},cases=cases,chunk_size=1)
    # Rejected inputs never poison the next calculation.
    assert np.isfinite(list(k.evaluate(**values).values())).all()


def test_generated_widths_and_finite_checks_cover_both_apis(mass_case):
    k,d,g,p=mass_case
    for geometry in (g[:-1],np.r_[np.nan,g[1:]]):
        with pytest.raises(ValueError):k.evaluate(d,geometry,p)
        with pytest.raises(ValueError):
            k.evaluate_batch(shared={'design':d,'parameters':p},cases={'geometry':geometry[None,:]})
    with pytest.raises(ValueError,match='Unknown or duplicate'):
        k.evaluate_batch(shared={'design':d,'geometry':g,'surprise':1},cases={'parameters':p[None,:]})
    empty=k.evaluate_batch(shared={'design':d},cases={'geometry':np.empty((0,len(g)))})
    assert empty.values.shape==(0,len(k.contract['massNames']))


def test_stale_precondition_code_is_rejected(mass_case):
    from tools.boat_analysis.model.boundary import ModelBoundary
    k,*_=mass_case
    schema=copy.deepcopy(k.kernel.schema);schema['checks']['sourceHash']='incorrect'
    with pytest.raises(ValueError,match='Stale generated preconditions'):
        ModelBoundary(k.contract,schema)

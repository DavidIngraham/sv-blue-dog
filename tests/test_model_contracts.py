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
    from tools.boat_analysis.generated import mass
    from tools.boat_analysis.evidence.records import input_record
    from tools.boat_analysis.model.runtime import ROOT
    import json
    c=json.loads((ROOT/'.tools/coupled-contract.json').read_text())
    record=input_record('coupled-mass-reference.json')
    geometry=np.r_[np.concatenate(list(record['geometry'].values())),record['ballastCentroid']]
    return mass,np.array(c['referenceDesign']),geometry,np.array(c['parameterValues'])


def test_mass_scalar_batch_defaults_and_typed_records(mass_case):
    from tools.boat_analysis.model.design_boundary import unpack
    from tools.boat_analysis.generated import Design, Parameters
    k,d,g,p=mass_case
    from dataclasses import fields
    typed_d=unpack(Design,d,[f.name for f in fields(Design)])
    typed_p=unpack(Parameters,p,[f.name for f in fields(Parameters)])
    expected=k(design=typed_d,geometry=g,parameters=typed_p)
    assert k(design=d,geometry=g)==expected
    batch=k.batch(shared={'design':typed_d,'parameters':typed_p},cases={'geometry':np.stack([g,g])})
    np.testing.assert_allclose(batch.values,[list(expected.values())]*2,rtol=1e-14)
    assert list(expected)==[f.name for f in fields(type(expected))]


@pytest.mark.parametrize('field,index,value,label',[
    ('design',0,0,'positiveDimensions'),('design',15,-1,'nonnegativeBallast'),
    ('parameters',12,0,'positiveBatterySpecificEnergy'),('parameters',0,-.01,'nonnegativeResinRatio')])
def test_mass_preconditions_apply_to_scalar_and_batch(mass_case,field,index,value,label):
    k,d,g,p=mass_case
    values={'design':d.copy(),'parameters':p.copy(),'geometry':g.copy()}
    invalid=values[field].copy();invalid[index]=value
    with pytest.raises(ValueError,match=label):
        k(**{**values,field:invalid})
    cases={field:np.stack([values[field],invalid,values[field]])}
    with pytest.raises(ValueError,match='case 1.*'+label):
        k.batch(shared={n:v for n,v in values.items() if n!=field},cases=cases,chunk_size=1)
    # Rejected inputs never poison the next calculation.
    assert np.isfinite(list(k(**values).values())).all()


def test_generated_widths_and_finite_checks_cover_both_apis(mass_case):
    k,d,g,p=mass_case
    for geometry in (g[:-1],np.r_[np.nan,g[1:]]):
        with pytest.raises(ValueError):k(design=d,geometry=geometry,parameters=p)
        with pytest.raises(ValueError):
            k.batch(shared={'design':d,'parameters':p},cases={'geometry':geometry[None,:]})
    with pytest.raises(ValueError,match='exactly once'):
        k.batch(shared={'design':d,'geometry':g,'surprise':1},cases={'parameters':p[None,:]})
    empty=k.batch(shared={'design':d},cases={'geometry':np.empty((0,len(g)))})
    assert empty.values.shape==(0,len(k(design=d,geometry=g)))


def test_stale_precondition_code_is_rejected(mass_case,tmp_path):
    import json
    from tools.boat_analysis.generated import MassResult
    from tools.boat_analysis.model.runtime import ROOT
    from sysml_python.execution import Calculation
    directory=ROOT/'tools/boat_analysis/generated'
    contract=json.loads((directory/'manifest.json').read_text())
    for entry in (contract['exports']['mass'],contract['exports']['mass']['checks']):
        entry['source']=str(directory/entry['source'])
    contract['exports']['mass']['checks']['sourceHash']='incorrect'
    manifest=tmp_path/'manifest.json';manifest.write_text(json.dumps(contract))
    with pytest.raises(ValueError,match='Generated source differs'):
        Calculation(manifest,'mass',MassResult).load()

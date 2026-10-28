"""Build model contracts and interpreter evidence, separate from runtime adapters."""
from sysml_python.records import from_array
import json
import numpy as np
from .runtime import ROOT, analysis_values, load_model, numerical_value
from ..evidence.records import input_record, output_path, source_hashes
from ..generated import Design, Parameters, MassResult, OperationResult


def prepare_mass():
    c=analysis_values('BlueDog::Analyses::Sizing::Inputs')
    c['sourceHashes']=source_hashes([])
    (ROOT/'.tools/coupled-contract.json').write_text(json.dumps(c,indent=2)+'\n')
    from tools.boat_analysis.geometry.vessel import build_geometry,ballast_geometry
    d=from_array(Design, c['referenceDesign']);p=from_array(Parameters, c['parameterValues'])
    _,vectors,_=build_geometry(d.to_mapping())
    bulb,center=ballast_geometry(d.ballast_kg/p.ballastDensity,-d.bottom_depth_m-d.keel_span_m)
    geometry=np.r_[np.concatenate(list(vectors.values())),center]
    values=numerical_value(load_model().calc('BlueDog::Analyses::Sizing::MassProperties',
        arguments=[c['referenceDesign'], c['parameterValues'], c['materialValues'], geometry.tolist()]).value)
    sources=['models/blue-dog.sysml','models/blue-dog.sysml','tools/boat_analysis/geometry/vessel.py','packages/sysml-python/sysml_python/execution.py','build/analysis/wing-geometry.json']
    saved={'sourceHashes':source_hashes(sources),'design':dict(zip(c['designNames'],c['referenceDesign'])),'parameters':dict(zip(c['parameterNames'],c['parameterValues'])),'geometry':{name:v.tolist() for name,v in vectors.items()},'ballastCentroid':center.tolist(),'mass':MassResult.from_array(values).to_mapping(),'qualified':False,'scope':'Reference geometry/material accounting only. Not a new optimized or verified vessel. Thin skin plus printed ribs and provisional equipment allocations. Seams/finish mass included, their displacement omitted. A volume-normalized 3:1:1 ballast bulb touches the keel tip without geometric overlap; its junction remains a structural detail.'}
    output_path('coupled-mass-reference.json').write_text(json.dumps(saved,indent=2)+'\n')

def prepare_operating():
    inputs=analysis_values('BlueDog::Configurations::OperatingEnvironment::Inputs')
    c={'sourceHashes':source_hashes([]),'environment':inputs['parameterValues']}
    c.update(analysis_values('BlueDog::Analyses::Operating::Inputs'))
    c['structure']=c['structureValues']
    c['conceptPolicy']=next(iter(analysis_values('BlueDog::Analyses::Sizing::Credibility::Inputs').values()))
    c['conceptSensitivity']=analysis_values('BlueDog::Analyses::Sizing::Credibility::SensitivityInputs')
    (ROOT/'.tools/coupled-operation-contract.json').write_text(json.dumps(c,indent=2)+'\n')
    reference=input_record('coupled-mass-reference.json')
    inputs=[list(reference['design'].values()),list(reference['parameters'].values()),c['environment'],[5,1,1,2,0,0,0,0,0],[.6,.02,-.07],list(reference['mass'].values()),[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]]
    values=numerical_value(load_model().calc('BlueDog::Analyses::Operating::Evaluate', arguments=inputs).value)
    record={'sourceHashes':c['sourceHashes'],'inputs':inputs,'outputs':OperationResult.from_array(values).to_mapping(),'scope':'Synthetic arithmetic replay, not an equilibrium or mission case.'}
    output_path('coupled-operation-audit.json').write_text(json.dumps(record,indent=2)+'\n')

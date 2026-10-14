"""Build model contracts and interpreter evidence, separate from runtime adapters."""
import json
import numpy as np
from .runtime import ROOT, analysis_values, load_model, numerical_value
from ..evidence.records import input_record, output_path, source_hashes


def prepare_mass():
    c=analysis_values('BlueDogCoupledSizing::Inputs')
    c['sourceHashes']=source_hashes([])
    # This is project reference data, not a compiler or execution contract.
    generated=json.loads((ROOT/'tools/boat_analysis/generated/manifest.json').read_text())
    c['massNames']=[f['name'] for f in generated['exports']['mass']['outputs']]
    (ROOT/'.tools/coupled-contract.json').write_text(json.dumps(c,indent=2)+'\n')
    from tools.boat_analysis.geometry.vessel import build_geometry,ballast_geometry
    _,vectors,_=build_geometry(dict(zip(c['designNames'],c['referenceDesign'])))
    d=dict(zip(c['designNames'],c['referenceDesign']))
    bulb,center=ballast_geometry(d['ballast_kg']/c['parameterValues'][33],-d['bottom_depth_m']-d['keel_span_m'])
    geometry=np.r_[np.concatenate(list(vectors.values())),center]
    values=numerical_value(load_model().calc('BlueDogCoupledSizing::MassProperties',
        arguments=[c['referenceDesign'], c['parameterValues'], c['materialValues'], geometry.tolist()]).value)
    sources=['models/analyses/sizing/inputs.sysml','models/vehicle/structure.sysml','tools/boat_analysis/geometry/vessel.py','packages/sysml-python/sysml_python/execution.py','build/analysis/wing-geometry.json']
    saved={'sourceHashes':source_hashes(sources),'design':dict(zip(c['designNames'],c['referenceDesign'])),'parameters':dict(zip(c['parameterNames'],c['parameterValues'])),'geometry':{name:v.tolist() for name,v in vectors.items()},'ballastCentroid':center.tolist(),'mass':dict(zip(c['massNames'],values)),'qualified':False,'scope':'Reference geometry/material accounting only. Not a new optimized or verified vessel. Thin skin plus printed ribs and provisional equipment allocations. Seams/finish mass included, their displacement omitted. A volume-normalized 3:1:1 ballast bulb touches the keel tip without geometric overlap; its junction remains a structural detail.'}
    output_path('coupled-mass-reference.json').write_text(json.dumps(saved,indent=2)+'\n')

def prepare_operating():
    inputs=analysis_values('BlueDogOperatingEnvironment::Inputs')
    c={'sourceHashes':source_hashes([]),'environment':inputs['parameterValues']}
    c.update(analysis_values('BlueDogCoupledOperation::Inputs'))
    c['structure']=c['structureValues']
    c['conceptPolicy']=next(iter(analysis_values('BlueDogConceptCredibility::Inputs').values()))
    c['conceptSensitivity']=analysis_values('BlueDogConceptCredibility::SensitivityInputs')
    generated=json.loads((ROOT/'tools/boat_analysis/generated/manifest.json').read_text())
    c['outputNames']=[f['name'] for f in generated['exports']['operation']['outputs']]
    for field in generated['exports']['operation']['inputs']:
        if record := field.get('record'):
            c[record['sysml_id']+'Fields']=record['fields']
    c['structureNames']=[f['name'] for f in generated['exports']['structure']['outputs']]
    c['conceptNames']=[f['name'] for f in generated['exports']['concept']['outputs']]
    names=c['outputNames']
    (ROOT/'.tools/coupled-operation-contract.json').write_text(json.dumps(c,indent=2)+'\n')
    reference=input_record('coupled-mass-reference.json')
    inputs=[list(reference['design'].values()),list(reference['parameters'].values()),c['environment'],[5,1,1,2,0,0,0,0,0],[.6,.02,-.07],list(reference['mass'].values()),[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]]
    values=numerical_value(load_model().calc('BlueDogCoupledOperation::Evaluate', arguments=inputs).value)
    record={'sourceHashes':c['sourceHashes'],'inputs':inputs,'outputs':dict(zip(names,values)),'scope':'Synthetic arithmetic replay, not an equilibrium or mission case.'}
    output_path('coupled-operation-audit.json').write_text(json.dumps(record,indent=2)+'\n')

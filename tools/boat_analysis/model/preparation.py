"""Build model contracts and interpreter evidence, separate from runtime adapters."""
import json
import numpy as np
from .runtime import ROOT, native, native_value
from .contracts import compile_model
from ..evidence.records import input_record, output_path, source_hashes


def analysis_values(name):
    report = json.loads(native('-analysis', name, '-json'))
    if report['status'] != 'holds':
        raise ValueError('Model input export failed: '+name)
    return {v['name']:native_value(v['value']) for v in report['checks'][0]['values']}


def prepare_mass():
    from tools.boat_analysis.model.runtime import MODELS,native
    from tools.boat_analysis.model.runtime import native_value
    models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/sizing/inputs.sysml')
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
    replay=ROOT/'.tools/coupled-mass-replay.sysml'
    replay.write_text('package CoupledMassReplay { private import ScalarValues::*; analysis reference { out attribute mass : Real [*] ordered nonunique = BlueDogCoupledSizing::MassProperties(BlueDogCoupledSizing::Inputs.referenceDesign,BlueDogCoupledSizing::Inputs.parameterValues,BlueDogCoupledSizing::Inputs.materialValues,('+','.join(format(v,'.17g') for v in geometry)+')); } }')
    report=json.loads(native('-analysis','CoupledMassReplay::reference','-json',models=models+(replay,)))
    if report['status']!='holds':raise ValueError('Reference mass replay failed')
    values=native_value(report['checks'][0]['values'][0]['value'])
    sources=['models/analyses/sizing/inputs.sysml','models/vehicle/structure.sysml','tools/boat_analysis/geometry/vessel.py','packages/sysml-python/sysml_python/execution.py','build/analysis/wing-geometry.json']
    saved={'sourceHashes':source_hashes(sources),'design':dict(zip(c['designNames'],c['referenceDesign'])),'parameters':dict(zip(c['parameterNames'],c['parameterValues'])),'geometry':{name:v.tolist() for name,v in vectors.items()},'ballastCentroid':center.tolist(),'mass':dict(zip(c['massNames'],values)),'qualified':False,'scope':'Reference geometry/material accounting only. Not a new optimized or verified vessel. Thin skin plus printed ribs and provisional equipment allocations. Seams/finish mass included, their displacement omitted. A volume-normalized 3:1:1 ballast bulb touches the keel tip without geometric overlap; its junction remains a structural detail.'}
    output_path('coupled-mass-reference.json').write_text(json.dumps(saved,indent=2)+'\n')

def prepare_operating():
    from tools.boat_analysis.model.runtime import MODELS,native
    from tools.boat_analysis.model.runtime import native_value
    models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/actuation.sysml',ROOT/'models/analyses/sizing/operating.sysml',ROOT/'models/libraries/marine/hull-resistance.sysml')
    inputs=analysis_values('BlueDogOperatingEnvironment::Inputs')
    c={'sourceHashes':source_hashes([]),'environment':inputs['parameterValues']}
    c.update(analysis_values('BlueDogCoupledOperation::Inputs'))
    c['structure']=c['structureValues']
    c['conceptPolicy']=next(iter(analysis_values('BlueDogConceptCredibility::Inputs').values()))
    c['conceptSensitivity']=analysis_values('BlueDogConceptCredibility::SensitivityInputs')
    compile_model(c, 'operation', path='models/libraries/marine/sailing.sysml',
        definition='MarineSailing::Evaluate', output_definition='MarineSailing::Core',
        aliases={'d':'design','p':'parameters','q':'environment','s':'state','aero':'aero','massData':'mass','hydro':'hydro'},
        source='coupled-operation.c', hash_key='generatedHash', output_key='outputNames',
        defaults={'environment':'environment'}, checks='MarineSailing::InputChecks',
        record_types={n:'MarineDesign::'+t for n,t in dict(design='Design',parameters='Parameters',
            state='OperatingState',aero='AeroCoefficients',mass='MassProperties',hydro='HydroState').items()})
    generated=json.loads((ROOT/'tools/boat_analysis/generated/manifest.json').read_text())
    c['structureNames']=[f['name'] for f in generated['exports']['structure']['outputs']]
    c['conceptNames']=[f['name'] for f in generated['exports']['concept']['outputs']]
    compile_model(c, 'route', path='models/libraries/marine/course.sysml', definition='MarineCourse::Route',
        aliases={'water':'water','states':'states','policy':'policy'}, source='coupled-route.c', hash_key='routeHash',
        defaults={'policy':'routeParameters'})
    names=c['outputNames']
    (ROOT/'.tools/coupled-operation-contract.json').write_text(json.dumps(c,indent=2)+'\n')
    reference=input_record('coupled-mass-reference.json')
    inputs=[list(reference['design'].values()),list(reference['parameters'].values()),c['environment'],[5,1,1,2,0,0,0,0,0],[.6,.02,-.07],list(reference['mass'].values()),[0,0,1,2,.6,.15,.071973,.85,1.05,1.1,.55,.727]]
    literal=lambda values:'('+','.join(format(v,'.17g') for v in values)+')'
    replay=ROOT/'.tools/coupled-operation-replay.sysml'
    replay.write_text('package CoupledOperationReplay { private import ScalarValues::*; analysis example { out attribute result : Real [*] ordered nonunique = BlueDogCoupledOperation::Evaluate('+','.join(literal(a) for a in inputs)+'); } }')
    audit=json.loads(native('-analysis','CoupledOperationReplay::example','-json',models=models+(replay,)))
    if audit['status']!='holds':raise ValueError('Operating arithmetic replay failed')
    values=native_value(audit['checks'][0]['values'][0]['value'])
    record={'sourceHashes':c['sourceHashes'],'inputs':inputs,'outputs':dict(zip(names,values)),'scope':'Synthetic arithmetic replay, not an equilibrium or mission case.'}
    output_path('coupled-operation-audit.json').write_text(json.dumps(record,indent=2)+'\n')

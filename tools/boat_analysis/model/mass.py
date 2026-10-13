"""Native coupled geometry/material accounting; numerical geometry stays external."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
import numpy as np
from numpy.typing import ArrayLike
from .design_types import Design, Parameters
from .design_boundary import design_vector, parameter_vector
from tools.boat_analysis.model.runtime import ROOT
from .native_kernel import KernelSpec, NativeKernel
from tools.boat_analysis.evidence.records import digest,validate
CONTRACT=ROOT/'.tools/coupled-contract.json'

def prepare():
    from tools.boat_analysis.model.runtime import MODELS,native
    from tools.boat_analysis.model.runtime import native_value
    models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/sizing/inputs.sysml')
    audit=json.loads(native('-analysis','BlueDogCoupledSizing::Inputs','-json',models=models))
    if audit['status']!='holds':raise ValueError('Coupled inputs did not execute')
    c={v['name']:native_value(v['value']) for v in audit['checks'][0]['values']}
    c['sourceHashes']={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in models}
    source=ROOT/'.tools/coupled-mass.c'
    native('-compile','BlueDogCoupledSizing::MassProperties','-source','-o',str(source),models=models)
    c['massHash']=digest(source)
    c['massNames']=['totalMass','hullMass','wingMass','keelMass','rudderMass','batteryMass','panelMass','wingDriveMass','rudderDriveMass','equipmentMass','cgX','cgY','cgZ','hullMaterialVolume','wingMaterialVolume','keelMaterialVolume','rudderMaterialVolume','hullLaminateThickness','wingLaminateThickness','keelLaminateThickness','rudderLaminateThickness']
    CONTRACT.write_text(json.dumps(c,indent=2)+'\n')
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
    sources=['models/analyses/sizing/inputs.sysml','models/vehicle/structure.sysml','tools/boat_analysis/geometry/vessel.py','tools/boat_analysis/model/mass.py','build/analysis/wing-geometry.json']
    saved={'sourceHashes':source_hashes(sources),'design':dict(zip(c['designNames'],c['referenceDesign'])),'parameters':dict(zip(c['parameterNames'],c['parameterValues'])),'geometry':{name:v.tolist() for name,v in vectors.items()},'ballastCentroid':center.tolist(),'mass':dict(zip(c['massNames'],values)),'qualified':False,'scope':'Reference geometry/material accounting only. Not a new optimized or verified vessel. Thin skin plus printed ribs and provisional equipment allocations. Seams/finish mass included, their displacement omitted. A volume-normalized 3:1:1 ballast bulb touches the keel tip without geometric overlap; its junction remains a structural detail.'}
    output_path('coupled-mass-reference.json').write_text(json.dumps(saved,indent=2)+'\n')

class MassKernel:
    def __init__(self):
        self.contract=json.loads(CONTRACT.read_text(encoding='utf-8'));c=self.contract
        validate(c['sourceHashes'])
        source=ROOT/'.tools/coupled-mass.c'
        if digest(source)!=c['massHash']:raise ValueError('Stale MassKernel source')
        self.runtime=NativeKernel(KernelSpec(source,('design', 'parameters', 'materials', 'geometry'),len(c['massNames'])))

    def evaluate(self,design: Design | ArrayLike,geometry: ArrayLike,parameters: Parameters | ArrayLike | None=None):
        c=self.contract
        design=design_vector(design,c)
        p=c['parameterValues'] if parameters is None else parameter_vector(parameters,c)
        arrays=[np.ascontiguousarray(a,dtype=float) for a in [design,p,c['materialValues'],geometry]]
        if [a.shape for a in arrays]!=[(29,),(41,),(len(c['materialValues']),),(51,)] or any(not np.isfinite(a).all() for a in arrays):raise ValueError('Invalid mass inputs')
        d=arrays[0]
        positive=[0,1,2,3,4,5,7,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25]
        if np.any(d[positive]<=0) or d[15]<0 or arrays[1][12]<=0 or arrays[1][0]<0:raise ValueError('Invalid physical mass inputs')
        result=self.runtime.evaluate(*arrays)
        return dict(zip(c['massNames'],result))

if __name__=='__main__':prepare()

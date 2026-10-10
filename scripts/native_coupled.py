"""Native coupled geometry/material accounting; numerical geometry stays external."""
import ctypes as ct
import json,subprocess,threading
import numpy as np
from .native_design_kernel import ROOT,Sequence
from .study_open_sizing import digest,validate
CONTRACT=ROOT/'.tools/coupled-contract.json'
_LOCK=threading.Lock()

def prepare():
    from .render_requirements import MODELS,native
    from .prepare_design_search import native_value
    models=MODELS+(ROOT/'models/structure.sysml',ROOT/'models/coupled-sizing.sysml')
    audit=json.loads(native('-analysis','BlueDogCoupledSizing::Inputs','-json',models=models))
    if audit['status']!='holds':raise ValueError('Coupled inputs did not execute')
    c={v['name']:native_value(v['value']) for v in audit['checks'][0]['values']}
    c['sourceHashes']={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in models}
    source=ROOT/'.tools/coupled-mass.c'
    native('-compile','BlueDogCoupledSizing::MassProperties','-source','-o',str(source),models=models)
    c['massHash']=digest(source)
    c['massNames']=['totalMass','hullMass','wingMass','keelMass','rudderMass','batteryMass','panelMass','wingDriveMass','rudderDriveMass','equipmentMass','cgX','cgY','cgZ','hullMaterialVolume','wingMaterialVolume','keelMaterialVolume','rudderMaterialVolume','hullLaminateThickness','wingLaminateThickness','keelLaminateThickness','rudderLaminateThickness']
    CONTRACT.write_text(json.dumps(c,indent=2)+'\n')
    from .coupled_geometry import build_geometry,ballast_geometry
    _,vectors=build_geometry(dict(zip(c['designNames'],c['referenceDesign'])))
    d=dict(zip(c['designNames'],c['referenceDesign']))
    bulb,center=ballast_geometry(d['ballast_kg']/c['parameterValues'][33],-d['bottom_depth_m']-d['keel_span_m'])
    geometry=np.r_[np.concatenate(list(vectors.values())),center]
    replay=ROOT/'.tools/coupled-mass-replay.sysml'
    replay.write_text('package CoupledMassReplay { private import ScalarValues::*; analysis reference { out attribute mass : Real [*] ordered nonunique = BlueDogCoupledSizing::MassProperties(BlueDogCoupledSizing::Inputs.referenceDesign,BlueDogCoupledSizing::Inputs.parameterValues,BlueDogCoupledSizing::Inputs.materialValues,('+','.join(format(v,'.17g') for v in geometry)+')); } }')
    report=json.loads(native('-analysis','CoupledMassReplay::reference','-json',models=models+(replay,)))
    if report['status']!='holds':raise ValueError('Reference mass replay failed')
    values=native_value(report['checks'][0]['values'][0]['value'])
    sources=['models/coupled-sizing.sysml','models/structure.sysml','scripts/coupled_geometry.py','scripts/native_coupled.py','docs/analysis/wing-geometry.json']
    saved={'sourceHashes':{name:digest(ROOT/name) for name in sources},'design':dict(zip(c['designNames'],c['referenceDesign'])),'parameters':dict(zip(c['parameterNames'],c['parameterValues'])),'geometry':{name:v.tolist() for name,v in vectors.items()},'ballastCentroid':center.tolist(),'mass':dict(zip(c['massNames'],values)),'qualified':False,'scope':'Reference geometry/material accounting only. Not a new optimized or verified vessel. Thin skin plus printed ribs and provisional equipment allocations. Seams/finish mass included, their displacement omitted. A volume-normalized 3:1:1 ballast bulb touches the keel tip without geometric overlap; its junction remains a structural detail.'}
    (ROOT/'docs/analysis/coupled-mass-reference.json').write_text(json.dumps(saved,indent=2)+'\n')

class MassKernel:
    def __init__(self):
        self.contract=json.loads(CONTRACT.read_text());validate(self.contract['sourceHashes'])
        source=ROOT/'.tools/coupled-mass.c';h=self.contract['massHash']
        if digest(source)!=h:raise ValueError('Stale mass kernel')
        library=ROOT/f'.tools/coupled-mass-{h[:16]}.so'
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library));self.lib.sysml_run.argtypes=[Sequence]*4+[ct.POINTER(Sequence)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p
    def evaluate(self,design,geometry,parameters=None):
        c=self.contract
        p=c['parameterValues'] if parameters is None else parameters
        arrays=[np.ascontiguousarray(a,dtype=float) for a in [design,p,c['materialValues'],geometry]]
        if [a.shape for a in arrays]!=[(28,),(38,),(len(c['materialValues']),),(51,)] or any(not np.isfinite(a).all() for a in arrays):raise ValueError('Invalid mass inputs')
        d=arrays[0]
        positive=[0,1,2,3,4,5,7,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25]
        if np.any(d[positive]<=0) or d[15]<0 or arrays[1][12]<=0 or arrays[1][0]<0:raise ValueError('Invalid physical mass inputs')
        args=[Sequence(2,a.size,a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with _LOCK:
            output=Sequence()
            if self.lib.sysml_run(*args,ct.byref(output)):raise ValueError(self.lib.sysml_error().decode())
            if output.shape!=2 or output.length!=len(c['massNames']):raise ValueError('Mass ABI mismatch')
            result=np.ctypeslib.as_array(output.data,shape=(output.length,)).copy()
        if not np.isfinite(result).all():raise ValueError('Nonfinite mass result')
        return dict(zip(c['massNames'],result))

if __name__=='__main__':prepare()

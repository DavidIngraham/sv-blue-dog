"""Native Delft bare-hull regression adapter with explicit applicability screening."""
import ctypes as ct
import json
import re
import subprocess
import threading
import numpy as np
from .native_design_kernel import ROOT, Sequence
from .study_open_sizing import digest, validate
CONTRACT=ROOT/'.tools/hull-resistance-contract.json'
_LOCK=threading.Lock()
NAMES=['resistance_N','resistance_weight_ratio','froude']+[f'{name}_{side}' for name in ['froude','lcb','cp','volume_area','beam_length','center_ratio','volume_length','cm','beam_draft'] for side in ['lower','upper']]


def prepare():
    from .render_requirements import native
    from .prepare_design_search import native_value
    model=ROOT/'models/hull-resistance.sysml'
    source=ROOT/'.tools/hull-resistance.c'
    native('-compile','BlueDogHullResistance::Evaluate','-source','-o',str(source),models=(model,))
    signature=re.search(r'int sysml_run\((.*?)\) \{',source.read_text(encoding='utf-8'),re.S)
    if not signature or not signature[1].endswith('sysml_seq_real *result'):
        raise ValueError('Unexpected hull resistance output ABI')
    fixture=ROOT/'.tools/hull-resistance-replay.sysml'
    h=[2,.6,.15,.071973,.85,1.05,1.1,.55,.727]
    speeds=[fn*(9.80665*2)**.5 for fn in [.15,.4,.425,.6,.65]]
    text='package HullResistanceReplay { private import ScalarValues::*; analysis example {\n'
    for i,v in enumerate(speeds):
        text+=f'out attribute case{i} : Real [*] ordered nonunique = BlueDogHullResistance::Evaluate(('+','.join(format(x,'.17g') for x in h)+f'),{v:.17g},1000.0,9.80665);\n'
    fixture.write_text(text+'} }',encoding='utf-8')
    audit=json.loads(native('-analysis','HullResistanceReplay::example','-json',models=(model,fixture)))
    if audit['status']!='holds':raise ValueError('Hull resistance arithmetic replay failed')
    rows=[native_value(v['value']) for v in audit['checks'][0]['values']]
    hashes={'models/hull-resistance.sysml':digest(model),'scripts/native_hull_resistance.py':digest(ROOT/'scripts/native_hull_resistance.py')}
    CONTRACT.write_text(json.dumps({'sourceHashes':hashes,'generatedHash':digest(source)},indent=2)+'\n',encoding='utf-8')
    record={'sourceHashes':hashes,'scope':'Synthetic arithmetic fixtures, not measured resistance validation. Fn 0.65 deliberately exceeds the implementation coverage limit. Not yet connected to coupled search.','hull':h,'density':1000,'gravity':9.80665,'cases':[{'speed_m_s':v,'outputs':dict(zip(NAMES,r))} for v,r in zip(speeds,rows)],'qualified':False}
    (ROOT/'docs/analysis/hull-resistance-audit.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


class HullResistanceKernel:
    def __init__(self):
        c=json.loads(CONTRACT.read_text(encoding='utf-8'));validate(c['sourceHashes'])
        source=ROOT/'.tools/hull-resistance.c'
        if digest(source)!=c['generatedHash']:raise ValueError('Stale resistance kernel')
        library=ROOT/f".tools/hull-resistance-{c['generatedHash'][:16]}.so"
        if not library.exists():subprocess.run(['gcc','-O2','-shared','-fPIC',str(source),'-lm','-o',str(library)],check=True)
        self.lib=ct.CDLL(str(library))
        self.lib.sysml_run.argtypes=[Sequence,ct.c_double,ct.c_double,ct.c_double,ct.POINTER(Sequence)]
        self.lib.sysml_run.restype=ct.c_int;self.lib.sysml_error.restype=ct.c_char_p

    def evaluate(self,hull,speed,density=1000.,gravity=9.80665,*,require_domain=True):
        h=np.ascontiguousarray(hull,dtype=float)
        if h.shape!=(9,) or not np.isfinite(h).all() or np.any(h<=0) or not np.isfinite([speed,density,gravity]).all() or min(speed,density,gravity)<=0:
            raise ValueError('Positive finite hull dimensions, speed, density and gravity required')
        with _LOCK:
            out=Sequence();arg=Sequence(2,h.size,h.ctypes.data_as(ct.POINTER(ct.c_double)))
            if self.lib.sysml_run(arg,speed,density,gravity,ct.byref(out)):raise ValueError(self.lib.sysml_error().decode())
            if out.shape!=2 or out.length!=len(NAMES):raise ValueError('Resistance ABI mismatch')
            values=np.ctypeslib.as_array(out.data,shape=(out.length,)).copy()
        if not np.isfinite(values).all():raise ValueError('Nonfinite resistance result')
        result=dict(zip(NAMES,values))
        if require_domain:
            failures=[k for k,v in result.items() if k in NAMES[3:] and v < -1e-12]
            if failures:raise ValueError('Outside Delft screening envelope: '+', '.join(failures))
            if result['resistance_N']<0:raise ValueError('Negative residuary regression result; no silent clamp')
        return result


if __name__=='__main__':prepare()

"""Parameterized, inviscid CAD-wing response grid; separated-flow validity is not claimed."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import argparse,hashlib,json
from pathlib import Path
import numpy as np
from tools.boat_analysis.aerodynamics.vsp.reference_vsp import build
from tools.boat_analysis.aerodynamics.vsp.vsp_runtime import ROOT


def run_case(aspect,camber,mesh=24,reverse=False,*,wake_iterations=5,alpha_start=-12,alpha_end=16,alpha_count=8,beta=0):
    v,wing,_,span,chord,cad_hash=build(1.,aspect,mesh)
    work=ROOT/'.tools/wing-grid'/f'ar{aspect:g}-camber{camber:g}-reverse{int(reverse)}-m{mesh}-w{wake_iterations}-b{beta:g}';work.mkdir(parents=True,exist_ok=True)
    p=next(p for p in input_record('wing-geometry.json')['profiles'] if p['span_station_mm']==150)
    x=np.array(p['x_mm']);u=(x-x[0])/(x[-1]-x[0]);top=-np.array(p['lower_mm']);bottom=-np.array(p['upper_mm'])
    mean=(top+bottom)/2;half=(top-bottom)/2
    mean=(mean-np.linspace(mean[0],mean[-1],len(mean)))*camber
    top=(mean+half)/p['chord_mm'];bottom=(mean-half)/p['chord_mm']
    if reverse:top=top[::-1];bottom=bottom[::-1]
    foil=work/'section.dat';foil.write_text('BlueDog CAD midsection; inviscid response study\n'+''.join(f'{a:.10f} {b:.10f}\n' for a,b in list(zip(u[::-1],top[::-1]))+list(zip(u[1:],bottom[1:]))))
    surf=v.GetXSecSurf(wing,0)
    for i in [0,1]:v.ReadFileAirfoil(v.GetXSec(surf,i),str(foil))
    v.Update();path=work/'wing.vsp3';v.SetVSP3FileName(str(path));v.WriteVSPFile(str(path),v.SET_ALL)
    for name in ['VSPAEROComputeGeometry','VSPAEROSweep']:
        v.SetAnalysisInputDefaults(name)
        for key,value in [('GeomSet',v.SET_NONE),('ThinGeomSet',v.SET_ALL),('Symmetry',0)]:v.SetIntAnalysisInput(name,key,[value])
    v.ExecAnalysis('VSPAEROComputeGeometry');name='VSPAEROSweep'
    for key,value in [('AlphaStart',alpha_start),('AlphaEnd',alpha_end),('BetaStart',beta),('BetaEnd',beta),('Sref',1),('bref',span),('cref',chord),('Vinf',5),('Rho',1.225),('ReCref',5*chord/1.5e-5),('MachStart',0),('MachEnd',0),('Xcg',chord/2)]:v.SetDoubleAnalysisInput(name,key,[value])
    for key,value in [('AlphaNpts',alpha_count),('BetaNpts',1),('NCPU',2),('WakeNumIter',wake_iterations),('RefFlag',0)]:v.SetIntAnalysisInput(name,key,[value])
    result=v.ExecAnalysis(name);manager=v.ErrorMgrSingleton.getInstance();errors=[]
    while manager.GetNumTotalErrors():errors.append(manager.PopLastError().m_ErrorString)
    rid=v.FindLatestResultsID('VSPAERO_Polar')
    if not result or not rid or errors:raise ValueError((result,rid,errors))
    values={key:list(v.GetDoubleResults(rid,key)) for key in ['Alpha','CLtot','CDi','CMytot']}
    if any(len(values[k])!=alpha_count or not np.isfinite(values[k]).all() for k in values):raise ValueError('Invalid response grid')
    return {'aspect':aspect,'camberScale':camber,'reverseChord':reverse,'mesh':mesh,'wakeIterations':wake_iterations,'beta_deg':beta,'tool':v.GetVSPVersion(),'cadSha256':cad_hash,'values':values}


def run():
    path=output_path('wing-polar-grid.json')
    drivers=['tools/boat_analysis/aerodynamics/vsp/polar_grid.py','tools/boat_analysis/aerodynamics/vsp/reference_vsp.py','tools/boat_analysis/aerodynamics/vsp/vsp_runtime.py']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in drivers}
    rows=[]
    tasks=[(ar,camber,reverse) for ar in [2.,4.,6.,8.] for camber in [.5,1.,1.5] for reverse in [False,True]]+[(4.,0.,False)]
    checkpoint=ROOT/'.tools/wing-grid-checkpoint.json'
    if checkpoint.exists():
        old=json.loads(checkpoint.read_text())
        if old.get('driverHashes')==hashes:rows=old['cases']
    for ar,camber,reverse in tasks:
        if any(r['aspect']==ar and r['camberScale']==camber and r['reverseChord']==reverse for r in rows):continue
        rows.append(run_case(ar,camber,reverse=reverse))
        checkpoint.write_text(json.dumps({'driverHashes':hashes,'cases':rows},indent=2)+'\n')
        print(f'Completed AR={ar}, camber={camber}, reverse={reverse}',flush=True)
    report={'driverHashes':hashes,'cases':rows,'validated':False,'physicalScope':'Inviscid VLM response surface, rounded-edge wake attachment assumed. No measured low-Re drag, stall, broadside flow or gust validity. Grid bounds are interpolation limits, not requirements. Camber is scaled while thickness stays fixed. Reverse-chord case tests geometric interchange only; it does not validate both-tack sailing.'}
    path.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':run()

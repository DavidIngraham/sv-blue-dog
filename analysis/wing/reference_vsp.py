"""CAD-section reference wing: first VSPAERO integration, not a validated polar."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from vsp_runtime import ROOT,load_vsp

def build(area,aspect,mesh):
    v=load_vsp();v.ClearVSPModel()
    data=json.loads((ROOT/'docs/analysis/wing-geometry.json').read_text())
    p=next(p for p in data['profiles'] if p['span_station_mm']==150)
    if p['incomplete_samples']:raise ValueError('Incomplete reference section')
    x=np.array(p['x_mm']);c=p['chord_mm'];xx=(x-x[0])/(x[-1]-x[0])
    # Reflect CAD Z so the concave surface is the lower surface in aero axes.
    upper=-np.array(p['lower_mm']);lower=-np.array(p['upper_mm'])
    datum=(upper[0]+lower[0])/2
    tilt=(upper[-1]+lower[-1])/2-datum
    upper=(upper-datum-tilt*xx)/c;lower=(lower-datum-tilt*xx)/c
    work=ROOT/'.tools/wing-vsp';work.mkdir(exist_ok=True)
    foil=work/'cad-midsection.dat'
    points=list(zip(xx[::-1],upper[::-1]))+list(zip(xx[1:],lower[1:]))
    foil.write_text('BlueDog STEP midsection reflected Z; unvalidated rounded-edge Kutta model\n'+''.join(f'{a:.9f} {b:.9f}\n' for a,b in points))
    wing=v.AddGeom('WING','');v.SetGeomName(wing,'CADSectionReferenceWing')
    v.SetParmVal(wing,'Sym_Planar_Flag','Sym',0)
    v.SetDriverGroup(wing,1,v.SPAN_WSECT_DRIVER,v.ROOTC_WSECT_DRIVER,v.TIPC_WSECT_DRIVER)
    span=math.sqrt(area*aspect);chord=area/span
    for name,value in [('Span',span),('Root_Chord',chord),('Tip_Chord',chord),('Sweep',0),('SectTess_U',mesh)]:
        v.SetParmVal(wing,name,'XSec_1',value)
    v.SetParmVal(wing,'Tess_W','Shape',2*mesh+1)
    surf=v.GetXSecSurf(wing,0)
    for i in [0,1]:
        v.ChangeXSecShape(surf,i,v.XS_FILE_AIRFOIL)
        v.ReadFileAirfoil(v.GetXSec(surf,i),str(foil))
    v.Update()
    path=work/f'reference-{mesh}.vsp3';v.SetVSP3FileName(str(path));v.WriteVSPFile(str(path),v.SET_ALL)
    return v,wing,work,span,chord,data['sha256']

def run(area,aspect,mesh):
    v,wing,work,span,chord,source=build(area,aspect,mesh)
    for name in ['VSPAEROComputeGeometry','VSPAEROSweep']:
        v.SetAnalysisInputDefaults(name)
        for key,value in [('GeomSet',v.SET_NONE),('ThinGeomSet',v.SET_ALL),('Symmetry',0)]:v.SetIntAnalysisInput(name,key,[value])
    geom=v.ExecAnalysis('VSPAEROComputeGeometry')
    name='VSPAEROSweep'
    for key,value in [('AlphaStart',-4),('AlphaEnd',12),('Sref',area),('bref',span),('cref',chord),('Vinf',5),('Rho',1.225),('ReCref',5*chord/1.5e-5),('MachStart',0),('MachEnd',0),('Xcg',chord/2)]:
        v.SetDoubleAnalysisInput(name,key,[value])
    for key,value in [('AlphaNpts',5),('NCPU',2),('WakeNumIter',5),('RefFlag',0)]:v.SetIntAnalysisInput(name,key,[value])
    result=v.ExecAnalysis(name)
    errors=[];manager=v.ErrorMgrSingleton.getInstance()
    while manager.GetNumTotalErrors():errors.append(manager.PopLastError().m_ErrorString)
    rid=v.FindLatestResultsID('VSPAERO_Polar')
    if not result or not rid or errors:raise ValueError((result,rid,errors))
    values={}
    for key in v.GetAllDataNames(rid):
        if v.GetResultsType(rid,key)==v.DOUBLE_DATA:values[key]=list(v.GetDoubleResults(rid,key))
    report={'tool':v.GetVSPVersion(),'cadSha256':source,'driverSha256':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),'area_m2':area,'aspectRatio':aspect,'span_m':span,'chord_m':chord,'mesh':mesh,'validated':False,
            'scope':'Rectangular free-air reference wing using CAD midsection, not a CAD planform replica. Inviscid VLM with assumed trailing-edge shedding on a rounded edge. No viscous/stall/broadside validity established. Not optimizer input.', 'results':values}
    (ROOT/f'docs/analysis/wing-vsp-reference-{mesh}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--area',type=float,default=1);parser.add_argument('--aspect',type=float,default=4);parser.add_argument('--mesh',type=int,default=16)
    args=parser.parse_args();run(args.area,args.aspect,args.mesh)


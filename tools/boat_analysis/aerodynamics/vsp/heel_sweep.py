"""VSPAERO heel/incidence sweeps with fixed horizontal apparent wind.

Wing axes are chord +X, span +Y, section normal +Z. World axes are aft,
starboard, up. The origin is root midchord. No physical geometry rotation is
needed: rotate wind into wing axes and forces/moments back into world axes.
"""
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from tools.boat_analysis.aerodynamics.vsp.reference_vsp import build
from tools.boat_analysis.model.runtime import ROOT, analysis_values
from tools.boat_analysis.evidence.records import digest


def rotation(axis, degrees):
    c,s=np.cos(np.radians(degrees)),np.sin(np.radians(degrees))
    return np.array([[1,0,0],[0,c,-s],[0,s,c]]) if axis=='x' else np.array([[c,-s,0],[s,c,0],[0,0,1]])


def orientation(heel, awa, nominal_alpha):
    return rotation('x',heel) @ rotation('z',nominal_alpha-awa) @ rotation('x',90)


def inflow(heel, awa, nominal_alpha):
    r=orientation(heel,awa,nominal_alpha)
    wind=np.array([np.cos(np.radians(awa)),-np.sin(np.radians(awa)),0.])
    local=r.T @ wind
    return np.degrees(np.arctan2(local[2],local[0])),np.degrees(np.arcsin(-local[1]))


def settings():
    return analysis_values('BlueDog::Analyses::WingHeel::sweepInputs')


def run():
    config=settings()
    source_paths=[Path(__file__).relative_to(ROOT).as_posix(),'tools/boat_analysis/aerodynamics/vsp/reference_vsp.py','tools/boat_analysis/aerodynamics/vsp/vsp_runtime.py','models/blue-dog.sysml']
    hashes={name:digest(ROOT/name) for name in source_paths}
    work=ROOT/'.tools/wing-heel';work.mkdir(exist_ok=True)
    checkpoint=work/'checkpoint.json'
    rows=[]
    if checkpoint.exists():
        old=json.loads(checkpoint.read_text())
        if old['sourceHashes']==hashes and old['settings']==config:rows=old['cases']
    for awa in config['apparentWindDegrees']:
        for heel in config['heelDegrees']:
            if any(c['awa_deg']==awa and c['heel_deg']==heel for c in rows):continue
            v,wing,_,span,chord,cad_hash=build(config['areaM2'],config['aspectRatio'],config['mesh'])
            case_dir=work/f'awa{awa:g}-heel{heel:g}';case_dir.mkdir(exist_ok=True)
            v.SetVSP3FileName(str(case_dir/'wing.vsp3'));v.WriteVSPFile(str(case_dir/'wing.vsp3'),v.SET_ALL)
            for name in ['VSPAEROComputeGeometry','VSPAEROSweep']:
                v.SetAnalysisInputDefaults(name)
                for key,value in [('GeomSet',v.SET_NONE),('ThinGeomSet',v.SET_ALL),('Symmetry',0)]:v.SetIntAnalysisInput(name,key,[value])
            v.ExecAnalysis('VSPAEROComputeGeometry')
            angles=[inflow(heel,awa,a) for a in config['nominalAlphaDegrees']]
            if not np.allclose(np.array(angles)[:,1],angles[0][1]):raise ValueError('Beta is not constant through trim sweep')
            name='VSPAEROSweep'
            values={'AlphaStart':angles[0][0],'AlphaEnd':angles[-1][0],'BetaStart':angles[0][1],'BetaEnd':angles[0][1],
                'Sref':config['areaM2'],'bref':span,'cref':chord,'Vinf':config['speedMps'],'Rho':config['airDensity'],
                'ReCref':config['speedMps']*chord/config['kinematicViscosity'],'MachStart':0,'MachEnd':0,'Xcg':chord/2,'Ycg':0,'Zcg':0}
            for key,value in values.items():v.SetDoubleAnalysisInput(name,key,[float(value)])
            for key,value in [('AlphaNpts',len(angles)),('BetaNpts',1),('MachNpts',1),('NCPU',2),('WakeNumIter',config['wakeIterations']),('RefFlag',0)]:v.SetIntAnalysisInput(name,key,[int(value)])
            result=v.ExecAnalysis(name)
            manager=v.ErrorMgrSingleton.getInstance();errors=[]
            while manager.GetNumTotalErrors():errors.append(manager.PopLastError().m_ErrorString)
            rid=v.FindLatestResultsID('VSPAERO_Polar')
            if not result or not rid or errors:raise ValueError((result,rid,errors))
            raw={key:list(v.GetDoubleResults(rid,key)) for key in ['Alpha','Beta','CLi','CDi','CFix','CFiy','CFiz','CMix','CMiy','CMiz']}
            if any(len(a)!=len(angles) or not np.isfinite(a).all() for a in raw.values()):raise ValueError('Incomplete heel run')
            if not np.allclose(raw['Alpha'],np.array(angles)[:,0],atol=1e-8) or not np.allclose(raw['Beta'],np.array(angles)[:,1],atol=1e-8):raise ValueError('Solver incidence mismatch')
            qS=.5*config['airDensity']*config['speedMps']**2*config['areaM2']
            points=[]
            for i,a in enumerate(config['nominalAlphaDegrees']):
                r=orientation(heel,awa,a)
                force=r @ (qS*np.array([raw[k][i] for k in ['CFix','CFiy','CFiz']]))
                moment=r @ (qS*np.array([span,chord,span])*np.array([raw[k][i] for k in ['CMix','CMiy','CMiz']]))
                points.append({'nominalAlpha_deg':a,'drive_N':-force[0],'starboard_N':force[1],'up_N':force[2],'heelMoment_Nm':moment[0]})
            rows.append({'awa_deg':awa,'heel_deg':heel,'raw':raw,'points':points,'tool':v.GetVSPVersion(),'cadSha256':cad_hash})
            checkpoint.write_text(json.dumps({'sourceHashes':hashes,'settings':config,'cases':rows},indent=2)+'\n',encoding='utf-8')
            print(f'Completed AWA {awa}, heel {heel}',flush=True)
    report={'sourceRevision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'sourceHashes':hashes,'settings':config,'validated':False,
        'scope':'Fixed-camber AR4 free-air inviscid heel sensitivity; fixed mast trim per nominal incidence, horizontal wind, no water/hull/stall/dynamic-roll effects. Moments about root midchord. Not optimizer input.',
        'forceConvention':'World X aft, Y starboard, Z up; positive heel right-hand about aft X. Drive = -Fx. Inviscid surface-integration forces only. CMx and CMz scale with span; CMy scales with chord.',
        'cases':rows}
    out=ROOT/'build/analysis/wing-heel-sweep.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(out)

if __name__=='__main__':run()

"""Sealed, freely flooded and retained-water static recovery sensitivities."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
import numpy as np
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.geometry.hydro import DisplacementBody,free_pitch_equilibrium
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest,validate


def run():
    saved=input_record('coupled-sizing-search.json')
    model=CoupledModel();x=[saved['design'][n] for n in model.c['designNames']];cases=[]
    sources=['build/analysis/coupled-sizing-search.json','tools/boat_analysis/optimization/recovery.py','tools/boat_analysis/model/vessel.py','tools/boat_analysis/geometry/vessel.py','models/analyses/sizing/inputs.sysml','models/analyses/recovery.sysml']
    hashes=source_hashes(sources)
    for density in model.operating_contract['recoveryDensities']:
        for trim in model.operating_contract['recoveryTrims']:
            original,m,g,_=model.configuration(x,np.deg2rad(trim),resolution=16)
            dry_mass=m['totalMass'];dry_cg=np.array([m['cgX'],m['cgY'],m['cgZ']])
            wing_volume=g[16];material_volume=m['wingMaterialVolume'];void=wing_volume-material_volume
            if not 0<material_volume<wing_volume:raise ValueError('Invalid wing void volume')
            for state in ['sealed','free_flooding_homogenized','full_water_retention']:
                bodies=original;mass=dry_mass;cg=dry_cg.copy();water_mass=0.
                if state=='free_flooding_homogenized':
                    bodies=[DisplacementBody(b.name,b.tetrahedra,material_volume/wing_volume if b.name=='wing' else 1.) for b in original]
                if state=='full_water_retention':
                    water_mass=density*void;mass+=water_mass;cg=(dry_cg*dry_mass+g[17:20]*water_mass)/mass
                points=[]
                for heel in np.linspace(*model.operating_contract['recoveryHeels'][:2],int(model.operating_contract['recoveryHeels'][2])):
                    try:points.append(free_pitch_equilibrium(model.hydro,bodies,cg,mass,heel,density=density))
                    except ValueError as e:points.append({'heel_deg':float(heel),'failure':str(e)})
                failures=sum('failure' in p for p in points)
                restoring=[p['righting_Nm']*np.sign(p['heel_deg']) for p in points if 'failure' not in p and 0<abs(p['heel_deg'])<180]
                cases.append({'density_kg_m3':density,'mast_trim_deg':trim,'wing_state':state,'mass_kg':mass,'cg_m':cg.tolist(),'retained_water_kg':water_mass,'minimumInteriorRestoring_Nm':min(restoring) if restoring else None,'failedEquilibria':failures,'sampledInteriorRestores':bool(not failures and min(restoring)>0),'points':points})
                print('RECOVERY',density,trim,state,cases[-1]['minimumInteriorRestoring_Nm'],failures,flush=True)
    validate(hashes)
    report={'sourceHashes':hashes,'design':saved['design'],'qualified':False,'cases':cases,'scope':'Static sensitivity only. Freely flooded material buoyancy is homogenized over the outer envelope; it is not an explicit shell/rib flood mesh. Full retention fills the entire estimated void and locates retained water at the volume centroid; no ingress, drainage or slosh dynamics are predicted. Four locked mast positions, freshwater and seawater, fixed roll with heave/pitch equilibrium. No dynamic release or global 3D equilibrium proof.'}
    output_path('coupled-recovery.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':run()

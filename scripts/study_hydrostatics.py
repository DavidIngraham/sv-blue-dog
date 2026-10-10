"""Full-angle diagnostic on the saved sizing baseline; not a new optimized design."""
import argparse,json
import numpy as np
from .native_hydrostatics import HydroKernel
from .hydro_geometry import DisplacementBody,hull_geometry,wing_geometry,ellipsoid,equilibrium,free_pitch_equilibrium
from .native_design_kernel import ROOT
from .study_open_sizing import digest


def geometry(design,row,trim,resolution=8,wing_buoyant_fraction=1.):
    d=design
    hull=hull_geometry(d['lwl_m'],d['beam_m'],row['draft'],d['freeboard_m'],resolution)
    wing=wing_geometry(d['sail_m2'],d['sail_AR'],mast_x=d['sail_x_fraction']*d['lwl_m'],base_z=d['freeboard_m'],trim_deg=trim,resolution=40)
    # Ballast aspect 3:1:1 is an explicit preliminary geometric choice.
    radius=(3*d['ballast_kg']/7800/(4*np.pi*3))**(1/3)
    ballast=ellipsoid([3*radius,radius,radius],center=[0,0,-row['draft']-d['keel_span_m']],resolution=resolution)
    return [DisplacementBody('hull',hull),DisplacementBody('wing',wing,wing_buoyant_fraction),DisplacementBody('ballast',ballast)]


def run(resolution):
    saved=json.loads((ROOT/'docs/analysis/mission-sizing.json').read_text());best=saved['studies']['printed_ribs']['rounded'];d=best['design'];row=best['results'][0]
    kernel=HydroKernel();cases=[]
    # Longitudinal first moment not present in prior search: place all other
    # equipment at x=0 and account for wing and rudder positions explicitly.
    cg=[(row['wingStructuralMass']*d['sail_x_fraction']*d['lwl_m']-row['rudderStructuralMass']*d['rudder_arm_fraction']*d['lwl_m'])/row['totalMass'],0,row['centerOfGravity']]
    for density in [1000.,1025.]:
        for trim in [0.,45.,90.]:
            for name,fraction in [('sealed',1.),('lost_wing_buoyancy',0.)]:
                bodies=geometry(d,row,trim,resolution,fraction)
                points=[free_pitch_equilibrium(kernel,bodies,cg,row['totalMass'],heel,density=density) for heel in np.linspace(-180,180,49)]
                positive=[p['righting_Nm']*np.sign(p['heel_deg']) for p in points if 0<abs(p['heel_deg'])<180]
                cases.append({'density_kg_m3':density,'mast_trim_deg':trim,'wing_state':name,'minimum_sampled_restoring_Nm':min(positive),'all_sampled_interior_angles_restore':bool(min(positive)>0),'points':points})
                print(density,trim,name,'minimum restoring',min(positive),flush=True)
    refinement=[]
    for name,fraction in [('sealed',1.),('lost_wing_buoyancy',0.)]:
        bodies=geometry(d,row,0.,2*resolution,fraction)
        coarse=next(c for c in cases if c['density_kg_m3']==1000 and c['mast_trim_deg']==0 and c['wing_state']==name)
        for heel in [15.,90.,135.,165.]:
            fine=free_pitch_equilibrium(kernel,bodies,cg,row['totalMass'],heel,density=1000.)
            previous=next(p for p in coarse['points'] if p['heel_deg']==heel)
            refinement.append({'wing_state':name,'heel_deg':heel,'coarse_resolution':resolution,'fine_resolution':2*resolution,
                'coarse_righting_Nm':previous['righting_Nm'],'fine_righting_Nm':fine['righting_Nm'],'change_Nm':fine['righting_Nm']-previous['righting_Nm']})
    sources=['models/hydrostatics.sysml','scripts/native_hydrostatics.py','scripts/hydrostatics_batch.c','scripts/hydro_geometry.py','scripts/study_hydrostatics.py','docs/analysis/mission-sizing.json','docs/analysis/wing-geometry.json']
    result={'sourceHashes':{s:digest(ROOT/s) for s in sources},'resolution':resolution,'design':d,'mass_kg':row['totalMass'],'cg_m':cg,'cases':cases,'mesh_refinement':refinement,
      'qualified':False,'scope':'Diagnostic only: new elliptical-planform hull family with saved design dimensions/mass/CG; rectangular wing from CAD midsection. Prescribed roll with heave and pitch equilibrium; nearest-zero pitch equilibrium within +/-85 degrees, pitch stability and alternative stable branches recorded. No dynamic release or global equilibrium proof. Lost-wing-buoyancy is a conservative sensitivity omitting material buoyancy, not a detailed flooded-body model. Keel/rudder structural displacement omitted. Retained water absent. Hull and wing material mass not yet recomputed for these shapes. No capsize requirement verdict.'}
    (ROOT/'docs/analysis/hydrostatics.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resolution',type=int,default=8);run(p.parse_args().resolution)

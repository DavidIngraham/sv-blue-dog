"""Capytaine radiation/diffraction at a fixed candidate's mean geometry.

Three response DOFs; native full-body hydrostatics and component mass allocation.
Forward-speed coefficients are cached, not evaluated inside each sailing solve.
"""
import json
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull
import capytaine as cpt
from capytaine.bem.airy_waves import froude_krylov_force
from ..model.runtime import ROOT,native,native_value
from ..model.vessel import CoupledModel
from ..geometry.hydro import equilibrium
from .inertia import mass_moments

DOFS=('Heave','Roll','Pitch')


def policy_inputs():
    report=json.loads(native('-analysis','BlueDogWavePerformance::Inputs','-json'))
    return {v['name']:native_value(v['value']) for v in report['checks'][0]['values']}


def mesh_part(tetrahedra,name,resolution):
    points=np.unique(np.round(tetrahedra.reshape(-1,3),12),axis=0)
    # Existing foil sections have 41 chord stations. Select a nested set of
    # stations for the BEM mesh, including both edges; retain exact section points.
    if name in ('keel','rudder'):
        xs=np.unique(points[:,0]);chosen=xs[np.unique(np.linspace(0,len(xs)-1,resolution+1).round().astype(int))]
        points=points[np.isin(points[:,0],chosen)]
    hull=ConvexHull(points);faces=hull.simplices.copy();tri=points[faces]
    inward=np.einsum('ij,ij->i',np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),tri.mean(axis=1)-points.mean(axis=0))<0
    faces[inward]=faces[inward][:,::-1]
    return cpt.Mesh(vertices=points,faces=np.c_[faces,faces[:,2]],name=name)


def geometry(design,resolution):
    model=CoupledModel();x=[design[n] for n in model.c['designNames']]
    bodies,mass,_,_=model.configuration(x,0.,resolution=12)
    mesh_bodies,_,_,_=model.configuration(x,0.,resolution=resolution)
    tensor,cg=mass_moments(bodies,mass,design,model.parameters,model.c['materialValues'])
    h=equilibrium(model.hydro,bodies,cg,mass['totalMass'],0.,0.,density=model.parameters[31])
    waterline=h['waterline_m'];shift=np.array([0,0,waterline])
    meshes=[mesh_part(b.tetrahedra-shift,b.name,resolution) for b in mesh_bodies if b.name!='wing']
    combined=meshes[0]
    for mesh in meshes[1:]:combined=combined+mesh
    body=cpt.FloatingBody(mesh=combined,center_of_mass=cg-shift,mass=mass['totalMass'],name='blue-dog')
    body.add_translation_dof(name='Heave')
    body.add_rotation_dof(rotation_center=cg-shift,direction=(1,0,0),name='Roll')
    body.add_rotation_dof(rotation_center=cg-shift,direction=(0,1,0),name='Pitch')
    body=body.immersed_part()
    # Linearize full-body buoyancy/gravity about CG at fixed mean waterline.
    def force(q):
        heave,roll,pitch=q;cr,sr=np.cos(roll),np.sin(roll);cp,sp=np.cos(pitch),np.sin(pitch)
        R=np.array([[cp,sp*sr,sp*cr],[0,cr,-sr],[-sp,cp*sr,cp*cr]])
        sums=np.zeros(4)
        for b in bodies:
            t=(b.tetrahedra-cg)@R.T+cg+[0,0,heave]
            sums+=model.hydro.moments(t,waterline)
        rho,g=model.parameters[31],model.parameters[34];cb=sums[1:]-sums[0]*(cg+[0,0,heave])
        return np.array([g*(rho*sums[0]-mass['totalMass']),rho*g*cb[1],-rho*g*cb[0]])
    eps=1e-4;K=np.column_stack([-(force(np.eye(3)[i]*eps)-force(-np.eye(3)[i]*eps))/(2*eps) for i in range(3)])
    K=(K+K.T)/2
    M=np.zeros((3,3));M[0,0]=mass['totalMass'];M[1:,1:]=tensor[:2,:2]
    if np.linalg.eigvalsh(K).min()<=0:raise ValueError('Unstable mean hydrostatic response')
    return body,dict(massMatrix=M.tolist(),stiffness=K.tolist(),cg=(cg-shift).tolist(),
        waterlineM=waterline,draftM=waterline+design['bottom_depth_m'],mass=mass,
        inertiaTensor=tensor.tolist(),faces=body.mesh.nb_faces,meshResolution=resolution,
        meanHydrostaticForce=force(np.zeros(3)).tolist())


def generate(design,policy,resolution,destination):
    body,metadata=geometry(design,resolution);solver=cpt.BEMSolver();rows=[]
    for period in policy['periods']:
        for speed in policy['speeds']:
            for direction in policy['directions']:
                common=dict(body=body,period=period,forward_speed=speed,wave_direction=np.deg2rad(direction),rho=1000.,g=9.80665)
                radiations=[solver.solve(cpt.RadiationProblem(**common,radiating_dof=d),keep_details=False) for d in DOFS]
                diffraction=solver.solve(cpt.DiffractionProblem(**common),keep_details=False)
                A=np.array([[r.added_mass[d] for r in radiations] for d in DOFS]);B=np.array([[r.radiation_damping[d] for r in radiations] for d in DOFS])
                incident=froude_krylov_force(diffraction.problem)
                F=np.array([diffraction.forces[d]+incident[d] for d in DOFS])
                rows.append(dict(period=period,speed=speed,direction=direction,addedMass=A.tolist(),damping=B.tolist(),forceReal=F.real.tolist(),forceImag=F.imag.tolist()))
                print('BEM',resolution,period,speed,direction,flush=True)
    record=dict(design=design,metadata=metadata,policy=policy,rows=rows,capytaineVersion=cpt.__version__,
        excitationConvention='Froude-Krylov plus diffraction; unit wave amplitude',
        scope='Linear heave/roll/pitch response about upright fixed geometry; component-distributed inertia, point equipment, approximate forward speed. No response qualification.')
    destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(json.dumps(record,indent=2)+'\n')
    return record


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh',type=int)
    parser.add_argument('--output',type=Path,default=ROOT/'build/analysis/wave-performance/bem.json')
    args=parser.parse_args();policy=policy_inputs()
    design=json.loads((ROOT/'evidence/runs/2026-10-13-surface-environment/operating-1.4.json').read_text())['design']
    generate(design,policy,args.mesh or int(policy['settings'][7]),args.output)

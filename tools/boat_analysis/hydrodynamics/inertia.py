"""Mass moments of the existing skin/rib/equipment allocation."""
import numpy as np
from ..model.vessel import skin_triangles


def distribution(vertices,weights,total):
    weights=np.asarray(weights);weights=weights/weights.sum()*total
    n=vertices.shape[1];s=vertices.sum(axis=1)
    second=(np.einsum('nki,nkj->nij',vertices,vertices)+np.einsum('ni,nj->nij',s,s))/(n*(n+1))
    return weights.sum(),np.einsum('n,ni->i',weights,vertices.mean(axis=1)),np.einsum('n,nij->ij',weights,second)


def mass_moments(bodies,mass,design,parameters,materials):
    d,p,m=design,parameters,materials;allocations=[]
    def add(points,weights,kg):
        if kg>0:allocations.append(distribution(np.asarray(points),weights,kg))
    for body in bodies:
        t=body.tetrahedra;vol=np.abs(np.linalg.det(t[:,1:]-t[:,:1]))/6
        if body.name=='ballast':add(t,vol,d['ballast_kg']);continue
        triangles=skin_triangles(t);area=np.linalg.norm(np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]),axis=1)/2
        kg=mass[body.name+'Mass']
        rib=0 if body.name=='hull' else m[3]*vol.sum()*m[4]/d['foil_rib_pitch_m']
        add(triangles,area,kg-rib)
        if rib:add(t,vol,rib)
    def point(kg,xyz):add(np.array(xyz)[None,None,:],[1],kg)
    L=d['length_m'];bottom=d['bottom_depth_m'];top=d['deck_height_m']
    point(mass['batteryMass'],[d['battery_x_fraction']*L,0,-bottom+(bottom+top)*d['battery_z_fraction']])
    point(mass['panelMass'],[0,0,top])
    point(mass['wingDriveMass'],[d['mast_x_fraction']*L,0,-bottom/2])
    point(mass['rudderDriveMass'],[-d['rudder_arm_fraction']*L,0,-bottom/2])
    point(mass['equipmentMass']-p[38],[0,0,-bottom/2]);point(p[38],[p[39]*L,0,top+p[40]])
    total=sum(a[0] for a in allocations);cg=sum(a[1] for a in allocations)/total
    covariance=sum(a[2] for a in allocations)-total*np.outer(cg,cg)
    tensor=np.eye(3)*np.trace(covariance)-covariance
    expected=np.array([mass['cgX'],mass['cgY'],mass['cgZ']])
    if abs(total-mass['totalMass'])>1e-8 or np.linalg.norm(cg-expected)>1e-7:
        raise ValueError('Inertia allocation does not reproduce native mass and CG')
    return tensor,cg

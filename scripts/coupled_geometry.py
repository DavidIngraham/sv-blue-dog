"""Geometric metrics for the coupled mass/strength and buoyancy models.

Geometry is external to SysML, like CAD/VSP geometry. Material accounting and
engineering balance remain native calculations. No material density is used here.
"""
from functools import lru_cache
import json
import numpy as np
from .native_design_kernel import ROOT
from .hydro_geometry import hull_geometry,ellipsoid

@lru_cache(maxsize=1)
def section_data():
    data=json.loads((ROOT/'docs/analysis/wing-geometry.json').read_text())
    p=next(p for p in data['profiles'] if p['span_station_mm']==150)
    if p['incomplete_samples']:raise ValueError('Incomplete reference section')
    x=np.array(p['x_mm']);u=(x-x[0])/(x[-1]-x[0]);top=-np.array(p['lower_mm']);bottom=-np.array(p['upper_mm'])
    mean=(top+bottom)/2;half=(top-bottom)/2
    mean=(mean-np.linspace(mean[0],mean[-1],len(mean)))/p['chord_mm']
    return u,mean,half/p['chord_mm']


def wing_section(camber,thickness=1.,resolution=40):
    u,mean,half=section_data();x=np.linspace(0,1,resolution+1)
    mean=np.interp(x,u,mean)*camber;half=np.interp(x,u,half)*thickness
    return np.c_[x,mean+half],np.c_[x,mean-half]


def prism(upper,lower,span):
    tetra=[]
    for i in range(len(upper)-1):
        quad=np.c_[np.array([lower[i],lower[i+1],upper[i+1],upper[i]]),np.zeros(4)]
        for indices in [[0,1,2],[0,2,3]]:
            a,b,c=quad[indices];aa,bb,cc=quad[indices]+[0,0,span]
            tetra.extend([[a,b,c,aa],[b,c,aa,bb],[c,aa,bb,cc]])
    return np.array(tetra)


def metrics(tetrahedra):
    """Return external skin area/centroid and enclosed volume/centroid."""
    t=np.asarray(tetrahedra)
    volumes=np.abs(np.linalg.det(t[:,1:]-t[:,:1]))/6
    t=t[volumes > max(1e-20,volumes.max()*1e-12)]
    vertices,inverse=np.unique(np.round(t.reshape(-1,3),12),axis=0,return_inverse=True)
    indices=inverse.reshape(-1,4)
    faces=np.concatenate([indices[:,triplet] for triplet in [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]])
    unique,counts=np.unique(np.sort(faces,axis=1),axis=0,return_counts=True)
    if np.any(counts>2):raise ValueError('Nonmanifold tetrahedral boundary')
    triangles=vertices[unique[counts==1]]
    areas=np.linalg.norm(np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]),axis=1)/2
    volumes=np.abs(np.linalg.det(t[:,1:]-t[:,:1]))/6
    if min(areas.sum(),volumes.sum())<=0:raise ValueError('Degenerate body')
    return np.r_[areas.sum(),np.average(triangles.mean(axis=1),axis=0,weights=areas),volumes.sum(),np.average(t.mean(axis=1),axis=0,weights=volumes)]


def section_properties(polygon):
    """Thin-skin section metrics, per unit laminate thickness.

    Output: minimum principal inertia [m3], worst-direction section modulus [m2],
    enclosed area [m2], perimeter [m]. Uses exact line integrals on polygon edges.
    """
    p=np.asarray(polygon);q=np.roll(p,-1,axis=0);lengths=np.linalg.norm(q-p,axis=1)
    centroid=np.sum(lengths[:,None]*(p+q)/2,axis=0)/lengths.sum()
    a,b=p-centroid,q-centroid
    covariance=np.sum(lengths[:,None,None]*((a[:,:,None]*a[:,None,:]+b[:,:,None]*b[:,None,:])/3+(a[:,:,None]*b[:,None,:]+b[:,:,None]*a[:,None,:])/6),axis=0)
    moment=np.array([[covariance[1,1],-covariance[0,1]],[-covariance[0,1],covariance[0,0]]])
    # Sigma/t = [y,-x] . inv(moment) . [Mx,My]; worst unit moment magnitude.
    stresses=np.linalg.norm(np.c_[a[:,1],-a[:,0]]@np.linalg.inv(moment),axis=1)
    area=abs(np.sum(p[:,0]*q[:,1]-q[:,0]*p[:,1]))/2
    return np.array([np.linalg.eigvalsh(moment).min(),1/stresses.max(),area,lengths.sum()])


def build_geometry(d,resolution=8):
    length,beam,depth,top=d['length_m'],d['beam_m'],d['bottom_depth_m'],d['deck_height_m']
    hull=hull_geometry(length,beam,depth,top,resolution)
    phi=np.linspace(-np.pi/2,np.pi/2,2*resolution+1)
    hull_section=np.vstack([np.c_[beam/2*np.sin(phi),-depth*np.cos(phi)],[[beam/2,top],[-beam/2,top]]])
    upper,lower=wing_section(d['camber_scale'],d['wing_thickness_scale'])
    chord=np.sqrt(d['sail_m2']/d['sail_AR']);span=np.sqrt(d['sail_m2']*d['sail_AR'])
    upper=upper*chord-[d['mast_fraction']*chord,0];lower=lower*chord-[d['mast_fraction']*chord,0]
    wing=prism(upper,lower,span)+[d['mast_x_fraction']*length,0,top]
    geometries={'hull':hull,'wing':wing};sections={'hull':section_properties(hull_section),'wing':section_properties(np.vstack([upper,lower[::-1]]))}
    for name,x in [('keel',0),('rudder',-d['rudder_arm_fraction']*length)]:
        chord=d[f'{name}_m2']/d[f'{name}_span_m'];span=d[f'{name}_span_m']
        u=np.linspace(0,1,41);thickness=.12*chord*np.sqrt(np.maximum(0,1-(2*u-1)**2))/2
        upper=np.c_[(u-.5)*chord,thickness];lower=np.c_[(u-.5)*chord,-thickness]
        body=prism(upper,lower,span);body[:,:,2]*=-1;body+=[x,0,-depth]
        geometries[name]=body;sections[name]=section_properties(np.vstack([upper,lower[::-1]]))
    vectors={name:np.r_[metrics(body),sections[name]] for name,body in geometries.items()}
    return geometries,vectors


def ballast_geometry(volume_m3,keel_tip_z,resolution=8):
    """3:1:1 bulb, volume-normalized mesh, touching the keel tip without overlap."""
    if volume_m3<=0:raise ValueError('Positive ballast volume required')
    unit=ellipsoid([3,1,1],resolution=resolution)
    scale=(volume_m3/metrics(unit)[4])**(1/3)
    center=np.array([0.,0.,keel_tip_z-scale])
    return unit*scale+center,center

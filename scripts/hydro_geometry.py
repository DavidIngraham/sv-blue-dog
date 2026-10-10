"""Geometry construction and numerical waterline equilibrium; physics is native SysML."""
from dataclasses import dataclass
import json
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import brentq
from .native_design_kernel import ROOT

@dataclass
class DisplacementBody:
    name: str
    tetrahedra: np.ndarray
    buoyant_fraction: float = 1.0


def convex_tetrahedra(points):
    points=np.asarray(points,dtype=float);hull=ConvexHull(points);center=points[hull.vertices].mean(axis=0)
    return np.array([[center,*points[triangle]] for triangle in hull.simplices])


def ellipsoid(axes,center=(0,0,0),resolution=12):
    # Staggered latitude/longitude sampling; convex hull closes pole caps.
    points=[]
    for latitude in np.linspace(-np.pi/2,np.pi/2,resolution+1):
        for longitude in np.linspace(0,2*np.pi,2*resolution,endpoint=False):
            points.append([np.cos(latitude)*np.cos(longitude),np.cos(latitude)*np.sin(longitude),np.sin(latitude)])
    return convex_tetrahedra(np.unique(np.round(points,14),axis=0)*np.asarray(axes)+center)


def hull_geometry(length,beam,draft,freeboard,resolution=12):
    # Elliptical planform with semi-elliptical bottom and vertical topsides.
    # This is a sizing hull family, not imported prototype hull CAD.
    points=[]
    for angle in np.linspace(-np.pi/2,np.pi/2,2*resolution+1):
        x=length/2*np.sin(angle);scale=np.cos(angle)
        for phi in np.linspace(-np.pi/2,np.pi/2,resolution+1):
            points.append([x,beam/2*scale*np.sin(phi),-draft*scale*np.cos(phi)])
        points.extend([[x,-beam/2*scale,freeboard],[x,beam/2*scale,freeboard]])
    return convex_tetrahedra(np.unique(np.round(points,14),axis=0))


def wing_geometry(area,aspect,camber_scale=1.0,mast_fraction=.5,mast_x=0.,base_z=0.,trim_deg=0.,resolution=40):
    p=next(p for p in json.loads((ROOT/'docs/analysis/wing-geometry.json').read_text())['profiles'] if p['span_station_mm']==150)
    if p['incomplete_samples']:raise ValueError('Reference wing section is incomplete')
    x=np.asarray(p['x_mm']);u=np.linspace(0,1,resolution+1)
    xp=(x-x[0])/(x[-1]-x[0]);upper=np.interp(u,xp,-np.array(p['lower_mm']));lower=np.interp(u,xp,-np.array(p['upper_mm']))
    mean=(upper+lower)/2;thickness=(upper-lower)/2
    mean=(mean-np.linspace(mean[0],mean[-1],len(mean)))*camber_scale
    chord=np.sqrt(area/aspect);span=np.sqrt(area*aspect)
    upper=(mean+thickness)/p['chord_mm']*chord;lower=(mean-thickness)/p['chord_mm']*chord
    xx=(u-mast_fraction)*chord;tetra=[]
    # Each outer-envelope chord strip is a quad, split into two triangles.
    for i in range(resolution):
        quad=np.array([[xx[i],lower[i],0],[xx[i+1],lower[i+1],0],[xx[i+1],upper[i+1],0],[xx[i],upper[i],0]])
        for indices in [[0,1,2],[0,2,3]]:
            a,b,c=quad[indices];aa,bb,cc=quad[indices]+[0,0,span]
            tetra.extend([[a,b,c,aa],[b,c,aa,bb],[c,aa,bb,cc]])
    theta=np.deg2rad(trim_deg);rotation=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    return np.asarray(tetra)@rotation.T+[mast_x,0,base_z]


def pose(points,heel_deg,pitch_deg=0.):
    r,p=np.deg2rad([heel_deg,pitch_deg])
    roll=np.array([[1,0,0],[0,np.cos(r),-np.sin(r)],[0,np.sin(r),np.cos(r)]])
    pitch=np.array([[np.cos(p),0,np.sin(p)],[0,1,0],[-np.sin(p),0,np.cos(p)]])
    return np.asarray(points)@(pitch@roll).T


def equilibrium(kernel,bodies,cg,mass,heel_deg,trim_pitch_deg=0.,density=1000.):
    geometry=[(pose(b.tetrahedra,heel_deg,trim_pitch_deg),b.buoyant_fraction) for b in bodies]
    if any(not 0<=fraction<=1 for _,fraction in geometry):raise ValueError('Buoyant fraction outside [0,1]')
    low=min(t[:,:,2].min() for t,_ in geometry)-.01;high=max(t[:,:,2].max() for t,_ in geometry)+.01
    world_cg=pose(cg,heel_deg,trim_pitch_deg)
    def moment(h):return sum((fraction*kernel.moments(t,h) for t,fraction in geometry if fraction),np.zeros(4))
    def residual(h):return kernel.balance(moment(h),world_cg,mass,density)[0]
    if residual(high)<0:raise ValueError('Insufficient enclosed displacement to float')
    h=brentq(residual,low,high,xtol=1e-10)
    m=moment(h);balance=kernel.balance(m,world_cg,mass,density)
    return {'heel_deg':float(heel_deg),'pitch_deg':float(trim_pitch_deg),'waterline_m':float(h),'displaced_m3':float(m[0]),'buoyancy_center_m':(m[1:]/m[0]).tolist(),'mass_residual_kg':float(balance[0]),'roll_torque_Nm':float(balance[1]),'pitch_torque_Nm':float(balance[2]),'righting_Nm':float(-balance[1])}

def free_pitch_equilibrium(kernel,bodies,cg,mass,heel_deg,density=1000.,preferred_pitch=0.):
    """Select a pitch equilibrium branch, recording its stability and alternatives.

    Roll remains prescribed; heave and pitch equilibrate. This is a static
    reduced curve, not proof of dynamic recovery or absence of every equilibrium.
    """
    cache={}
    def state(pitch):
        key=float(pitch)
        if key not in cache:cache[key]=equilibrium(kernel,bodies,cg,mass,heel_deg,key,density)
        return cache[key]
    def residual(pitch):return state(pitch)['pitch_torque_Nm']
    nodes=sorted(set([-85.,-60.,-30.,0.,30.,60.,85.,float(preferred_pitch)]))
    roots=[]
    for a,b in zip(nodes,nodes[1:]):
        fa,fb=residual(a),residual(b)
        if abs(fa)<1e-8:roots.append(a)
        elif fa*fb<0:roots.append(brentq(residual,a,b,xtol=1e-8))
    if abs(residual(nodes[-1]))<1e-8:roots.append(nodes[-1])
    stable=[]
    for root in sorted(set(round(r,8) for r in roots)):
        slope=(residual(root+.001)-residual(root-.001))/.002
        if slope<0:stable.append(root)
    if not roots:raise ValueError('No pitch equilibrium within +/-85 degrees')
    selected=min(roots,key=lambda p:abs(p-preferred_pitch))
    result=dict(state(selected))
    result['righting_Nm']=-result['roll_torque_Nm']*np.cos(np.deg2rad(selected))
    result['pitch_stable_branches_deg']=stable
    result['pitch_stable']=any(abs(selected-r)<1e-6 for r in stable)
    return result

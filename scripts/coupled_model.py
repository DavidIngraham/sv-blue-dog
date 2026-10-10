"""Coupled geometric pose, buoyancy and native operating equations."""
import numpy as np
from scipy.optimize import brentq
from .coupled_geometry import build_geometry,ballast_geometry
from .hydro_geometry import DisplacementBody,equilibrium,pose
from .native_coupled import MassKernel
from .native_coupled_operation import OperationKernel
from .native_hydrostatics import HydroKernel
from .wing_polar import WingPolar


def skin_triangles(t):
    volumes=np.abs(np.linalg.det(t[:,1:]-t[:,:1]))/6;t=t[volumes>max(1e-20,volumes.max()*1e-12)]
    vertices,inverse=np.unique(np.round(t.reshape(-1,3),12),axis=0,return_inverse=True);indices=inverse.reshape(-1,4)
    faces=np.concatenate([indices[:,triplet] for triplet in [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]])
    unique,counts=np.unique(np.sort(faces,axis=1),axis=0,return_counts=True)
    return vertices[unique[counts==1]]


def wet_area(triangles,height):
    wet=triangles[:,:,2]<=height
    full=triangles[np.all(wet,axis=1)]
    total=np.linalg.norm(np.cross(full[:,1]-full[:,0],full[:,2]-full[:,0]),axis=1).sum()/2
    for triangle in triangles[np.any(wet,axis=1)&~np.all(wet,axis=1)]:
        polygon=[]
        for a,b in zip(triangle,np.roll(triangle,-1,axis=0)):
            if a[2]<=height:polygon.append(a)
            if (a[2]<height<b[2]) or (b[2]<height<a[2]):polygon.append(a+(b-a)*(height-a[2])/(b[2]-a[2]))
        if len(polygon)>=3:
            poly=np.array(polygon);total+=sum(np.linalg.norm(np.cross(poly[i]-poly[0],poly[i+1]-poly[0]))/2 for i in range(1,len(poly)-1))
    return float(total)

class CoupledModel:
    def __init__(self):
        self.mass=MassKernel();self.operation=OperationKernel();self.hydro=HydroKernel();self.polar=WingPolar()
        self.c=self.mass.contract;self.parameters=np.array(self.c['parameterValues']);self.last=None
    def candidate(self,x,resolution=4):
        if self.last is not None and np.array_equal(x,self.last[0]) and resolution==self.last[1]:return self.last[2]
        d=dict(zip(self.c['designNames'],x));g,v=build_geometry(d,resolution)
        bulb,center=ballast_geometry(d['ballast_kg']/self.parameters[33],-d['bottom_depth_m']-d['keel_span_m'],resolution)
        g['ballast']=bulb
        result=(d,g,v,center,skin_triangles(g['hull']))
        self.last=(np.array(x,copy=True),resolution,result)
        return result
    def configuration(self,x,trim,resolution=4):
        d,g,v,center,hull_skin=self.candidate(x,resolution)
        rotation=np.array([[np.cos(trim),-np.sin(trim),0],[np.sin(trim),np.cos(trim),0],[0,0,1]])
        mast=np.array([d['mast_x_fraction']*d['length_m'],0,d['deck_height_m']])
        def transform(points):return ((np.asarray(points)-mast)*[1,-1,1])@rotation.T+mast
        vectors={name:a.copy() for name,a in v.items()}
        vectors['wing'][1:4]=transform(v['wing'][1:4]);vectors['wing'][5:8]=transform(v['wing'][5:8])
        m=self.mass.evaluate(x,np.r_[np.concatenate(list(vectors.values())),center],self.parameters)
        bodies=[DisplacementBody(name,transform(body) if name=='wing' else body) for name,body in g.items()]
        return bodies,m,np.r_[np.concatenate(list(vectors.values())),center],hull_skin
    def at_state(self,x,state,resolution=4,pitch_equilibrium=True):
        d,g,v,center,hull_skin=self.candidate(x,resolution)
        wind,up,foul,speed,heading,alpha,beta,delta,heel=state
        awx=wind*np.cos(np.deg2rad(heading))+speed*np.cos(np.deg2rad(beta))
        awy=wind*np.sin(np.deg2rad(heading))-speed*np.sin(np.deg2rad(beta))
        # VSP X is LE->TE, Y span, Z section-normal. Wing span maps to boat +Z.
        # In the geometric x/section-height/span storage, flip height before yaw.
        reverse_flow=heading<0
        trim=np.pi-np.arctan2(awy,awx)+np.deg2rad(alpha)+(np.pi if reverse_flow else 0)
        bodies,m,geometry,hull_skin=self.configuration(x,trim,resolution)
        cg=np.array([m['cgX'],m['cgY'],m['cgZ']]);mass=m['totalMass']
        cache={}
        def hydro_at(pitch):
            if pitch not in cache:cache[pitch]=equilibrium(self.hydro,bodies,cg,mass,heel,pitch,density=self.parameters[31])
            return cache[pitch]
        pitch=0.
        if pitch_equilibrium:
            pitch=brentq(lambda a:hydro_at(a)['pitch_torque_Nm'],-20,20,xtol=1e-6)
        h=hydro_at(pitch)
        wetted=wet_area(pose(hull_skin,heel,pitch),h['waterline_m'])
        aero=self.polar.evaluate(d['sail_AR'],d['camber_scale'],alpha,reverse_flow=reverse_flow)
        result=self.operation.evaluate(x,self.parameters,state,aero,list(m.values()),[h['waterline_m'],h['righting_Nm'],wetted])
        result.update({'pitch_deg':pitch,'waterline_m':h['waterline_m'],'wetted_m2':wetted,'mast_trim_deg':float(np.rad2deg(trim)),'mass_kg':mass,'mass_residual_kg':h['mass_residual_kg'],'pitch_residual_Nm':h['pitch_torque_Nm']})
        return result

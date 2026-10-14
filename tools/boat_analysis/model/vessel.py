"""Coupled geometric pose, buoyancy and native operating equations."""
import json
import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import brentq
from tools.boat_analysis.geometry.vessel import build_geometry,ballast_geometry
from tools.boat_analysis.geometry.hydro import DisplacementBody,equilibrium,pose
from tools.boat_analysis.model.design_boundary import design_vector, pack, unpack
from tools.boat_analysis.model.design_types import Design, Parameters, OperatingState, AeroCoefficients, HydroState
from tools.boat_analysis.generated import mass, operation
from tools.boat_analysis.evidence.records import validate
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.model.hydrostatics import HydroKernel
from tools.boat_analysis.aerodynamics.polar import WingPolar
from tools.boat_analysis.geometry.hull import upright_hull_features,deck_area
from tools.boat_analysis.geometry.laminate import finite_skin_properties


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
        self.mass=mass;self.operation=operation;self.hydro=HydroKernel();self.polar=WingPolar()
        self.operating_contract=json.loads((ROOT/'.tools/coupled-operation-contract.json').read_text())
        validate(self.operating_contract['sourceHashes'])
        self.c=json.loads((ROOT/'.tools/coupled-contract.json').read_text());self.parameters=pack(Parameters.from_mapping(dict(zip(self.c['parameterNames'],self.c['parameterValues'],strict=True))),self.c['parameterNames']);self.last=None;self.hull_reference=None;self.section_cache=None
    def design_record(self, values: ArrayLike) -> Design:
        return unpack(Design, values, self.c['designNames'])

    @property
    def assumptions(self) -> Parameters:
        return unpack(Parameters, self.parameters, self.c['parameterNames'])

    def candidate(self,x: Design | ArrayLike,resolution=4):
        x=design_vector(x,self.c)
        if self.last is not None and np.array_equal(x,self.last[0]) and resolution==self.last[1]:return self.last[2]
        d=dict(zip(self.c['designNames'],x));g,v,outlines=build_geometry(d,resolution)
        bulb,center=ballast_geometry(d['ballast_kg']/self.parameters[33],-d['bottom_depth_m']-d['keel_span_m'],resolution)
        g['ballast']=bulb
        result=(d,g,v,center,skin_triangles(g['hull']),outlines)
        self.last=(np.array(x,copy=True),resolution,result)
        return result
    def configuration(self,x: Design | ArrayLike,trim: float,resolution=4):
        x=design_vector(x,self.c)
        d,g,v,center,hull_skin,outlines=self.candidate(x,resolution)
        rotation=np.array([[np.cos(trim),-np.sin(trim),0],[np.sin(trim),np.cos(trim),0],[0,0,1]])
        mast=np.array([d['mast_x_fraction']*d['length_m'],0,d['deck_height_m']])
        def transform(points):return ((np.asarray(points)-mast)*[1,-1,1])@rotation.T+mast
        vectors={name:a.copy() for name,a in v.items()}
        vectors['wing'][1:4]=transform(v['wing'][1:4]);vectors['wing'][5:8]=transform(v['wing'][5:8])
        m=self.mass(design=x,geometry=np.r_[np.concatenate(list(vectors.values())),center],parameters=self.parameters).to_mapping()
        bodies=[DisplacementBody(name,transform(body) if name=='wing' else body) for name,body in g.items()]
        thicknesses=[m[name+'LaminateThickness'] for name in outlines]
        key=(tuple(x),resolution,tuple(thicknesses))
        if self.section_cache is None or self.section_cache[0]!=key:
            sections=np.concatenate([finite_skin_properties(outlines[name],thickness) for name,thickness in zip(outlines,thicknesses)])
            self.section_cache=(key,sections)
        return bodies,m,np.r_[np.concatenate(list(vectors.values())),center,deck_area(g['hull']),self.section_cache[1]],hull_skin
    def at_state(self,x: Design | ArrayLike,state: OperatingState | ArrayLike,resolution=4,pitch_equilibrium=True):
        x=design_vector(x,self.c)
        d,g,v,center,hull_skin,outlines=self.candidate(x,resolution)
        if not isinstance(state, OperatingState):
            state=unpack(OperatingState,state,self.operating_contract['MarineDesign::OperatingStateFields'])
        wind,up,foul,speed,heading,alpha,beta,delta,heel=(
            state.windSpeed_m_s,state.windward,state.foulingMultiplier,state.speed_m_s,
            state.windFrom_deg,state.incidence_deg,state.leeway_deg,state.rudder_deg,state.heel_deg)
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
        key=(tuple(x),resolution,float(self.parameters[31]),mass)
        if self.hull_reference is None or self.hull_reference[0]!=key:
            upright=equilibrium(self.hydro,bodies,cg,mass,0.,0.,density=self.parameters[31])
            hull=next(b for b in bodies if b.name=='hull')
            features=upright_hull_features(hull.tetrahedra,upright['waterline_m'])
            self.hull_reference=(key,features)
        features=self.hull_reference[1]
        aero=unpack(AeroCoefficients,aero,self.operating_contract['MarineDesign::AeroCoefficientsFields'])
        hydro=unpack(HydroState,np.r_[h['waterline_m'],h['righting_Nm'],wetted,features],
                     self.operating_contract['MarineDesign::HydroStateFields'])
        result=dict(self.operation(design=self.design_record(x),parameters=self.assumptions,state=state,aero=aero,mass=m,hydro=hydro))
        result.update({'pitch_deg':pitch,'waterline_m':h['waterline_m'],'wetted_m2':wetted,'mast_trim_deg':float(np.rad2deg(trim)),'mass_kg':mass,'mass_residual_kg':h['mass_residual_kg'],'pitch_residual_Nm':h['pitch_torque_Nm']})
        return result

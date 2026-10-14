"""Cycle-averaged sailing forces with bounded linear wave response.

The outer operating solve closes mean surge/sway/yaw/roll balance. Controls
remain fixed across a cycle. No wave-resolved steering or second-order BEM drift.
"""
import numpy as np
from .surface import SurfaceOperation,NativeCalculation
from ..environment.motion import point_motion


class WaveAveragedOperation:
    def __init__(self,contract,polar,wind_policy,response,height,period,wave_wind_angle,phases=None,resistance_coefficient=1.):
        self.surface=SurfaceOperation(contract,polar,wind_policy)
        self.contract=contract;self.response=response
        self.resistance_coefficient=resistance_coefficient
        self.height=height;self.period=period;self.wave_wind_angle=wave_wind_angle
        self.settings=response.policy['settings'];self.phases=int(phases or self.settings[0])
        self.orbital=NativeCalculation('MarineWavePerformance::OrbitalVelocity',1)
        self.foil=NativeCalculation('MarineWavePerformance::FoilLoad',1)
        self.balance=NativeCalculation('MarineWavePerformance::BalanceCorrection',1)
        self.actuation=NativeCalculation('MarineWavePerformance::Actuation',3)
        self.wave=NativeCalculation('MarineSurface::WaveScreen',1)

    def __call__(self, **inputs):
        return self.evaluate(**inputs)

    def evaluate(self,design,parameters,state,aero,mass,hydro):
        design,parameters,state,aero,mass,hydro=self.surface.pack(design,parameters,state,aero,mass,hydro)
        d,p,s=np.array(design),np.array(parameters),np.array(state)
        if self.height==0:
            result=self.surface.evaluate(d,p,s,aero,mass,hydro)
            result.update(waveCoverageMargin=1.,profileFailures=0,incidenceFailures=0,phaseCount=self.phases,addedWaveResistanceN=0.,motionAngleRad=0.)
            return result
        direction=self.wave_wind_angle-np.deg2rad(s[4])
        speeds=self.response.policy['speeds'];clipped=np.clip(s[3],min(speeds),max(speeds))
        speed_margin=min(s[3]-min(speeds),max(speeds)-s[3])
        a=self.height/2;origin=np.array(self.response.meta['cg'])
        beta,heel,delta=np.deg2rad(s[[6,8,7]]);cb,sb=np.cos(beta),np.sin(beta)
        q=self.contract['environment'];outputs=[];coverage=[];profile=incidence=0;max_angle=0.
        for pose,phase,k,encounter in self.response.samples(a,self.period,clipped,direction,self.phases):
            out=self.surface.evaluate(d,p,s,aero,mass,hydro,motion=pose,motion_origin=origin)
            profile+=out['surfaceHeightMargin']<0;incidence+=out['surfaceIncidenceMargin']<0
            max_angle=max(max_angle,float(max(abs(pose[1]),abs(pose[2]))))
            coverage.extend([self.settings[8]-self.response.mesh_error(self.period,clipped,direction),speed_margin,self.settings[2]-max(abs(pose[1]),abs(pose[2])),
                self.settings[3]-k*a,self.settings[5]*self.response.meta['draftM']-abs(pose[0]),self.settings[6]-abs(s[8])])
            forces=[]
            for index,(area,span,x,steer,inflow) in enumerate(((d[10],d[11],0.,0.,1.),(d[12],d[13],-d[14]*d[0],delta,q[1]))):
                depth=hydro[0]+d[2]+span/2
                point=[x,depth*np.sin(heel),-depth*np.cos(heel)]
                position,velocity,R=point_motion(point,pose,origin)
                localphase=phase+k*(position[0]*np.cos(direction)+position[1]*np.sin(direction))
                orbital=self.orbital([a,k,2*np.pi/self.period,position[2],localphase,direction,p[34]])
                flow=R.T@(np.array([s[3]*cb,s[3]*sb,0.])+velocity-orbital)
                v=np.linalg.norm(flow[:2])*inflow;localbeta=np.arctan2(flow[1],flow[0])
                root,_,_=point_motion([x,(hydro[0]+d[2])*np.sin(heel),-(hydro[0]+d[2])*np.cos(heel)],pose,origin)
                eta=a*np.cos(phase+k*(root[0]*np.cos(direction)+root[1]*np.sin(direction)))
                root_depth=eta-root[2]
                wet=np.clip(1+root_depth/span,0,1)
                load=self.foil([p[31],area,span,v,localbeta+steer,heel,p[27],p[28],s[2],p[26],np.deg2rad(q[0]),wet])
                coverage.extend([root_depth,flow[0],load[2],load[3]])
                forces.append((load,localbeta,position,v))
            lk,dk=forces[0][0][:2];lr,dr=forces[1][0][:2]
            old_yaw=(out['lr']*cb+out['dr']*sb)*(-d[14]*d[0])
            new_yaw=(lr*np.cos(forces[1][1])+dr*np.sin(forces[1][1]))*(-d[14]*d[0])
            kz=hydro[0]+d[2]+d[11]/2;rz=hydro[0]+d[2]+d[13]/2
            old_roll=((out['lk']*cb+out['dk']*sb)*kz+(out['lr']*cb+out['dr']*sb)*rz)*np.cos(heel)
            new_roll=sum((load[0]*np.cos(angle)+load[1]*np.sin(angle))*(-pos[2]) for load,angle,pos,v in forces)
            corrected=self.balance([*[out[n] for n in self.contract['outputNames'][:4]],out['dk']+out['dr'],dk+dr,out['lk']+out['lr'],lk+lr,old_yaw,new_yaw,old_roll,new_roll])
            out.update(zip(self.contract['outputNames'][:4],corrected))
            out['resistance']+=dk+dr-out['dk']-out['dr'];out['heeling']+=new_roll-old_roll
            out.update(lk=lk,lr=lr,dk=dk,dr=dr,keelResultant=float(np.hypot(lk,dk)),rudderResultant=float(np.hypot(lr,dr)))
            for prefix,item in zip(('keel','rudder'),forces):
                out[prefix+'LiftMargin']=item[0][2];out[prefix+'AngleMargin']=item[0][3]
            rudder_pressure_area=0.5*p[31]*forces[1][3]**2*d[12]
            rudder_cl=lr/max(rudder_pressure_area*np.cos(heel),1e-12)
            rudder_torque=rudder_pressure_area*np.hypot(rudder_cl,p[28])*q[2]*d[12]/d[13]+q[3]
            out['rudderTorque']=rudder_torque
            out['averagePower'],out['peakPower'],out['peakMargin']=self.actuation(p,q,[out['wingTorque'],rudder_torque,d[16]])
            out['rudderDriveMargin']=min(out['rudderDriveMargin'],1-p[35]*rudder_torque/d[19])
            out['keelRe']=forces[0][3]*(d[10]/d[11])/p[30]
            out['rudderRe']=forces[1][3]*(d[12]/d[13])/p[30]
            out['keelReMargin']=out['keelRe']/q[6]-1
            out['rudderReMargin']=out['rudderRe']/q[6]-1
            outputs.append(out)
        result={key:float(np.mean([o[key] for o in outputs])) for key in outputs[0]}
        for key in result:
            if 'Margin' in key or key.startswith('delftDomain'):result[key]=min(o[key] for o in outputs)
        for key in ('wingTorque','rudderTorque','peakPower','wingResultant','keelResultant','rudderResultant'):
            result[key]=max(o[key] for o in outputs)
        # First-order BEM does not supply mean drift resistance. Existing
        # explicit coefficient is applied once here, never again in the mission.
        freeboard=d[3]-hydro[0]
        added=self.wave([a,self.period,0.,d[0],d[1],s[3],np.cos(direction),self.resistance_coefficient,freeboard,freeboard,hydro[0]+d[2]+min(d[11],d[13]),p[34],p[31]])[3]
        result['surgeResidual']-=added/10;result['resistance']+=added
        margin=float(min(coverage));result['wingLiftMargin']=min(result['wingLiftMargin'],margin)
        result.update(waveCoverageMargin=margin,profileFailures=int(profile),incidenceFailures=int(incidence),phaseCount=self.phases,addedWaveResistanceN=float(added),motionAngleRad=max_angle)
        return result

"""Persistent directional wind seas and explicit nearby-traffic wake screens."""
import math
import numpy as np

from ..model.surface import NativeCalculation


class SeaHistory:
    def __init__(self, weather, policy, gravity=9.80665):
        fetch,tau,*_=policy
        if fetch<=0 or tau<=0:raise ValueError('Positive fetch and wave growth time required')
        growth=NativeCalculation('MarineSurface::FetchSea',1)
        self.rows=[];components={}
        decay=math.exp(-1/tau)
        for index,state in enumerate(weather.rows):
            # Two opposing long-crested trains preserve old waves after a wind
            # reversal. No independent draw can erase the previous sea state.
            direction=(state.wind_from_deg+180)%360
            target,period=growth([state.wind_mps,fetch,gravity])
            if index==0:components[direction]=(target,period)
            for key in list(components):
                h,t=components[key];components[key]=(h*math.sqrt(decay),t)
            previous=components.get(direction,(0.,period))[0]
            components[direction]=(math.sqrt(previous**2+(1-decay)*target**2),period)
            self.rows.append([(float(h),float(t),float(d)) for d,(h,t) in components.items() if h>1e-5])

    def at(self,seconds):
        index=int(seconds//3600)
        if index<0 or index>=len(self.rows):raise ValueError('Sea history outside coverage')
        return self.rows[index]


class WaveEffects:
    """Mean speed sensitivity, plus coverage and contact diagnostics.

    Does not integrate wave phase or vessel motion. No positive surfing credit.
    Current and vessel velocity are projected along each wave's propagation.
    """
    def __init__(self,inputs,weather,traffic=()):
        self.config=inputs['surfaceEnvironment'];self.policy=self.config['seaPolicy']
        self.sea=SeaHistory(weather,self.policy);self.traffic=traffic
        self.kernel=NativeCalculation('MarineSurface::WaveScreen',1)
        self.retention=NativeCalculation('MarineSurface::SpeedRetention',1)
        self.wakes={};self.seen=set();self.components=[];self.diagnostics=[]

    def update(self,seconds,position,current):
        self.current=current;self.components=list(self.sea.at(seconds))
        _,_,_,height,period,duration,radius=self.policy
        for i,actor in enumerate(self.traffic):
            if i in self.seen or actor.name not in ('commercial tow','recreational powerboat','passenger vessel'):continue
            if actor.start_seconds<=seconds<=actor.end_seconds:
                delta=np.asarray(position)-actor.position(seconds)
                if 0<np.linalg.norm(delta)<=radius:
                    # Radial propagation allocation, no claimed Kelvin wake model.
                    direction=(90-math.degrees(math.atan2(delta[1],delta[0])))%360
                    self.wakes[i]=(seconds+duration,height,period,direction);self.seen.add(i)
        for i,(expiry,h,t,d) in list(self.wakes.items()):
            if expiry>seconds:self.components.append((h,t,d))
            else:del self.wakes[i]

    def evaluate(self,wind,headings,speeds):
        scalar=np.ndim(speeds)==0
        heading=np.atleast_1d(headings);speeds=np.atleast_1d(speeds)
        cfg=self.config;d=cfg['geometry'];drag=np.interp(wind,cfg['winds'],cfg['calmResistanceN'])
        if drag<=0:raise ValueError('Positive calm-water resistance required')
        result=[];self.diagnostics=[]
        for angle,speed in zip(heading,speeds):
            added=0.;valid=True;hs2=0.;minimum_contact=np.full(3,np.inf);encounter=0.
            for h,t,propagation in self.components:
                radians=math.radians(90-propagation)
                along=float(np.dot(self.current,[math.cos(radians),math.sin(radians)]))
                cosine=math.cos(radians-math.radians(angle))
                values=self.kernel([h,t,along,*d[:2],speed,cosine,self.policy[2],*d[2:],9.80665,1000])
                hs2+=values[0]**2;added+=values[3];encounter=max(encounter,values[2])
                valid &= values[4]>0 and values[5]>=0
                minimum_contact=np.minimum(minimum_contact,values[6:9])
            retained=float(self.retention([added,drag])[0]) if valid else 0.
            result.append(speed*retained)
            self.diagnostics.append(dict(significantHeightM=math.sqrt(hs2),addedResistanceN=added,
                speedRetention=retained,covered=bool(valid),encounterRadS=encounter,
                contactScreen=bool(math.sqrt(hs2)>min(d[2:])),wakeCount=len(self.wakes)))
        return np.asarray(result)[0] if scalar else np.asarray(result)

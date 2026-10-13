"""Prescribed phase response and rigid-body point kinematics.

Coordinates: x forward, y port, z up; R = Ry(pitch) Rx(roll).
Motion is imposed, not a solution of the hydrodynamic equations of motion.
"""
import numpy as np
from ..model.surface import NativeCalculation


def rotation(pitch,roll):
    cp,sp=np.cos(pitch),np.sin(pitch);cr,sr=np.cos(roll),np.sin(roll)
    return np.array([[cp,sp*sr,sp*cr],[0,cr,-sr],[-sp,cp*sr,cp*cr]])


def point_motion(point,pose):
    heave,pitch,roll,vz,pitch_rate,roll_rate=pose
    matrix=rotation(pitch,roll)
    offset=matrix@np.asarray(point)
    omega=np.array([roll_rate*np.cos(pitch),pitch_rate,-roll_rate*np.sin(pitch)])
    return offset+np.array([0,0,heave]),np.cross(omega,offset)+[0,0,vz],matrix


class MotionResponse:
    def __init__(self,policy):
        self.heave,self.slope,count,self.limit=policy
        self.count=int(count)
        if self.count<8 or min(self.heave,self.slope)<0 or self.limit<=0:
            raise ValueError('Invalid prescribed motion policy')
        self.kernel=NativeCalculation('MarineSurface::HarmonicResponse',1)

    def samples(self,trains):
        # train = amplitude, k, signed encounter rad/s, propagation in body rad.
        # Regular equivalent wave H=2Hs. Diagnostic stress screen, not spectrum.
        for index in range(self.count):
            poses=[];waves=[]
            for j,(a,k,frequency,direction) in enumerate(trains):
                phase=2*np.pi*((index*(2*j+1)/self.count+j*.38196601125)%1)
                poses.append(self.kernel([a,k,frequency,phase,direction,self.heave,self.slope]))
                waves.append((a,k,direction,phase))
            yield np.sum(poses,axis=0) if poses else np.zeros(6),waves

    @staticmethod
    def elevation(position,waves):
        return sum(a*np.cos(phase+k*(position[0]*np.cos(d)+position[1]*np.sin(d))) for a,k,d,phase in waves)

    def clearance(self,trains,geometry,points=None):
        length,beam,freeboard,root,immersion=geometry
        # Hull corners, centerline wing root, and centerline appendage tip.
        points=points or ([[x,y,freeboard] for x in (-length/2,length/2) for y in (-beam/2,beam/2)] + [[0,0,root],[0,0,-immersion]])
        minimum=np.full(3,np.inf);covered=True;maximum_angle=0.
        for pose,waves in self.samples(trains):
            maximum_angle=max(maximum_angle,float(max(abs(pose[1]),abs(pose[2]))))
            covered &= maximum_angle<=self.limit
            heights=[]
            for point in points:
                position,_,_=point_motion(point,pose)
                heights.append(position[2]-self.elevation(position,waves))
            minimum=np.minimum(minimum,[min(heights[:4]),heights[4],-max(heights[5:])])
        return dict(minimumHullClearanceM=float(minimum[0]),minimumWingClearanceM=float(minimum[1]),
                    minimumAppendageImmersionM=float(minimum[2]),motionCovered=bool(covered),
                    maximumMotionAngleRad=maximum_angle,contactScreen=bool(min(minimum)<0))


def contact_points(design,geometry):
    """Bounding deck corners and actual longitudinal wing/appendage stations."""
    length,beam,freeboard,root,_=geometry
    waterline=design['deck_height_m']-freeboard
    points=[[x,y,freeboard] for x in (-length/2,length/2) for y in (-beam/2,beam/2)]
    points += [[design['mast_x_fraction']*length,0,root],
               [0,0,-waterline-design['bottom_depth_m']-design['keel_span_m']],
               [-design['rudder_arm_fraction']*length,0,-waterline-design['bottom_depth_m']-design['rudder_span_m']]]
    return points

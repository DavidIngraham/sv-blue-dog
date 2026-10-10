"""Extract upright bare-hull regression coordinates from a convex sizing mesh.

The regression uses static upright canoe-body geometry. Appendages are excluded.
This is deliberately separate from instantaneous heeled wetted-surface calculations.
"""
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import minimize_scalar


def section(points,axis,value):
    points=np.unique(np.asarray(points).reshape(-1,3),axis=0)
    hull=ConvexHull(points)
    faces=hull.simplices
    edges=np.unique(np.sort(np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]),axis=1),axis=0)
    a,b=points[edges[:,0]],points[edges[:,1]]
    da=a[:,axis]-value;db=b[:,axis]-value
    crossing=da*db<0
    cuts=a[crossing]+(b[crossing]-a[crossing])*(-da[crossing]/(db[crossing]-da[crossing]))[:,None]
    return np.unique(np.round(np.concatenate([points[np.abs(points[:,axis]-value)<1e-12],cuts]),12),axis=0)


def polygon_area_centroid(points,axes):
    q=np.asarray(points)[:,axes]
    if len(q)<3:return 0.,np.zeros(2)
    q=q[ConvexHull(q).vertices];n=np.roll(q,-1,axis=0)
    cross=q[:,0]*n[:,1]-n[:,0]*q[:,1]
    area=cross.sum()/2
    center=((q+n)*cross[:,None]).sum(axis=0)/(6*area)
    return abs(float(area)),center


def upright_hull_features(tetrahedra,waterline):
    points=np.unique(np.asarray(tetrahedra).reshape(-1,3),axis=0)
    if not points[:,2].min()<waterline<points[:,2].max():raise ValueError('Waterline must cut the canoe body')
    wp=section(points,2,waterline)
    wet=np.unique(np.concatenate([points[points[:,2]<waterline],wp]),axis=0)
    hull=ConvexHull(wet);center=wet[hull.vertices].mean(axis=0)
    triangles=wet[hull.simplices]
    volumes=np.abs(np.linalg.det(triangles-center))/6
    volume=volumes.sum();cb=(volumes[:,None]*(triangles.sum(axis=1)+center)/4).sum(axis=0)/volume
    aw,cf=polygon_area_centroid(wp,[0,1])
    aft,fore=wp[:,0].min(),wp[:,0].max();length=fore-aft
    beam=np.ptp(wp[:,1]);draft=waterline-wet[:,2].min()
    area=lambda x:polygon_area_centroid(section(wet,0,x),[1,2])[0]
    maximum=minimize_scalar(lambda x:-area(x),bounds=(aft+length*1e-7,fore-length*1e-7),method='bounded',options={'xatol':1e-9})
    amax=-maximum.fun
    # Midship area at half static waterline length, distinct from maximum area.
    amid=area((aft+fore)/2)
    return np.array([length,beam,draft,volume,aw,fore-cb[0],fore-cf[0],volume/(length*amax),amid/(beam*draft)])

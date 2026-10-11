"""Geometric stiffness properties of a finite laminate inside a section outline.

Polygon offsets define the inner boundary; Green's-theorem area integrals
supply centroidal moments. Engineering stress and deflection remain in SysML.
"""
import numpy as np
from shapely.geometry import Polygon


def _ring_moments(points):
    p=np.asarray(points,dtype=float);q=np.roll(p,-1,axis=0)
    cross=p[:,0]*q[:,1]-q[:,0]*p[:,1]
    raw=np.array([cross.sum()/2,
        np.sum((p[:,0]+q[:,0])*cross)/6,
        np.sum((p[:,1]+q[:,1])*cross)/6,
        np.sum((p[:,1]**2+p[:,1]*q[:,1]+q[:,1]**2)*cross)/12,
        np.sum((p[:,0]**2+p[:,0]*q[:,0]+q[:,0]**2)*cross)/12,
        np.sum((2*p[:,0]*p[:,1]+p[:,0]*q[:,1]+q[:,0]*p[:,1]+2*q[:,0]*q[:,1])*cross)/24])
    return raw if raw[0]>=0 else -raw


def _moments(geometry):
    if geometry.is_empty:return np.zeros(6)
    if geometry.geom_type=='Polygon':
        raw=_ring_moments(np.asarray(geometry.exterior.coords)[:-1])
        for ring in geometry.interiors:raw-=_ring_moments(np.asarray(ring.coords)[:-1])
        return raw
    if geometry.geom_type=='MultiPolygon':
        return sum((_moments(g) for g in geometry.geoms),np.zeros(6))
    raise ValueError('Expected polygonal section geometry')


def finite_skin_properties(outline,thickness):
    """Return minimum principal I [m4] and worst-direction section modulus [m3].

    The laminate occupies the outer polygon minus its inward offset. A filled
    section saturates at solid-section properties, never above them. The inner
    cavity can split or disappear; no FDM stiffness is credited.
    """
    p=np.asarray(outline,dtype=float)
    if p.ndim!=2 or p.shape[1]!=2 or not np.isfinite(p).all() or not np.isfinite(thickness) or thickness<=0:
        raise ValueError('Finite outline and positive laminate thickness required')
    p=p-p.mean(axis=0) # Avoid cancellation for translated geometry.
    outer=Polygon(p)
    if not outer.is_valid or outer.area<=0:raise ValueError('Invalid section outline')
    inner=outer.buffer(-float(thickness),join_style=2)
    raw=_moments(outer)-_moments(inner)
    area,mx,my,ix,iy,ixy=raw
    if area<=0:raise ValueError('Degenerate laminate section')
    cx,cy=mx/area,my/area
    inertia=np.array([[ix-area*cy*cy,-(ixy-area*cx*cy)],[-(ixy-area*cx*cy),iy-area*cx*cx]])
    minimum=float(np.linalg.eigvalsh(inertia).min())
    if minimum<=0:raise ValueError('Nonpositive laminate inertia')
    stress=np.linalg.norm(np.c_[p[:,1]-cy,-(p[:,0]-cx)]@np.linalg.inv(inertia),axis=1)
    return np.array([minimum,1/stress.max()])

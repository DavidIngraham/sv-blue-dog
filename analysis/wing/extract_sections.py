"""Extract planar STEP sections for geometry inspection (CAD units: mm)."""
import hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.gp import gp_Pln,gp_Pnt,gp_Dir
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.TopExp import TopExp_Explorer
from inspect_geometry import ROOT,load_shape,properties

def sections(shape,stations):
    result=[]
    for y in stations:
        cut=BRepAlgoAPI_Section(shape,gp_Pln(gp_Pnt(0,y,0),gp_Dir(0,1,0)),False)
        cut.Build()
        if not cut.IsDone():raise ValueError('Section failed')
        curves=[];it=TopExp_Explorer(cut.Shape(),TopAbs_EDGE)
        while it.More():
            curve=BRepAdaptor_Curve(TopoDS.Edge_s(it.Current()))
            points=[curve.Value(float(t)) for t in np.linspace(curve.FirstParameter(),curve.LastParameter(),81)]
            curves.append([[p.X(),p.Z()] for p in points]);it.Next()
        result.append({'span_station_mm':y,'edges_xz_mm':curves})
    return result

def outer_profile(section, count=161):
    # Intersect sampled edge segments with chordwise lines. Extremes select
    # exterior surfaces and discard rib/cavity boundaries inside the section.
    edges=[np.asarray(e) for e in section['edges_xz_mm']]
    allpoints=np.concatenate(edges);lo,hi=allpoints[:,0].min(),allpoints[:,0].max()
    x=np.linspace(lo+1e-5,hi-1e-5,count);upper=[];lower=[]
    for q in x:
        heights=[]
        for edge in edges:
            a,b=edge[:-1],edge[1:];dx=b[:,0]-a[:,0]
            use=(np.abs(dx)>1e-12)&(q>=np.minimum(a[:,0],b[:,0]))&(q<=np.maximum(a[:,0],b[:,0]))
            heights.extend((a[use,1]+(q-a[use,0])*((b[use,1]-a[use,1])/dx[use])).tolist())
        if len(heights)<2:
            upper.append(float('nan'));lower.append(float('nan'));continue
        upper.append(max(heights));lower.append(min(heights))
    return {'span_station_mm':section['span_station_mm'],'chord_mm':hi-lo,
            'x_mm':x.tolist(),'upper_mm':[None if np.isnan(z) else z for z in upper],'lower_mm':[None if np.isnan(z) else z for z in lower],
            'incomplete_samples':int(np.isnan(upper).sum()),'enclosed_area_mm2':float(np.trapezoid(np.array(upper)-lower,x)) if not np.isnan(upper).any() else None}

if __name__=='__main__':
    source=ROOT/'cad/SweptCrescentWing.STEP';shape=load_shape(source)
    profiles=[outer_profile(s) for s in sections(shape,[1,50,150,250,299])]
    result={'source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'units':'mm','axes':{'chord':'X','span':'Y','section_height':'Z'},'solid_properties':properties(shape),'profiles':profiles,
      'limitations':'Outer envelopes from sampled section edges; enclosed area excludes internal holes. Five interior stations do not establish a sealed watertight volume or complete full-vessel wing.'}
    output=ROOT/'docs/analysis/wing-geometry.json';output.write_text(json.dumps(result,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(9,3))
    for i,p in enumerate(profiles):
        color=f'C{i}'
        ax.plot(p['x_mm'],p['upper_mm'],color=color,label=f"y={p['span_station_mm']} mm")
        ax.plot(p['x_mm'],p['lower_mm'],color=color)
    ax.set(xlabel='CAD X / mm',ylabel='CAD Z / mm',title='Original STEP wing: extracted outer sections');ax.axis('equal');ax.grid();ax.legend(ncol=3)
    fig.tight_layout();fig.savefig(ROOT/'docs/figures/wing-sections.png',dpi=180)
    print([(p['span_station_mm'],p['chord_mm'],p['enclosed_area_mm2']) for p in profiles])

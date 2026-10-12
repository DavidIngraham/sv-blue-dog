"""Publish equal-scale concept sketches from accepted sizing evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from tools.boat_analysis.evidence.continuation import compatible_stages
from tools.boat_analysis.evidence.records import run_record,digest
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.geometry.export import export_candidate,COLORS

RUN='2026-10-12-finite-passage'


def figures(candidates,destination):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    points=np.concatenate([m.vertices for meshes,_ in candidates for m in meshes.values()])
    lo=points.min(axis=0)-.12;hi=points.max(axis=0)+.12
    fig=plt.figure(figsize=(14,7.6),layout='constrained')
    for row,(meshes,meta) in enumerate(candidates):
        for col,(name,elev,azim) in enumerate([('Isometric',18,-55),('Side',0,-90),('Front',0,0),('Top',90,-90)]):
            ax=fig.add_subplot(2,4,row*4+col+1,projection='3d')
            for component,mesh in meshes.items():
                ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor=COLORS[component],edgecolor='none',alpha=1))
            h=meta['waterlineM'];d=meta['design']
            ax.plot([-d['length_m']/2,d['length_m']/2],[-d['beam_m']/2-.015]*2,[h,h],color='#4098c1',lw=1.5)
            ax.scatter(*meta['cgM'],color='#ca2567',s=18,depthshade=False)
            ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]))
            ax.set_box_aspect(hi-lo);ax.set_proj_type('ortho');ax.view_init(elev,azim);ax.set_axis_off()
            ax.set_title(name,fontsize=10)
            if col==0:ax.text2D(0.,.02,f"{d['length_m']:.1f} m hull · {meta['massKg']:.1f} kg",transform=ax.transAxes,fontsize=11,weight='bold')
    fig.suptitle('Blue Dog sizing concepts — same scale',fontsize=17)
    fig.text(.5,.015,'Blue: hull  ·  Sand: wing  ·  Teal: keel  ·  Orange: rudder  ·  Slate: ballast  ·  Pink: CG',ha='center',fontsize=10)
    fig.savefig(destination/'sizing-concepts.png',dpi=180)
    plt.close(fig)


def render(output,run=RUN,figures_dir=None):
    from tools.boat_analysis.model.vessel import CoupledModel
    directory=ROOT/'evidence/runs'/run
    record=run_record(directory,'sizing-continuation.json')
    # Reject changed shape definitions instead of silently redrawing old results with new geometry.
    for path,expected in record['sourceHashes'].items():
        if path.startswith('tools/boat_analysis/geometry/') and digest(ROOT/path)!=expected:
            raise ValueError('Archived geometry source changed: '+path)
    stages=[s for s in compatible_stages(directory) if s['feasible']]
    chosen=[stages[0],stages[-1]]
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    model=CoupledModel();candidates=[];entries=[]
    for stage in chosen:
        label=f"candidate-{stage['lengthM']:.1f}".replace('.','p')
        meshes,meta=export_candidate(model,stage['design'],output/(label+'.glb'))
        if not np.isclose(meta['massKg'],stage['mass']['totalMass'],rtol=1e-9):raise ValueError('Candidate mass changed')
        meta.update(run=run,evidence='sizing-continuation.json',sourceHashes=record['sourceHashes'],
                    exporterSha256=digest(ROOT/'tools/boat_analysis/geometry/export.py'),
                    glbSha256=hashlib.sha256((output/(label+'.glb')).read_bytes()).hexdigest(),envelope=stage['envelope'])
        (output/(label+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
        candidates.append((meshes,meta));entries.append({'file':label+'.glb','metadata':label+'.json',**meta})
    (output/'candidates.json').write_text(json.dumps(entries,indent=2)+'\n')
    template=(ROOT/'tools/publishing/concepts.html').read_text(encoding='utf-8')
    (output/'index.html').write_text(template,encoding='utf-8')
    figures(candidates,figures_dir or output)
    return entries


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',default=RUN)
    p.add_argument('--output',type=Path,default=ROOT/'build/concepts');p.add_argument('--figures',type=Path)
    a=p.parse_args();render(a.output,a.run,a.figures)

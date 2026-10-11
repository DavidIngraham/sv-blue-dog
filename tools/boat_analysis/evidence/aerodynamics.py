"""Reproduce aerodynamic figures from immutable, hash-checked VSP run evidence."""
import hashlib
import json
from pathlib import Path
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from tools.boat_analysis.evidence.records import baseline_record
from tools.boat_analysis.model.runtime import ROOT


def render(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':11,'svg.fonttype':'none','svg.hashsalt':'blue-dog-vsp'})
    refs=[baseline_record(f'wing-vsp-reference-{n}.json') for n in (16,32,64)]
    grid=baseline_record('wing-polar-grid.json')['cases']
    geometry=baseline_record('wing-geometry.json')
    if len(grid)!=25 or any(len(c['values']['Alpha'])!=8 for c in grid):
        raise ValueError('Unexpected archived response grid')
    for case in grid:
        if not np.isfinite([case['values'][key] for key in ('Alpha','CLtot','CDi','CMytot')]).all():
            raise ValueError('Nonfinite aerodynamic evidence')
    def save(fig,name):
        fig.savefig(output/f'{name}.svg',metadata={'Date':None})
        fig.savefig(output/f'{name}.png',dpi=140)
        plt.close(fig)
    def axes(title):
        fig,axs=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
        fig.suptitle(title,weight='bold')
        for ax,label in zip(axs,('Lift coefficient CL','Induced drag coefficient CDi','Pitch moment coefficient CMy')):
            ax.set_xlabel('Angle of attack α (degrees)');ax.set_ylabel(label);ax.grid(alpha=.2)
        return fig,axs
    fig,axs=axes('Reference wing: mesh sensitivity (AR 4, area 1 m²)')
    for r in refs:
        for ax,key in zip(axs,('CLtot','CDi','CMytot')):
            ax.plot(r['results']['Alpha'],r['results'][key],'o-',label=f"Mesh parameter {r['mesh']}")
    axs[0].legend();fig.supxlabel('OpenVSP 3.54.0 · 5 m/s · CMy about midchord · exploratory VLM; no stall model')
    save(fig,'reference-sweeps')
    for mode,title in [('aspect','Aspect ratio sensitivity — original camber, forward chord'),('camber','Camber sensitivity — AR 4, forward chord'),('reverse','Chord-direction sensitivity — AR 4, original camber')]:
        fig,axs=axes(title)
        rows=[r for r in grid if (mode=='aspect' and r['camberScale']==1 and not r['reverseChord']) or (mode=='camber' and r['aspect']==4 and not r['reverseChord']) or (mode=='reverse' and r['aspect']==4 and r['camberScale']==1)]
        for r in rows:
            label=f"AR {r['aspect']:g}" if mode=='aspect' else f"Camber ×{r['camberScale']:g}" if mode=='camber' else ('Reversed chord' if r['reverseChord'] else 'Forward chord')
            for ax,key in zip(axs,('CLtot','CDi','CMytot')):ax.plot(r['values']['Alpha'],r['values'][key],'o-',label=label,markersize=3)
        axs[0].legend(fontsize=9);fig.supxlabel('Recorded samples joined by lines; not a stall prediction. Raw solver axes for both chord directions.')
        save(fig,mode+'-sweeps')
    fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
    for r in grid:
        if r['camberScale']==1 and not r['reverseChord']:
            ax.plot(r['values']['CDi'],r['values']['CLtot'],'o-',label=f"AR {r['aspect']:g}")
    ax.set(xlabel='Induced drag coefficient CDi (not total drag)',ylabel='Lift coefficient CL',title='Induced-drag polars — original camber, forward chord')
    ax.legend();ax.grid(alpha=.2);save(fig,'induced-polars')
    p=next(p for p in geometry['profiles'] if p['span_station_mm']==150)
    x=np.array(p['x_mm']);u=(x-x[0])/(x[-1]-x[0]);top=-np.array(p['lower_mm']);bottom=-np.array(p['upper_mm'])
    mean=(top+bottom)/2;half=(top-bottom)/2;mean-=np.linspace(mean[0],mean[-1],len(mean))
    fig,ax=plt.subplots(figsize=(11,4),layout='constrained')
    for scale in (0,.5,1,1.5):
        line=ax.plot(u,(mean*scale+half)/p['chord_mm'],label=f'Camber ×{scale:g}')[0]
        ax.plot(u,(mean*scale-half)/p['chord_mm'],color=line.get_color())
    ax.set(xlabel='Normalized chord x/c',ylabel='Section height z/c',title='Sections supplied to OpenVSP — fixed thickness, scaled mean camber')
    ax.set_aspect('equal');ax.legend(ncol=4,loc='upper center',bbox_to_anchor=(.5,-.35));ax.grid(alpha=.2);save(fig,'sections')
    source=ROOT/'evidence/vsp-geometry'
    manifest=json.loads((source/'manifest.json').read_text())
    for name,digest in manifest['files'].items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=digest:raise ValueError('Changed geometry evidence: '+name)
        shutil.copy2(source/name,output/name)
    (output/'provenance.json').write_text(json.dumps({'source':'evidence/runs/2026-10-10-coupled','referenceMeshes':[16,32,64],'gridCases':len(grid),'gridSamples':sum(len(c['values']['Alpha']) for c in grid),'validated':False},indent=2)+'\n')
    return output

if __name__=='__main__':
    print(render(ROOT/'build/vsp-figures'))


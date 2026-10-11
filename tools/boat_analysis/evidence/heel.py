"""Publish the archived heel study without re-running VSPAERO."""
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools.boat_analysis.model.runtime import ROOT

DIRECTORY=ROOT/'evidence/runs/2026-10-11-heel'


def load():
    manifest=json.loads((DIRECTORY/'manifest.json').read_text(encoding='utf-8'))
    content=(DIRECTORY/'wing-heel-sweep.json').read_bytes()
    if hashlib.sha256(content).hexdigest()!=manifest['sha256']:
        raise ValueError('Changed archived heel study')
    return json.loads(content)


def render(output):
    data=load();out=Path(output);out.mkdir(parents=True,exist_ok=True)
    cfg=data['settings'];rows=data['cases']
    colors={-40:'#0072B2',-20:'#56B4E9',0:'#222222',20:'#E69F00',40:'#D55E00'}
    for awa in cfg['apparentWindDegrees']:
        fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
        for row in [r for r in rows if r['awa_deg']==awa]:
            for ax,key,label in zip(axes.flat,['drive_N','starboard_N','up_N','heelMoment_Nm'],['Forward force (N)','Starboard force (N)','Upward force (N)','Moment about aft axis (N m)']):
                ax.plot([p['nominalAlpha_deg'] for p in row['points']],[p[key] for p in row['points']],'o-',color=colors[row['heel_deg']],label=f"Heel {row['heel_deg']:g}°",markersize=3)
                ax.set(xlabel='Nominal upright incidence (degrees)',ylabel=label);ax.grid(alpha=.2);ax.axhline(0,color='gray',linewidth=.6)
        axes[0,0].legend(ncol=2,fontsize=9)
        fig.suptitle(f'Heel sensitivity — apparent wind {awa:g}° from bow',weight='bold',fontsize=15)
        fig.supxlabel('AR 4 · area 1 m² · wind 5 m/s · fixed mast trim per nominal incidence\nLocal alpha varies with heel; full study range −19.5° to +23.5°. No stall model.\nInviscid loads about root midchord; no water surface or boat equilibrium.',fontsize=10)
        for suffix in ('svg','png'):fig.savefig(out/f'heel-awa-{awa:g}.{suffix}',dpi=140,metadata={'Date':None} if suffix=='svg' else None)
        plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
    alpha=8
    qS=.5*cfg['airDensity']*cfg['speedMps']**2*cfg['areaM2']
    summary=[]
    for ax,awa in zip(axes,cfg['apparentWindDegrees']):
        selected=sorted([r for r in rows if r['awa_deg']==awa],key=lambda r:r['heel_deg'])
        zero=next(r for r in selected if r['heel_deg']==0)
        index=cfg['nominalAlphaDegrees'].index(alpha)
        heels=np.array([r['heel_deg'] for r in selected])
        actual=np.array([r['points'][index]['drive_N'] for r in selected])
        a=np.radians(awa)
        approximation=qS*(zero['raw']['CLi'][index]*np.cos(np.radians(heels))*np.sin(a)-zero['raw']['CDi'][index]*np.cos(a))
        ax.plot(heels,actual,'o-',label='Coupled alpha/beta solve')
        ax.plot(heels,approximation,'s--',label='Upright lift × cos(heel)')
        ax.set(title=f'Apparent wind {awa:g}°',xlabel='Heel (degrees)',ylabel='Forward inviscid force (N)');ax.grid(alpha=.2)
        summary.append({'awa_deg':awa,'nominalAlpha_deg':alpha,'heel_deg':heels.tolist(),'solvedDrive_N':actual.tolist(),'cosineProjectionDrive_N':approximation.tolist()})
    axes[0].legend(fontsize=8)
    fig.suptitle('Does the simple cosine projection reproduce the heel sweep?',weight='bold')
    fig.supxlabel('Fixed trim giving 8° incidence upright · same inviscid upright baseline for both curves',fontsize=10)
    for suffix in ('svg','png'):fig.savefig(out/f'heel-projection-comparison.{suffix}',dpi=140,metadata={'Date':None} if suffix=='svg' else None)
    plt.close(fig)
    (out/'heel-comparison.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return summary

if __name__=='__main__':print(render(ROOT/'build/vsp-figures'))

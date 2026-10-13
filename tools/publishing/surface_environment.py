"""Plot the recorded paired surface-environment replay without rerunning it."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from tools.boat_analysis.model.runtime import ROOT


def render(directory,output):
    directory=Path(directory);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for ax,length in zip(axes[0],(1.4,2.0)):
        r=json.loads((directory/f'operating-{length:.1f}.json').read_text())
        before=[v['outputs']['waterVMG'] for v in r['uniformCases']]
        after=[c['outputs']['waterVMG'] for c in r['cases']]
        x=np.arange(len(after))
        ax.bar(x-.18,before,.36,label='Re-solved controls, uniform wind',color='#93abc1')
        ax.bar(x+.18,after,.36,label='Re-solved controls, wind shear',color='#166574')
        ax.set(xticks=x,xticklabels=[f"{c['wind_m_s']:g}\n{'beat' if c['windward'] else 'run'} {'+' if c['tack']>0 else '−'}" for c in r['cases']],
               ylabel='Water-relative VMG (m/s)',title=f'{length:.1f} m hull — fixed dimensions')
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
        for i,c in enumerate(r['cases']):
            if not c['screenFeasible']:ax.text(i,after[i],'unsupported',rotation=90,fontsize=8)
    axes[0,0].legend(fontsize=8)
    colors=['#93abc1','#166574','#c97936']
    for color,name in zip(colors,('uniform-calm','shear-calm','shear-waves')):
        r=json.loads((directory/(name+'.json')).read_text())
        for i,v in enumerate(r['results']):
            y=v['index']+{'uniform-calm':-.18,'shear-calm':0,'shear-waves':.18}[name]
            axes[1,0].scatter(v['elapsed_seconds']/3600,y,c=color,marker='o' if v['outcome']=='qualified_completion' else 'x',label=name if i==0 else None)
        if name=='shear-waves':
            for v in r['results']:
                samples=v['surface_summary'].get('samples',[])
                axes[1,1].plot([s['seconds']/3600 for s in samples],[s['significantHeightM'] for s in samples],label=f"Seed {v['index']}")
    axes[1,0].set(xlabel='Elapsed voyage time (h)',ylabel='Paired scenario index',title='1.4 m missions: circle completes; × stops')
    axes[1,0].legend(fontsize=8);axes[1,0].grid(alpha=.2)
    axes[1,1].set(xlabel='Elapsed voyage time (h)',ylabel='Modeled significant height (m)',title='Wind seas and scripted wakes')
    axes[1,1].legend(fontsize=8);axes[1,1].grid(alpha=.2)
    fig.suptitle('Surface-environment sensitivity — synthetic scenarios, not qualification',fontsize=14)
    fig.savefig(output,dpi=160);plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--output',type=Path,default=ROOT/'docs/figures/surface-environment.png')
    a=p.parse_args();render(a.directory,a.output)

"""Plot prescribed-motion load sensitivity and paired contact screens."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from tools.boat_analysis.model.runtime import ROOT


def render(directory):
    record=json.loads((directory/'phase-loads.json').read_text());phases=record['results']
    missions=json.loads((directory/'missions.json').read_text())['results']
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    selected=[r for r in phases if r['responseGains']==[1,1]]
    for j,(sea,color) in enumerate(zip(('head','beam','following'),('steelblue','darkorange','seagreen'))):
        rows=[r for r in selected if r['sea']==sea]
        x=np.arange(len(rows))+(j-1)*.23
        mean=np.array([r['meanDriveN']/r['baselineDriveN'] for r in rows])
        lo=np.array([r['minDriveN']/r['baselineDriveN'] for r in rows])
        hi=np.array([r['maxDriveN']/r['baselineDriveN'] for r in rows])
        axes[0].errorbar(x,mean,yerr=[mean-lo,hi-mean],fmt='o',capsize=2,label=sea,color=color)
    axes[0].axhline(1,color='gray',lw=1)
    axes[0].set(xticks=range(8),xticklabels=['5 U+','5 U−','5 D+','5 D−','8 U+','8 U−','8 D+','8 D−'],
                ylabel='Drive / stationary-boat drive',xlabel='U10 (m/s), upwind/downwind, tack',title=f"Phase mean and range: {record['significantHeightM']} m Hs, {record['periodS']} s")
    axes[0].tick_params(axis='x',rotation=35);axes[0].legend()
    unsupported=sum(r['unsupportedPhaseCount'] for r in selected)
    total=len(selected)*int(record['policy'][2])
    axes[0].text(.02,.02,f'{unsupported}/{total} phases outside aerodynamic/profile coverage',
                 transform=axes[0].transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.85,edgecolor='none'))
    x=np.arange(len(missions))
    axes[1].bar(x-.18,[r['previousContactScreenSeconds']/3600 for r in missions],.36,label='Fixed vertical position')
    axes[1].bar(x+.18,[r['surface_summary']['contactScreenSeconds']/3600 for r in missions],.36,label='Prescribed wave following')
    axes[1].set(xticks=x,xlabel='Paired weather/traffic seed index',ylabel='Hours flagged for possible contact',title='Mission clearance screen')
    axes[1].legend();fig.suptitle('Wave motion sensitivity — imposed response, not qualified seakeeping')
    for ax in axes:ax.grid(axis='y',alpha=.2)
    output=ROOT/'docs/figures/wave-motion.png';fig.savefig(output,dpi=170);plt.close(fig)
    return output


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);print(render(p.parse_args().directory))

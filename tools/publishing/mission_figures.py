"""Render mission trajectories and energy from a source-validated campaign."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from tools.boat_analysis.evidence.records import validate, run_record, verify_run_sources
from tools.boat_analysis.model.runtime import ROOT


def render(source, destination):
    source=Path(source)
    if (source.parent/'manifest.json').exists():
        verify_run_sources(source.parent)
        report=run_record(source.parent,source.name)
    else:
        report=json.loads(source.read_text(encoding='utf-8'))
        validate(report['sourceHashes'])
    plt.rcParams.update({'svg.hashsalt':'blue-dog-mission','font.size':10})
    fig,axes=plt.subplots(3,1,figsize=(11,12),constrained_layout=True,
                          gridspec_kw={'height_ratios':[1.2,1,1]})
    records=report['results'];longest=max(records,key=lambda r:r['elapsed_seconds'])
    for record in records:
        history=np.array([row[:4] for row in record['history']],dtype=float)
        if not len(history):continue
        highlight=record is longest
        color='#ad4c21' if highlight else '#286d8c'
        axes[0].plot(history[:,1]/1000,history[:,2]/1000,color=color,
                     alpha=1 if highlight else .18,lw=1.5 if highlight else .6)
        if record['outcome'] != 'qualified_completion':
            axes[0].scatter(history[-1,1]/1000,history[-1,2]/1000,color='#a02b35',marker='x',s=28,zorder=5)
        axes[2].plot(history[:,0]/3600,history[:,3],color=color,
                     alpha=1 if highlight else .25,lw=1.5 if highlight else .7)
    axes[0].set(title='Simulated tracks between the marker-based gates',
                xlabel='East of local origin (km)',ylabel='North of local origin (km)')
    axes[0].set_aspect('equal',adjustable='datalim')
    axes[0].text(.01,.02,'Orange: longest realization; blue: others; red ×: incomplete run',
                 transform=axes[0].transAxes,fontsize=9)
    completed=[r['elapsed_seconds']/3600 for r in records if r['outcome']=='qualified_completion']
    axes[1].hist(completed,bins='auto',color='#286d8c',edgecolor='white')
    axes[1].set(title='Elapsed time among completed synthetic scenarios',xlabel='Hours',ylabel='Runs')
    summary=', '.join(f'{k.replace("_"," ")}: {v}' for k,v in report['outcomes'].items())
    axes[1].text(.98,.95,summary,ha='right',va='top',transform=axes[1].transAxes,fontsize=9)
    reserve=report['inputs']['energy'][2]
    axes[2].axhline(reserve,color='#b33636',linestyle='--',label='Configured recovery reserve')
    axes[2].set(title='Stored energy through each voyage',xlabel='Hours',ylabel='Wh')
    axes[2].legend(loc='lower right')
    for ax in axes:ax.grid(alpha=.18)
    fig.suptitle(f'Gorge mission experiment · {len(records)} seeded scenarios\nConceptual boat; uncalibrated weather and traffic hypotheses',fontsize=14)
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(destination,metadata={'Date':None},bbox_inches='tight')
    plt.close(fig)
    if destination.suffix == ".svg":
        destination.write_bytes(("\n".join(line.rstrip() for line in destination.read_text(encoding="utf-8").splitlines())+"\n").encode())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'build/analysis/mission-campaign.json')
    parser.add_argument('--output',type=Path,default=ROOT/'docs/figures/mission-campaign.svg')
    args=parser.parse_args();render(args.source,args.output)

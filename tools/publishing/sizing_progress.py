"""Plot compatible accepted sizing stages from immutable evidence."""
import argparse
from tools.boat_analysis.evidence.continuation import compatible_stages
from tools.boat_analysis.model.runtime import ROOT


def render(run,preview=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'svg.hashsalt':'blue-dog-finite-sizing','svg.fonttype':'none'})
    stages={s['lengthM']:s for s in compatible_stages(ROOT/'evidence/runs'/run) if s['feasible'] and 'concept' in s}
    rows=[stages[k] for k in sorted(stages)]
    x=[s['lengthM'] for s in rows]
    fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    series=[('Vessel mass (kg)',[s['mass']['totalMass'] for s in rows]),
            ('Nominal battery capacity (Wh)',[s['design']['battery_Wh'] for s in rows]),
            ('Full swept length (m)',[s['envelope']['sweptLengthM'] for s in rows]),
            ('No-harvest passage allowance (h)',[s['concept']['passageHours'] for s in rows])]
    for ax,(label,values) in zip(axes.ravel(),series):
        ax.plot(x,values,'o-',color='#176a65',lw=2)
        ax.set(xlabel='Hull length (m)',ylabel=label,xticks=x)
        ax.grid(alpha=.2)
    axes[1,0].plot(x,x,':',color='#777777',label='Hull length')
    axes[1,0].legend(frameon=False)
    fig.suptitle('Finite-passage sizing: accepted coarse stages',fontsize=15)
    output=ROOT/'docs/figures/finite-passage-sizing.svg'
    fig.savefig(output,metadata={'Date':None,'Description':f'Generated from {run}; nominal coarse screens, not physical qualification.'})
    output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines())+'\n')
    if preview:fig.savefig(ROOT/'.tools/finite-passage-sizing.png',dpi=130)
    plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',default='2026-10-12-finite-passage');p.add_argument('--preview',action='store_true')
    args=p.parse_args();render(args.run,args.preview)

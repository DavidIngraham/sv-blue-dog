"""Render archived hydrodynamic response and wave-aware sailing results."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools.boat_analysis.model.runtime import ROOT


def response(record,period,speed,direction):
    row=next(r for r in record['rows'] if r['period']==period and r['speed']==speed and r['direction']==direction)
    M=np.array(record['metadata']['massMatrix']);K=np.array(record['metadata']['stiffness'])
    damping=2*record['policy']['settings'][4]*np.sqrt(np.diag(M)*np.diag(K))
    w=2*np.pi/period;k=w*w/9.80665;encounter=w-k*speed*np.cos(np.deg2rad(direction))
    Z=K-encounter**2*(M+np.array(row['addedMass']))-1j*encounter*(np.array(row['damping'])+np.diag(damping))
    return np.linalg.solve(Z,np.array(row['forceReal'])+1j*np.array(row['forceImag']))


def render(directory):
    bem=json.loads((directory/'bem-refined.json').read_text());operating=json.loads((directory/'operating.json').read_text())
    mesh=json.loads((directory/'mesh-check.json').read_text())['cases']
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    periods=bem['policy']['periods'];speed=1.5
    for direction,label in [(0,'Following'),(90,'Beam'),(180,'Head')]:
        values=np.array([response(bem,t,speed,direction) for t in periods])
        for j,ax in enumerate(axes.flat[:3]):
            ax.plot(periods,np.abs(values[:,j]),'o-',label=label)
            rejected=[i for i,t in enumerate(periods) if next(r['relativeResponseError'] for r in mesh if r['period']==t and r['speed']==speed and r['direction']==direction)>bem['policy']['settings'][8]]
            if rejected:ax.scatter(np.array(periods)[rejected],np.abs(values[rejected,j]),marker='x',color='red',s=90,zorder=4)
    for ax,title,unit in zip(axes.flat[:3],('Heave','Roll','Pitch'),('m/m','rad/m','rad/m')):
        ax.set(title=title+' response at 1.5 m/s',xlabel='Wave period (s)',ylabel='Response / wave amplitude ('+unit+')')
        ax.grid(alpha=.2);ax.legend()
    ax=axes[1,1]
    for direction,color in zip((0,90,180,270),('steelblue','darkorange','seagreen','purple')):
        rows=[r for r in operating['cases'] if r['waveWindAngleDeg']==direction]
        for i,row in enumerate(rows):
            baseline=next(r for r in operating['baseline'] if r['wind_m_s']==row['wind_m_s'] and r['windward']==row['windward'] and r['tack']==row['tack'])
            ratio=row['outputs']['waterVMG']/baseline['outputs']['waterVMG']
            ax.scatter(i+(direction/90-1.5)*.15,ratio,marker='o' if row['numericalSupport'] else 'x',color=color,label=str(direction)+'°' if i==0 else None)
    ax.axhline(1,color='gray',lw=1);ax.set(xticks=range(8),xticklabels=['5 U+','5 U−','5 D+','5 D−','8 U+','8 U−','8 D+','8 D−'],ylabel='Wave VMG / calm VMG',xlabel='U10 (m/s), U/D = up/downwind, +/− = tack',title='4 cm regular waves, 3 s; × = unsupported')
    ax.tick_params(axis='x',rotation=35);ax.legend(title='Wave direction from wind-from axis',fontsize=8,loc='lower right');ax.grid(alpha=.2)
    fig.suptitle('Fixed 1.4 m candidate: wave response and sailing\nRed × on response curves = mesh check outside tolerance')
    out=ROOT/'docs/figures/wave-performance.png';fig.savefig(out,dpi=170);plt.close(fig)
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path);print(render(parser.parse_args().directory))

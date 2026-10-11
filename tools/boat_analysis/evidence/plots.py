"""Plot the current static recovery evidence without implying dynamic stability."""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import validate


def render(preview=False):
    data=input_record('coupled-recovery.json')
    plt.rcParams.update({'font.size':10,'svg.hashsalt':'blue-dog-coupled-recovery','svg.fonttype':'none'})
    fig,axes=plt.subplots(3,1,figsize=(10,10),sharex=True,layout='constrained')
    states=[('sealed','Sealed wing'),('free_flooding_homogenized','Freely flooded wing — homogenized buoyancy'),('full_water_retention','Wing retaining its full void volume of water')]
    colors={0.:'#0072B2',90.:'#E69F00',180.:'#009E73',270.:'#CC79A7'}
    for ax,(state,title) in zip(axes,states):
        for case in [c for c in data['cases'] if c['wing_state']==state]:
            points=case['points'];heel=np.array([p['heel_deg'] for p in points])
            restoring=np.array([np.nan if 'failure' in p else p['righting_Nm']*np.sign(p['heel_deg']) for p in points])
            # At zero roll the directional restoring metric is undefined.
            restoring[heel==0]=np.nan
            fresh=case['density_kg_m3']==1000
            color=colors[case['mast_trim_deg']]
            ax.plot(heel,restoring,color=color,linestyle='-' if fresh else '--',linewidth=1.3,label=f"Mast {case['mast_trim_deg']:g}°" if fresh else None)
            unstable=np.array(['failure' not in p and not p['pitch_stable'] for p in points])
            ax.scatter(heel[unstable],restoring[unstable],s=10,color=color,marker='x',alpha=.7)
            missing=np.array(['failure' in p for p in points])
            ax.scatter(heel[missing],np.zeros(missing.sum()),s=40,color=color,marker='v',zorder=4)
        ax.axhline(0,color='#333333',linewidth=.8)
        ax.set_title(title,loc='left',fontweight='bold')
        ax.set_ylabel('Signed restoring moment (N m)')
        ax.grid(alpha=.18);ax.set_xlim(-180,180);ax.set_xticks(np.arange(-180,181,45))
    axes[0].legend(ncol=2,loc='upper center',frameon=False)
    axes[-1].set_xlabel('Prescribed roll angle (degrees)')
    fig.suptitle(f"Static recovery sensitivity — {data['design']['length_m']:.3f} m analysis candidate",fontsize=15,fontweight='bold')
    fig.supxlabel('Positive values oppose roll. Solid: freshwater; dashed: seawater. ×: pitch-unstable; ▼: missing pitch root.\nSelected equilibrium branches may jump; no wave dynamics, drainage, slosh or recovery trajectory.',fontsize=10)
    out=ROOT/'docs/figures/coupled-recovery.svg'
    fig.savefig(out,metadata={'Date':None,'Description':'Generated from build/analysis/coupled-recovery.json; static sensitivity, not recovery qualification.'})
    if preview:fig.savefig(ROOT/'.tools/coupled-recovery-preview.png',dpi=130)
    plt.close(fig)


if __name__=='__main__':render(preview=True)

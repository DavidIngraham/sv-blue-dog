"""Plot saved fixed-design polar coverage without joining across failed points."""
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .study_mission_sizing import read_report


def figure():
    report=read_report()
    fig,axes=plt.subplots(1,2,subplot_kw={'projection':'polar'},figsize=(11,6))
    for ax,(name,study) in zip(axes,report['studies'].items(),strict=True):
        for wind in sorted({p['wind'] for p in study['polar']}):
            points=[p for p in study['polar'] if p['wind']==wind]
            ax.plot(np.deg2rad([p['angle'] for p in points]),
                    [p['speed'] if p['valid'] else np.nan for p in points],
                    marker='o',markersize=3,label=f'{wind:g} m/s')
        ax.set_theta_zero_location('N');ax.set_theta_direction(-1)
        ax.set_thetamin(0);ax.set_thetamax(180)
        ax.set_ylim(0,4.5);ax.set_title(name.replace('_',' ').title(),pad=20)
        ax.set_rlabel_position(90);ax.grid(alpha=.4)
    axes[1].legend(title='Water-relative wind',loc='upper left',bbox_to_anchor=(1.05,1))
    fig.suptitle('2 m waterline — predicted boat speed (m/s)',fontsize=14)
    fig.text(.5,.04,'Clean water; gaps indicate unsolved or constraint-violating points, not zero speed.\nPreliminary physics; these curves do not establish survival or capsize recovery.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.03,right=.83,bottom=.15,top=.86,wspace=.2)
    data=BytesIO();fig.savefig(data,format='png',dpi=160);plt.close(fig)
    return data.getvalue()

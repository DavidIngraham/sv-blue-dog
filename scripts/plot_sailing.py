"""Plot native sailing-analysis outputs; no sailing equations are implemented here."""
from io import BytesIO
import json
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


NUMBER = r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'


def quantities(text):
    return [float(x) for x in re.findall(r'(' + NUMBER + r') \[', text)]


def sailing_figures(report):
    report = json.loads(report)
    case = next(c for c in report['checks'] if c['subject'] == 'BlueDogSailing::SailingSensitivity')
    if case['status'] != 'holds':
        raise ValueError('Cannot publish a failed sensitivity study')
    values = {v['name']: v['value'] for v in case['values']}
    figures = {}
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})

    fig, ax = plt.subplots(figsize=(8, 7), subplot_kw={'projection': 'polar'})
    for angles, speeds, color, label in [
        ('beatAngles', 'beatSpeeds', '#176a9b', 'Upwind route demand'),
        ('runAngles', 'runSpeeds', '#a45a17', 'Downwind route demand'),
    ]:
        theta = np.deg2rad(json.loads(values[angles]))
        speed = quantities(values[speeds])
        if len(theta) != len(speed):
            raise ValueError('Native angle and speed arrays differ in length')
        ax.plot(theta, speed, color=color, linewidth=2.5, label=label)
        ax.plot(-theta, speed, color=color, linewidth=2.5)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(90)
    ax.set_title('Required clean polar speed (m/s)\nDemand boundary, not predicted boat performance', pad=25)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)
    fig.text(0.5, 0.02, f"Along-current {quantities(values['alongCurrent'])[0]:g} m/s; ground target {quantities(values['groundTarget'])[0]:g} m/s; retention {values['retainedPerformance']} × {values['maneuverRetention']}.\n"
             'Zero leeway; symmetric tacks/gybes. Shown angles are a sweep, not proven sailable angles.', ha='center', fontsize=9)
    fig.subplots_adjust(top=0.82, bottom=0.22)
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=180, metadata={'Software': 'SV Blue Dog — native SysML results'})
    figures['required-polar.png'] = buffer.getvalue()
    plt.close(fig)

    lengths, speeds = quantities(values['waterlines']), quantities(values['waveSpeeds'])
    if len(lengths) != len(speeds):
        raise ValueError('Native length and speed arrays differ in length')
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(lengths, speeds, color='#176a9b', linewidth=2.5, label='Deep-water wave speed at wavelength = LWL')
    ax.axhline(quantities(values['cleanDemand'])[0], color='#a45a17', linewidth=2, label=f"Required clean polar speed: {quantities(values['cleanDemand'])[0]:.2f} m/s — {float(values['referenceTwaDegrees']):g}° reference case")
    ax.axhline(quantities(values['operatingDemand'])[0], color='#a45a17', linestyle='--', linewidth=2, label=f"Required operating speed: {quantities(values['operatingDemand'])[0]:.2f} m/s after retention {values['retainedPerformance']}")
    ax.set(xlabel='Assembled vessel waterline length (m)', ylabel='Water-relative boat speed (m/s)',
           title='Hull-speed reference versus mission demand', xlim=(min(lengths), max(lengths)), ylim=(0, 4.3))
    ax.grid(alpha=0.2)
    ax.legend(loc='lower right', frameon=False, fontsize=9)
    fig.text(0.5, 0.015, 'The reference is neither a maximum speed nor a planing threshold. No hull-resistance or lift prediction is made.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=180, metadata={'Software': 'SV Blue Dog — native SysML results'})
    figures['hull-speed-screen.png'] = buffer.getvalue()
    plt.close(fig)
    return figures

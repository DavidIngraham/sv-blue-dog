"""Render representative VSPAERO numerical sensitivity from immutable records."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .records import AERODYNAMIC_REFERENCE, run_record


def render(output):
    record = run_record(AERODYNAMIC_REFERENCE, 'wing-convergence.json')
    fig, axes = plt.subplots(3, 3, figsize=(13, 10), layout='constrained')
    for row, (reverse, beta, title) in enumerate([(False, 0, 'Forward'), (True, 0, 'Reversed chord'), (False, 20, 'Forward, beta 20°')]):
        selected = [c for c in record['cases'] if c['reverseChord'] == reverse and c['beta_deg'] == beta]
        for case in selected:
            for column, (key, label) in enumerate([('CLtot', 'Lift CL'), ('CDi', 'Induced drag CDi'), ('CMytot', 'Pitching moment CMy')]):
                ax = axes[row, column]
                ax.plot(case['values']['Alpha'], case['values'][key], 'o-', markersize=3,
                        label=f"Mesh {case['mesh']}, wake {case['wakeIterations']}")
                ax.set(xlabel='Solver alpha (degrees)', ylabel=label, title=title)
                ax.grid(alpha=.2)
        for column, key in enumerate(['CLtot', 'CDi', 'CMytot']):
            comparisons = [c for c in record['comparisons'] if c['reverseChord'] == reverse and c['beta_deg'] == beta]
            text = '\n'.join(f"{c['comparison']} Δmax {c['maxAbsoluteDifference'][key]:.3g}" for c in comparisons)
            axes[row, column].text(.03, .97, text, transform=axes[row, column].transAxes, va='top', fontsize=8,
                                   bbox={'facecolor': 'white', 'alpha': .8, 'edgecolor': 'none'})
    axes[0, 0].legend(fontsize=7, loc='lower right')
    fig.suptitle('Representative mesh and wake sensitivity', fontsize=16, weight='bold')
    fig.supxlabel('AR 4 · original camber · 5 m/s · inviscid attached-flow model\nLast increments: wake 15→30 at mesh 24; mesh 48→72 at wake 30.', fontsize=10)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ('svg', 'png'):
        fig.savefig(output / f'convergence.{suffix}', dpi=140, metadata={'Date': None} if suffix == 'svg' else None)
    plt.close(fig)
    candidate = run_record(AERODYNAMIC_REFERENCE, 'wing-candidate-check.json')
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.5), layout='constrained')
    for row, case in enumerate(candidate['cases']):
        for column, (key, label) in enumerate([('CLtot', 'Lift CL'), ('CDi', 'Induced drag CDi'), ('CMytot', 'Pitching moment CMy')]):
            ax = axes[row, column]
            ax.plot(case['values']['Alpha'], case['values'][key], 'o-', label='Direct VSPAERO', markersize=4)
            ax.plot(case['values']['Alpha'], case['interpolated'][key], 'x--', label='Grid interpolation', markersize=5)
            ax.set(xlabel='Solver alpha (degrees)', ylabel=label, title='Reversed chord' if case['reverseChord'] else 'Forward chord')
            ax.grid(alpha=.2)
            ax.text(.03, .97, f"Max absolute difference {case['maxAbsoluteInterpolationError'][key]:.3g}", transform=ax.transAxes, va='top', fontsize=8)
    axes[0, 0].legend(fontsize=8, loc='lower right')
    design = candidate['design']
    fig.suptitle('Interpolation check at an off-grid reference geometry', fontsize=16, weight='bold')
    fig.supxlabel(f"AR {design['sail_AR']:.3f} · camber scale {design['camber_scale']:.3f} · mesh 24 · wake 5\nReference section thickness · wing area 1 m²", fontsize=10)
    for suffix in ('svg', 'png'):
        fig.savefig(output / f'candidate-interpolation.{suffix}', dpi=140, metadata={'Date': None} if suffix == 'svg' else None)
    plt.close(fig)
    return record['comparisons']

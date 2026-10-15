"""Render standard technical-risk metadata without assigning missing assessments."""
from fractions import Fraction
from math import ceil, isfinite
from collections import defaultdict
import json
from tools.boat_analysis.model.runtime import ROOT, native, model_files


def coordinate(value):
    if not value.strip():
        return None
    number = float(Fraction(value))
    if not isfinite(number) or not 0 <= number <= 1:
        raise ValueError(f'Risk coordinate outside [0, 1]: {value}')
    return number


def read_rows():
    report = native('-render-document', 'BlueDogRiskPlot::Data',
                    models=(*model_files(), ROOT/'tools/publishing/reference.sysml'))
    rows = []
    for line in report.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 4 and cells[0].startswith('R-'):
            identifier, area, probability, impact = cells
            rows.append(dict(identifier=identifier, area=area,
                             probability=coordinate(probability), impact=coordinate(impact)))
    if not rows or len({r['identifier'] for r in rows}) != len(rows):
        raise ValueError('Risk export must contain distinct identified risks')
    return rows


def cell(value):
    return max(0, ceil(value * 5) - 1)


def render(directory, rows=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from textwrap import fill
    rows = read_rows() if rows is None else rows
    directory.mkdir(parents=True, exist_ok=True)
    assessed, unassessed = defaultdict(list), []
    for row in rows:
        p, i = row['probability'], row['impact']
        if p is None or i is None:
            unassessed.append(row)
        else:
            coordinate(str(p)); coordinate(str(i))
            assessed[cell(i), cell(p)].append(row['identifier'])
    with plt.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'blue-dog-risk-cube'}):
        fig, (ax, side) = plt.subplots(1, 2, figsize=(11, 6), gridspec_kw={'width_ratios': [1.5, 1]}, layout='constrained')
        fig.suptitle('Development risk assessment', fontsize=19, fontweight='bold')
        for x in range(5):
            for y in range(5):
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor='#edf2f7', edgecolor='white', linewidth=2))
                if assessed[x, y]:
                    ax.text(x+.5, y+.5, fill(', '.join(assessed[x, y]), 15), ha='center', va='center', fontsize=10, color='#133e64', fontweight='bold')
        ax.set(xlim=(0,5), ylim=(0,5), aspect='equal', xlabel='Consequence / normalized impact →', ylabel='Likelihood / probability →')
        labels=['0–.2','>.2–.4','>.4–.6','>.6–.8','>.8–1']
        ax.set_xticks([.5,1.5,2.5,3.5,4.5], labels)
        ax.set_yticks([.5,1.5,2.5,3.5,4.5], labels)
        ax.tick_params(length=0, labelsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        side.axis('off')
        side.text(0, .98, f'Unassessed · {len(unassessed)}', fontsize=16, fontweight='bold', va='top', color='#133e64')
        items=[f"{r['identifier']}  {r['area'].capitalize()}" for r in unassessed]
        side.text(0, .86, '\n\n'.join(items) if items else 'All risks have coordinates.', fontsize=12, va='top')
        side.text(0, .20, 'Missing likelihood or consequence\nstays outside the cube.\nUnknown does not mean low risk.', fontsize=10, va='top', color='#44566a')
        side.text(0, .06, f'{sum(len(v) for v in assessed.values())} assessed · {len(rows)} total\nNeutral cells: no acceptance policy assigned.', fontsize=10, va='top', color='#44566a')
        fig.savefig(directory/'cube.svg', metadata={'Date':None, 'Description':'Technical risk likelihood and consequence from SysML. Unassessed risks are listed separately.'})
        fig.savefig(directory/'cube.png', dpi=140)
        plt.close(fig)
    (directory/'data.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    return directory/'cube.svg'


if __name__ == '__main__':
    print(render(ROOT/'build/risk-preview'))

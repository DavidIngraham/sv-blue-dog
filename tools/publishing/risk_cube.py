"""Render ordinal development judgments separately from quantitative risk fields."""
from collections import defaultdict
import json
from tools.boat_analysis.model.runtime import ROOT, native, model_files

LIKELIHOOD = ('Remote', 'Unlikely', 'Possible', 'Likely', 'Demonstrated')
CONSEQUENCE = ('Negligible', 'Minor', 'Moderate', 'Major', 'Critical')


def coordinate(value, labels):
    value = value.strip()
    if not value:
        return None
    if value not in labels:
        raise ValueError(f'Unknown qualitative risk class: {value}')
    return labels.index(value)


def read_rows():
    report = native('-render-document', 'BlueDogRiskPlot::Data',
                    models=(*model_files(), ROOT/'tools/publishing/reference.sysml'))
    rows = []
    for line in report.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 5 and cells[0].startswith('R-'):
            identifier, kind, area, likelihood, consequence = cells
            if not kind or not kind.isascii() or not kind.replace("-", "").isalpha():
                raise ValueError(f"Invalid risk kind: {kind!r}")
            coordinate(likelihood, LIKELIHOOD)
            coordinate(consequence, CONSEQUENCE)
            rows.append(dict(identifier=identifier, kind=kind, area=area,
                             likelihood=likelihood, consequence=consequence))
    if not rows or len({r['identifier'] for r in rows}) != len(rows):
        raise ValueError('Risk export must contain distinct identified risks')
    return rows


def render(directory, rows=None, *, kind="technical"):
    """Render one risk kind; never mix categories on a cube."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from textwrap import fill
    rows = read_rows() if rows is None else rows
    rows = [row for row in rows if row["kind"] == kind]
    directory.mkdir(parents=True, exist_ok=True)
    assessed, unassessed = defaultdict(list), []
    for row in rows:
        likelihood = coordinate(row['likelihood'], LIKELIHOOD)
        consequence = coordinate(row['consequence'], CONSEQUENCE)
        if likelihood is None or consequence is None:
            unassessed.append(row)
        else:
            assessed[consequence, likelihood].append(row['identifier'])
    with plt.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'blue-dog-risk-cube'}):
        fig, (ax, side) = plt.subplots(1, 2, figsize=(12, 6.5), gridspec_kw={'width_ratios': [1.6, 1]}, layout='constrained')
        fig.suptitle(f'{kind.capitalize()} risk assessment', fontsize=19, fontweight='bold')
        for x in range(5):
            for y in range(5):
                present = assessed[x, y]
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor='#d6e7f4' if present else '#edf2f7', edgecolor='white', linewidth=2))
                if present:
                    ax.text(x+.5, y+.5, fill(', '.join(present), 15), ha='center', va='center', fontsize=10, color='#133e64', fontweight='bold')
        ax.set(xlim=(0,5), ylim=(0,5), aspect='equal', xlabel='Consequence if unresolved →', ylabel='Prospect of redesign or scope restriction →')
        ax.set_xticks([.5,1.5,2.5,3.5,4.5], CONSEQUENCE)
        ax.set_yticks([.5,1.5,2.5,3.5,4.5], LIKELIHOOD)
        ax.tick_params(length=0, labelsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        side.axis('off')
        side.text(0, .98, f'Assessed {kind} risks', fontsize=15, fontweight='bold', va='top', color='#133e64')
        side.text(0, .88, '\n\n'.join(f"{r['identifier']}  {r['area'].capitalize()}" for r in rows), fontsize=12, va='top')
        unknown = ', '.join(r['identifier'] for r in unassessed) or 'None'
        side.text(0, .32, fill('Unassessed: '+unknown, 39), fontsize=10, va='top', color='#44566a')
        side.text(0, .22, 'Qualitative engineering judgments.\nDemonstrated = a current limitation\nalready restricts the conclusion.\nNot probabilities of accidents.', fontsize=10, va='top', color='#44566a')
        side.text(0, .07, f'{sum(len(v) for v in assessed.values())} assessed · {len(rows)} total\nNo residual-risk acceptance implied.', fontsize=10, va='top', color='#44566a')
        fig.savefig(directory/'cube.svg', metadata={'Date':None, 'Description':'Ordinal development risk judgments from SysML; not measured incident probabilities. Unassessed entries remain outside the grid.'})
        fig.savefig(directory/'cube.png', dpi=140)
        plt.close(fig)
    (directory/'data.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    return directory/'cube.svg'


def render_all(directory, rows=None):
    """Publish a separate asset directory for every recorded risk kind."""
    rows = read_rows() if rows is None else rows
    paths = {kind: render(directory / kind, rows, kind=kind)
             for kind in sorted({row['kind'] for row in rows})}
    # Preserve the existing asset URL as an explicitly technical-only view.
    if 'technical' in paths:
        render(directory, rows, kind='technical')
    return paths


if __name__ == '__main__':
    print(render(ROOT/'build/risk-preview'))

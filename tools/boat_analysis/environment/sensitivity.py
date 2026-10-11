"""Plot native persistent-regime sensitivity of the archived candidate.

This reinterprets existing evidence; it does not rerun the optimizer or qualify it.
"""
import json

from tools.boat_analysis.model.runtime import ROOT, native, native_value
from tools.boat_analysis.evidence.records import source_hashes


def run():
    names = ['primary', 'construction', 'aerodynamic', 'hydrodynamic', 'energy', 'combined']
    arguments = [item for name in names for item in ('-analysis', 'BlueDogWeather::'+name)]
    report = json.loads(native(*arguments, '-json'))
    rows = [{v['name']: native_value(v['value']) for v in check['values']} for check in report['checks']]
    if len(rows) != len(names):
        raise ValueError('Incomplete native weather assessment')
    record = dict(zip(names, rows))
    output = ROOT/'build/analysis/weather-sensitivity.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'sourceHashes':source_hashes(['tools/boat_analysis/environment/sensitivity.py']),
                                 'scope':__doc__, 'scenarios':record}, indent=2)+'\n', encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt'] = 'blue-dog-weather'
    fig, axes = plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
    for name, row in record.items():
        axes[0].plot(row['probabilities'], row['coverage'], label=name, linestyle=['-', '--', ':', '-.', '--', ':'][names.index(name)], linewidth=2)
        times = [t if p > 0 else float('nan') for t,p in zip(row['conditionalHours'],row['coverage'])]
        axes[1].plot(row['probabilities'], times, label=name)
        print(name, 'west/east route screen:', row['westPass'], row['eastPass'])
    axes[0].set(ylabel='Passing route-screen probability', ylim=(-.03,1.03))
    axes[1].set(ylabel='Hours, conditional on passing route screen')
    for ax in axes:
        ax.set(xlabel='Assumed full-passage easterly probability', xlim=(0,1))
        ax.grid(alpha=.2)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='outside lower center',ncol=3,frameon=False)
    fig.suptitle('Fixed candidate: probability sensitivity, not a weather forecast\nMechanical handling and self-righting failures remain unresolved')
    path = ROOT/'docs/figures/weather-performance-sensitivity.svg'
    fig.savefig(path, metadata={'Date': None})
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    plt.close(fig)


if __name__ == '__main__':
    run()

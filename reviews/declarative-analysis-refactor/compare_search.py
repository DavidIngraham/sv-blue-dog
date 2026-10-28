"""Evaluate the baseline and discovered search layouts on identical real inputs."""
import json
import subprocess
import numpy as np
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.optimization.search import Problem

source = subprocess.check_output(['git', 'show', '9c8878f:tools/boat_analysis/optimization/search.py'], cwd=ROOT, text=True)
namespace = {'__name__': 'blue_dog_search_baseline', '__file__': str(ROOT/'tools/boat_analysis/optimization/search.py')}
exec(compile(source, namespace['__file__'], 'exec'), namespace)
old = namespace['Problem']()
new = Problem()
comparisons = {}
def compare(label, left, right):
    a, b = np.asarray(left), np.asarray(right)
    np.testing.assert_allclose(a, b, rtol=1e-13, atol=1e-12)
    comparisons[label] = dict(shape=list(a.shape), maximumAbsoluteDifference=float(np.max(np.abs(a-b))) if a.size else 0)
for name in ('lo', 'hi', 'span'):
    compare(name, getattr(old, name), getattr(new, name))
z_old, z_new = old.initial(), new.initial()
compare('initial', z_old, z_new)
left, right = old.evaluate(z_old), new.evaluate(z_new)
for name in ('eq', 'ineq', 'design', 'states', 'route', 'westerlyRoute', 'righting'):
    compare(name, left[name], right[name])
assert old.constraint_names == new.constraint_names
for row_index, (a, b) in enumerate(zip(left['rows'], right['rows'], strict=True)):
    assert a.keys() == b.keys()
    for key in a:
        if isinstance(a[key], (int, float)):
            compare(f'operating.{row_index}.{key}', a[key], b[key])
        else:
            assert a[key] == b[key], (row_index, key)
report = dict(baseline='9c8878f', rtol=1e-13, atol=1e-12,
    comparisons=comparisons, constraints=len(new.constraint_names),
    designFields=new.design_count, freeStateFields=new.state_count, operatingCases=new.case_count,
    interpretation='Single real shared-design evaluation and initialization; not optimizer convergence or physical validation.')
(ROOT/'.tools/search-comparison.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
print(json.dumps({**{k: v for k, v in report.items() if k != 'comparisons'}, 'maximumAbsoluteDifference': max(x['maximumAbsoluteDifference'] for x in comparisons.values())}, indent=2))

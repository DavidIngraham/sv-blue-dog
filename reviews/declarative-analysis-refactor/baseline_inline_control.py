"""Reproduce the unchanged inline-view assertion from the preserved baseline."""
from pathlib import Path
import json
import subprocess
import tempfile
import traceback

from tools.boat_analysis.model.runtime import ROOT

baseline = '9c8878f'
paths = ['docs/methods/modeling.md', 'tests/test_inline_views.py',
         'tools/boat_analysis/model/runtime.py', 'tools/boat_analysis/model/install.py']
paths += [str(p.relative_to(ROOT)) for p in (ROOT/'models').rglob('*.sysml')]
paths += [str(p.relative_to(ROOT)) for p in (ROOT/'tools/publishing').rglob('*.py')]
for name in paths:
    old = subprocess.check_output(['git', 'show', f'{baseline}:{name}'], cwd=ROOT)
    current = (ROOT/name).read_bytes()
    assert old.replace(b'\r\n', b'\n') == current.replace(b'\r\n', b'\n'), name
source = subprocess.check_output(['git', 'show', f'{baseline}:tests/test_inline_views.py'], cwd=ROOT, text=True)
namespace = {'__name__': 'baseline_inline_control', '__file__': str(ROOT/'tests/test_inline_views.py')}
exec(compile(source, namespace['__file__'], 'exec'), namespace)
with tempfile.TemporaryDirectory() as directory:
    try:
        namespace['test_inline_view_resolves_actual_refinement_and_statements'](Path(directory))
    except AssertionError:
        result = dict(baseline=baseline, outcome='same baseline assertion fails',
                      byteVerifiedInputs=paths, traceback=traceback.format_exc(),
                      scope='Baseline test implementation, authored page, model files and publishing/runtime sources match; no model or publishing change belongs to this refactor.')
    else:
        raise AssertionError('Baseline control passed; cannot classify the full-suite failure as unchanged')
(ROOT/'reviews/declarative-analysis-refactor/baseline-inline-control.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({key: value for key, value in result.items() if key != 'byteVerifiedInputs'}, indent=2))

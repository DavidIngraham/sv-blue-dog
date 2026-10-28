"""Export the native sizing input contract for the browser design explorer.

No engineering acceptance is inferred here. Defaults, brackets and the wing
section are exported from the same contracts used by the Python sizing model.
"""
import argparse
import json
import re
import numpy as np
import subprocess
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.generated import Design, Parameters
from tools.boat_analysis.evidence.records import validate, run_record
from tools.boat_analysis.geometry.vessel import section_data


def render(output):
    mass = json.loads((ROOT/'.tools/coupled-contract.json').read_text())
    operation = json.loads((ROOT/'.tools/coupled-operation-contract.json').read_text())
    validate(mass['sourceHashes']); validate(operation['sourceHashes'])
    candidate = run_record(ROOT/'evidence/runs/2026-10-15-integrated-candidate', 'integrated-sizing.json')
    design = Design.from_mapping(candidate['design']).to_mapping()
    assumptions = Parameters.from_mapping(candidate['replay']['parameters'])
    text = (ROOT/'models/blue-dog.sysml').read_text()
    materials = re.search(r'out attribute materialValues.*?= \((.*?)\);', text, re.S)[1]
    material_names = re.findall(r'material\.(\w+)', materials)
    if len(material_names) != len(mass['materialValues']):
        raise ValueError('Material input names and values differ')
    u, mean, half = section_data()
    sample = np.linspace(0, 1, 41)
    mean, half = np.interp(sample, u, mean), np.interp(sample, u, half)
    u = sample
    fields = []
    for i, name in enumerate(mass['designNames']):
        fields.append(dict(name=name, kind='design', value=design[name],
                           minimum=operation['designLower'][i], maximum=operation['designUpper'][i]))
    for kind, names, values in [('parameters', mass['parameterNames'], [assumptions.to_mapping()[n] for n in mass['parameterNames']]),
                                ('materials', material_names, mass['materialValues'])]:
        fields.extend(dict(name=n, kind=kind, value=v) for n,v in zip(names, values, strict=True))
    record = dict(version=1, revision=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                  baseline='2026-10-15-integrated-candidate / IC-01; illustrative wing geometry, rig selection open',
                  fields=fields, wingSection=dict(u=u.tolist(), mean=mean.tolist(), half=half.tolist()),
                  solverInputs={k:v for k,v in operation.items() if not k.endswith('Hash') and k!='sourceHashes'},
                  sourceHashes={**mass['sourceHashes'], **operation['sourceHashes']})
    output=Path(output); output.mkdir(parents=True, exist_ok=True)
    (output/'design.json').write_text(json.dumps(record, indent=2)+'\n')
    return record

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=ROOT/'build/design-explorer')
    render(p.parse_args().output)

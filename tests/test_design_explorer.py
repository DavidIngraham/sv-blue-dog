"""Browser export must preserve all native sizing inputs and search brackets."""
import json
import numpy as np
from tools.publishing.design_explorer import render
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.geometry.vessel import wing_section


def test_native_contract_export(tmp_path):
    data=render(tmp_path)
    mass=json.loads((ROOT/'.tools/coupled-contract.json').read_text())
    operation=json.loads((ROOT/'.tools/coupled-operation-contract.json').read_text())
    fields=data['fields']
    assert len(fields)==80
    design=[f for f in fields if f['kind']=='design']
    assert [f['name'] for f in design]==mass['designNames']
    assert [f['minimum'] for f in design]==operation['designLower']
    assert [f['maximum'] for f in design]==operation['designUpper']
    assert [f['value'] for f in fields if f['kind']=='parameters']==mass['parameterValues']
    assert [f['value'] for f in fields if f['kind']=='materials']==mass['materialValues']
    for camber, thickness in [(0.5,0.5),(1,1),(1.5,2)]:
        upper,lower=wing_section(camber,thickness)
        mean=np.array(data['wingSection']['mean'])*camber
        half=np.array(data['wingSection']['half'])*thickness
        np.testing.assert_allclose(upper[:,1],mean+half)
        np.testing.assert_allclose(lower[:,1],mean-half)
    assert json.loads((tmp_path/'design.json').read_text())==data

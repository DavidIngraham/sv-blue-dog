"""Native replay and isolation of a length-only design-space experiment."""
import json
from types import SimpleNamespace

import numpy as np
import pytest

from scripts.prepare_design_search import native_value
from scripts.render_requirements import MODELS, native
from scripts.study_hull_length import STUDY_MODEL, RESULT_MODEL, read_report, problem_for, subjects, solve


def test_length_domain_comes_from_native_mass_bound():
    report=read_report()
    output=json.loads(native('-analysis','BlueDogHullLengthStudy::LengthInputs','-json',models=MODELS+(STUDY_MODEL,)))
    assert output['status']=='holds' and not output['diagnostics']
    actual={v['name']:native_value(v['value']) for v in output['checks'][0]['values']}
    assert actual['massImpliedLengthCeiling']==pytest.approx(31.25)
    assert actual['relaxedUpper'][1:]==report['contract']['upper'][1:]
    assert actual['relaxedUpper'][0]>report['contract']['upper'][0]
    assert actual['sweepLengths']==report['contract']['sweepLengths']


def test_fixed_length_is_constant_for_every_normalized_coordinate():
    contract=read_report()['contract']
    seen=[]
    def evaluate(design,scenario):
        seen.append(design.copy())
        return np.zeros(len(contract['outputNames']))
    kernel=SimpleNamespace(contract=contract,evaluate=evaluate)
    problem=problem_for(kernel,[2,3],8)
    for value in [0,.3,1]:
        problem.evaluate(np.full(problem.lower.size,value))
    assert all(d[0]==8 for d in seen)
    assert problem.upper[1:13].tolist()==contract['upper'][1:]
    assert problem.lower[1:13].tolist()==contract['lower'][1:]


def test_native_replay_of_every_selected_length_case():
    report=read_report()
    arguments=[]
    for name in report['studies']:
        arguments.extend(('-analysis',f'BlueDogHullLengthResults::{name}Audit'))
    output=json.loads(native(*arguments,'-json',models=MODELS+(STUDY_MODEL,RESULT_MODEL)))
    assert not output['diagnostics'] and output['status']=='holds'
    for (name,study),check in zip(report['studies'].items(),output['checks'],strict=True):
        actual={v['name']:v['value'] for v in check['values']}
        best=study['best']
        expected=[[row[k] for k in report['contract']['outputNames']] for row in best['results']]
        np.testing.assert_allclose(np.asarray(native_value(actual['rows'])).reshape(np.shape(expected)),expected,rtol=1e-10,atol=1e-8)
        assert actual['boundsValid']==actual['operatingFeasible']=='true'
        assert actual['numericalFeasible']==actual['supportedDesign']=='false'
        assert float(actual['waterlineLength'])==pytest.approx(best['design']['lwl_m'])
        if study['fixedLength'] is not None:
            assert float(actual['waterlineLength'])==study['fixedLength']
    assert RESULT_MODEL.read_text(encoding='utf-8')==subjects(report)


def test_feasible_search_minimizes_length_not_mass():
    # Small constrained problem exercises the second-stage branch even though
    # no engineering case currently reaches it: L >= .4, trim coordinate = .5.
    class Toy:
        lower=np.zeros(7)
        span=np.ones(7)
        nd=ne=ng=1
        c={'designNames':['lwl_m'],'outputNames':['equilibrium','margin']}
        def run(self,seed,budget):
            return {'numericalFeasible':True,'operatingFeasible':True,'design':{'lwl_m':.9},'states':[[.5]*6]}
        def evaluate(self,z):return np.array([[z[1]-.5,z[0]-.4]])
        def equality(self,z):return self.evaluate(z)[:,0]
        def inequality(self,z):return self.evaluate(z)[:,1]
        def feasible(self,z):return abs(z[1]-.5)<1e-7 and z[0]>=.4-1e-7
        def residual(self,z):return self.equality(z)
    result=solve(Toy(),17,100,True)
    assert result['design']['lwl_m']==pytest.approx(.4)
    assert result['lengthOptimizationMessage']=='Optimization terminated successfully'

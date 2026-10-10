"""Linux/GCC ABI tests; native interpreter parity is covered by test_design_search."""
import sys
import numpy as np
import pytest
from scripts.native_design_kernel import Kernel
from scripts.publish_design_search import read_search

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Generated C search runtime currently requires Linux/GCC')


@pytest.fixture(scope='module')
def kernel():
    return Kernel()


def candidate(kernel):
    best = read_search()['studies']['nominal_5ms']['best']
    return np.array(list(best['design'].values())), np.r_[5,1,1,best['states'][0]]


def test_kernel_matches_saved_results_and_copies_memory(kernel):
    d,s = candidate(kernel)
    first=kernel.evaluate(d,s)
    snapshot=first.copy()
    expected=read_search()['studies']['nominal_5ms']['best']['results'][0]
    np.testing.assert_allclose(first, [expected[k] for k in kernel.contract['outputNames']], rtol=1e-11, atol=1e-9)
    s[5] *= .5
    second=kernel.evaluate(d,s)
    assert not np.array_equal(first,second)
    np.testing.assert_array_equal(first,snapshot)


def test_lift_and_displacement_respond_to_design(kernel):
    d,s=candidate(kernel)
    names=kernel.contract['outputNames']
    base=kernel.evaluate(d,s)
    s[5] *= .5
    lower_alpha=kernel.evaluate(d,s)
    assert lower_alpha[names.index('wingCL')] == pytest.approx(base[names.index('wingCL')]/2)
    d[8] += 1
    heavier=kernel.evaluate(d,s)
    assert heavier[names.index('draft')] > lower_alpha[names.index('draft')]
    assert heavier[names.index('hullDrag')] > lower_alpha[names.index('hullDrag')]


@pytest.mark.parametrize('bad', ['short', 'nan', 'matrix'])
def test_invalid_arrays_fail_before_entering_c(kernel,bad):
    d,s=candidate(kernel)
    if bad=='short': d=d[:-1]
    if bad=='nan': d[0]=np.nan
    if bad=='matrix': s=s.reshape(3,3)
    with pytest.raises(ValueError):kernel.evaluate(d,s)

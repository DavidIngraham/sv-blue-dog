"""Native batching equivalence, failure isolation and shared-library ownership."""
from concurrent.futures import ThreadPoolExecutor
import sys

import numpy as np
import pytest

from sysml_python.backends.native import BatchError, KernelSpec, NativeKernel

pytestmark = pytest.mark.skipif(sys.platform != 'linux', reason='Native runtime requires Linux/GCC')


@pytest.fixture
def kernel(tmp_path):
    # Deliberately reuse static output memory: detects missing per-row copies.
    source = tmp_path / 'fixture.c'
    source.write_text('''#include <stdint.h>
#include <math.h>
#include <stdio.h>
typedef double sysml_real;
typedef struct { int8_t shape; int64_t len; double *data; } sysml_seq_real;
const char *sysml_error(void) { return "negative scale"; }
int sysml_run(sysml_seq_real input, sysml_real scale, sysml_seq_real *result) {
    static double data[2];
    if (scale < 0) return 1;
    data[0] = input.data[0] * scale; data[1] = input.data[1] + scale;
    *result = (sysml_seq_real){2, 2, data}; return 0;
}
''', encoding='utf-8')
    return NativeKernel(KernelSpec(source, ('input', 'scale'), 2))


def test_batch_copy_strides_chunks_and_scalar_equivalence(kernel):
    inputs = np.arange(42.).reshape(7, 6)[:, ::3]  # noncontiguous input
    scales = np.arange(7.)
    expected = np.array([kernel.evaluate(v, s) for v, s in zip(inputs, scales)])
    for chunk in (1, 3, 256):
        result = kernel.evaluate_batch(shared={}, cases={'input': inputs, 'scale': scales}, chunk_size=chunk)
        np.testing.assert_array_equal(result.values, expected)
        assert result.errors == (None,)*7
    actual = kernel.evaluate_batch(shared={'input': [2, 4]}, cases={'scale': scales})
    np.testing.assert_array_equal(actual.values[:, 0], scales*2)
    actual = kernel.evaluate_batch(shared={'scale': 2}, cases={'input': inputs})
    np.testing.assert_array_equal(actual.values[:, 0], inputs[:, 0]*2)


def test_batch_error_index_and_recovery(kernel):
    with pytest.raises(BatchError, match='case 3') as error:
        kernel.evaluate_batch(shared={'input': [2, 4]}, cases={'scale': [1, 2, 3, -1, 5]}, chunk_size=2)
    assert error.value.index == 3
    result = kernel.evaluate_batch(shared={'input': [2, 4]}, cases={'scale': [1, -1, 3]}, errors='collect')
    assert result.errors == (None, 'negative scale', None)
    assert np.isnan(result.values[1]).all()
    np.testing.assert_array_equal(result.values[2], [6, 7])
    np.testing.assert_array_equal(kernel.evaluate([2, 4], 4), [8, 8])


def test_empty_and_invalid_batches(kernel):
    result = kernel.evaluate_batch(shared={'input': [2, 4]}, cases={'scale': []})
    assert result.values.shape == (0, 2) and result.errors == ()
    for shared, cases in [({'input': [1, 2]}, {'scale': [[1]]}),
                          ({'input': [1, 2]}, {'scale': [np.nan]}),
                          ({}, {'input': [[1, 2]], 'scale': [1, 2]}),
                          ({'input': [1, 2], 'scale': 1}, {'scale': [1]})]:
        with pytest.raises(ValueError):
            kernel.evaluate_batch(shared=shared, cases=cases)


def test_instances_share_lock_and_copy_outputs(kernel):
    other = NativeKernel(kernel.spec)
    assert other.lock is kernel.lock
    assert other.lib is kernel.lib
    def run(i):
        target = kernel if i % 2 else other
        return target.evaluate_batch(shared={'input': [i, i+1]}, cases={'scale': [1, 2, 3]}).values
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, range(40)))
    for i, values in enumerate(results):
        np.testing.assert_array_equal(values[:, 0], np.array([1, 2, 3])*i)


def test_output_abi_mismatch_is_checked(kernel):
    wrong = NativeKernel(KernelSpec(kernel.spec.source, ('input', 'scale'), 3))
    with pytest.raises(ValueError, match='ABI mismatch'):
        wrong.evaluate([1, 2], 1)
    with pytest.raises(BatchError, match='ABI mismatch'):
        wrong.evaluate_batch(shared={'input': [1, 2]}, cases={'scale': [1]})


def test_real_operation_batch_matches_scalar():
    from tools.boat_analysis.generated import operation
    from tools.boat_analysis.evidence.records import input_record
    k = operation
    d, p, _, state, aero, mass, hydro = input_record('coupled-operation-audit.json')['inputs']
    states = np.tile(state, (5, 1)); states[:, 3] = np.linspace(1, 3, 5)
    shared = dict(design=d, parameters=p, aero=aero, mass=mass, hydro=hydro)
    result = k.batch(shared=shared, cases={'state': states}, chunk_size=2)
    expected = [list(k(**shared, state=s).values()) for s in states]
    np.testing.assert_allclose(result.values, expected, rtol=1e-13)
    states[2, 3] = 0
    with pytest.raises(ValueError, match='case 2'):
        k.batch(shared=shared, cases={'state': states})


@pytest.mark.parametrize('name,inputs', [
    ('StripLoad', [[1.2, 2, 0, 5, 0, 3, 1, .1, .5, .2], [1.2, 2, 0, 6, 0, 3, 1, .1, .5, .2]]),
    ('SpeedRetention', [[0, 10], [20, 10]]),
    ('WindSample', [[10, 10, .0002, 1, 0, 0, 0, 1, .05], [10, 10, .0002, 2, 0, 0, 0, 1, .05]])])
def test_real_surface_output_types(name, inputs):
    from tools.boat_analysis.model.surface import NativeCalculation
    scalar = NativeCalculation('MarineSurface::'+name, 1)
    expected = np.array([scalar(v) for v in inputs])
    batch = NativeCalculation('MarineSurface::'+name, 1, output_size=expected.shape[1])
    actual = batch.evaluate_batch(shared={}, cases={'input0': inputs})
    np.testing.assert_allclose(actual.values, expected, rtol=1e-14)


def test_generated_runtime_recovers_after_a_failed_row():
    from tools.boat_analysis.model.surface import NativeCalculation
    k = NativeCalculation('MarineSurface::StripLoad', 1, output_size=4)
    valid = [1.2, 2, 0, 5, 0, 3, 1, .1, .5, .2]
    invalid = valid.copy(); invalid[3] = 0  # zero apparent speed: division by zero
    result = k.evaluate_batch(shared={}, cases={'input0': [valid, invalid, valid]}, errors='collect')
    assert result.errors[0] is None and result.errors[1] and result.errors[2] is None
    assert np.isnan(result.values[1]).all()
    np.testing.assert_array_equal(result.values[0], result.values[2])
    np.testing.assert_array_equal(k(valid), result.values[0])


def test_nonfinite_output_is_never_accepted(kernel):
    with pytest.raises(ValueError, match='Nonfinite'):
        kernel.evaluate([2, 4], 1e308)
    result = kernel.evaluate_batch(shared={'input': [2, 4]}, cases={'scale': [1e308, 1]}, errors='collect')
    assert result.errors[0] == 'Nonfinite native output'
    assert np.isnan(result.values[0]).all()
    np.testing.assert_array_equal(result.values[1], [2, 5])


def test_source_change_invalidates_compiled_cache(kernel):
    source = kernel.spec.source
    source.write_text(source.read_text(encoding='utf-8').replace('input.data[0] * scale', 'input.data[0] * scale * 2'), encoding='utf-8')
    updated = NativeKernel(kernel.spec)
    assert updated.lib is not kernel.lib
    np.testing.assert_array_equal(updated.evaluate([2, 4], 2), [8, 6])
    np.testing.assert_array_equal(kernel.evaluate([2, 4], 2), [4, 6])

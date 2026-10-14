"""Portable native ABI, batching, cache and concurrency coverage."""
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pytest
from sysml_python.backends.native import BatchError, KernelSpec, NativeKernel, prepare_kernels


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


def test_group_build_cache_and_isolated_state(tmp_path, monkeypatch):
    from sysml_python.backends import build
    sources = []
    for i in range(2):
        source = tmp_path / f'constant{i}.c'
        source.write_text(f"""#include <stdint.h>
#include <math.h>
#include <stdio.h>
typedef double sysml_real;
const char *sysml_error(void) {{ return "error"; }}
int sysml_run(sysml_real value, sysml_real *result) {{ *result = value + {i}; return 0; }}
""")
        sources.append(source)
    specs = [KernelSpec(source, ('value',), 1) for source in sources]
    kernels = prepare_kernels(specs)
    assert kernels[sources[0]].evaluate(2)[0] == 2
    assert kernels[sources[1]].evaluate(2)[0] == 3
    assert kernels[sources[0]].lib is not kernels[sources[1]].lib
    assert len(list((tmp_path/'.native').glob('*/receipt.json'))) == 1
    def unexpected(*args):
        raise AssertionError('Unchanged build should reuse receipt')
    monkeypatch.setattr(build, '_run', unexpected)
    cached = prepare_kernels(specs)
    assert cached[sources[0]].lib is kernels[sources[0]].lib
    metadata = cached[sources[0]].lib._sysml_build
    assert metadata['compilers']['c']['id']
    assert metadata['mesonVersion']
    assert len(metadata['recipeSha256']) == 64


def test_meson_diagnostic_includes_compiler_error(tmp_path):
    from sysml_python.backends.build import build_libraries
    source = tmp_path/'broken.c'
    source.write_text('#error deliberate_compiler_failure\n')
    with pytest.raises(RuntimeError, match='deliberate_compiler_failure'):
        build_libraries([source])
    assert not list((tmp_path/'.native').glob('*/receipt.json'))


def test_conflicting_source_names_rejected(tmp_path):
    from sysml_python.backends.build import build_libraries
    a = tmp_path/'a'; a.mkdir()
    b = tmp_path/'b'; b.mkdir()
    (a/'same.c').write_text('first')
    (b/'same.c').write_text('second')
    with pytest.raises(ValueError, match='Conflicting'):
        build_libraries([a/'same.c', b/'same.c'])


def test_concurrent_processes_publish_one_snapshot(tmp_path):
    import subprocess
    import sys
    source = tmp_path/'shared.c'
    source.write_text("""#include <stdint.h>
#include <math.h>
#include <stdio.h>
typedef double sysml_real;
const char *sysml_error(void) { return "error"; }
int sysml_run(sysml_real value, sysml_real *result) { *result = value * 2; return 0; }
""")
    script = "from pathlib import Path; import sys; from sysml_python.backends.native import NativeKernel, KernelSpec; k=NativeKernel(KernelSpec(Path(sys.argv[1]), ('value',), 1)); print(k.evaluate(3)[0])"
    def run(_):
        return subprocess.check_output([sys.executable, '-c', script, str(source)], text=True).strip()
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(run, range(2))) == ['6.0', '6.0']
    assert len(list((tmp_path/'.native').glob('*/receipt.json'))) == 1

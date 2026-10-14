"""Shared execution of generated OpenSysML C; project-independent runtime.

Batching uses explicit shared/cases mappings, never inferred broadcasting.
Generated code has process-global state: calls to one loaded library serialize.
"""
from dataclasses import dataclass
import ctypes as ct
import hashlib
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .abi import Sequence
from .build import build_libraries


@dataclass(frozen=True)
class KernelSpec:
    source: Path
    arguments: tuple[str, ...]
    output_size: int | None = None

    def __post_init__(self):
        if len(set(self.arguments)) != len(self.arguments):
            raise ValueError('Kernel argument names must be unique')
        if self.output_size is not None and self.output_size < 1:
            raise ValueError('Expected positive output size')


@dataclass(frozen=True)
class BatchResult:
    values: NDArray[np.float64]
    errors: tuple[str | None, ...]


class BatchError(ValueError):
    def __init__(self, index: int, message: str):
        self.index = index
        super().__init__(f"Batch case {index}: {message}")


_registry_lock = threading.RLock()
_libraries = {}


def load_library(source: Path, *, dependencies=(), built=None):
    source = source.resolve()
    library, metadata = built or build_libraries((source,), dependencies=dependencies)[source]
    with _registry_lock:
        if library not in _libraries:
            lib = ct.CDLL(str(library))
            lib._sysml_build = metadata
            lib.sysml_error.restype = ct.c_char_p
            _libraries[library] = (lib, threading.RLock())
        return _libraries[library]


class Number(ct.Structure):
    _fields_ = [('real', ct.c_bool), ('integer', ct.c_int64), ('value', ct.c_double)]


class NumberSequence(ct.Structure):
    _fields_ = [('shape', ct.c_int8), ('length', ct.c_int64), ('data', ct.POINTER(Number))]


class NativeKernel:
    def __init__(self, spec: KernelSpec, *, _defer=False):
        self.spec = spec
        text = spec.source.read_text(encoding='utf-8')
        signature = re.search(r'int sysml_run\((.*?)\)\s*\{', text, re.S)
        if not signature:
            raise ValueError('Missing sysml_run ABI')
        fields = signature[1].split(',')
        types = [field.strip().rsplit(' ', 1)[0] for field in fields[:-1]]
        self.vector = tuple(t == 'sysml_seq_real' for t in types)
        if len(types) != len(spec.arguments) or any(t not in ('sysml_seq_real', 'sysml_real') for t in types):
            raise ValueError('Unsupported native input ABI: ' + signature[1])
        output = fields[-1].strip()
        outputs = {'sysml_seq_real *result': Sequence, 'sysml_seq_num *result': NumberSequence,
                   'sysml_real *result': ct.c_double, 'sysml_num *result': Number}
        if output not in outputs:
            raise ValueError('Unsupported native output ABI: ' + output)
        self.result_type = outputs[output]
        if self.result_type in (ct.c_double, Number) and spec.output_size not in (None, 1):
            raise ValueError('Scalar output requires size 1')
        shim = self._shim(output.split(' *')[0])
        wrapper = spec.source.parent / ('batch-' + hashlib.sha256(shim.encode()).hexdigest()[:24] + '.c')
        if not wrapper.exists():
            # Concurrent constructors publish complete identical source atomically.
            fd, temporary = tempfile.mkstemp(dir=wrapper.parent, suffix='.c')
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(shim)
            os.replace(temporary, wrapper)
        self.wrapper = wrapper
        if not _defer:
            self._load()

    def _load(self, built=None):
        self.lib, self.lock = load_library(self.wrapper, dependencies=(self.spec.source,), built=built)
        self.lib.sysml_run.argtypes = [Sequence if v else ct.c_double for v in self.vector] + [ct.POINTER(self.result_type)]
        self.lib.sysml_run.restype = ct.c_int
        pointer = ct.POINTER(ct.c_double)
        self.lib.sysml_python_batch.argtypes = [ct.c_int64, ct.POINTER(pointer), ct.POINTER(ct.c_int64),
            ct.POINTER(ct.c_int64), ct.c_int64, pointer, ct.POINTER(ct.c_int), ct.c_void_p]
        self.lib.sysml_python_batch.restype = None

    def _shim(self, output):
        args = []
        for i, vector in enumerate(self.vector):
            args.append(f'(sysml_seq_real){{2, widths[{i}], inputs[{i}] + row * strides[{i}]}}' if vector
                        else f'inputs[{i}][row * strides[{i}]]')
        check = '' if output in ('sysml_real', 'sysml_num') else 'if (out.shape != 2 || out.len != width || !out.data) message = "Output ABI mismatch";'
        value = {'sysml_real': 'out', 'sysml_num': '(out.real ? out.r : out.i)',
                 'sysml_seq_real': 'out.data[j]',
                 'sysml_seq_num': '(out.data[j].real ? out.data[j].r : out.data[j].i)'}[output]
        return f'''#include "{self.spec.source.name}"
void sysml_python_batch(int64_t count, double **inputs, int64_t *widths, int64_t *strides,
                int64_t width, double *values, int *status, char *errors) {{
    for (int64_t row = 0; row < count; row++) {{
        {output} out;
        const char *message = NULL;
        if (sysml_run({', '.join([*args, '&out'])})) {{ message = sysml_error(); if (!message) message = "Native calculation failed"; }}
        else {{ {check} }}
        if (!message) for (int64_t j = 0; j < width; j++) {{
            double value = {value};
            if (!isfinite(value)) {{ message = "Nonfinite native output"; break; }}
            values[row * width + j] = value;
        }}
        status[row] = message ? 1 : 0;
        if (message) {{
            snprintf(errors + row * 512, 512, "%s", message);
            for (int64_t j = 0; j < width; j++) values[row * width + j] = NAN;
        }}
    }}
}}
'''

    def evaluate(self, *values):
        if len(values) != len(self.vector):
            raise ValueError('Wrong number of native arguments')
        arrays = [np.ascontiguousarray(v, dtype=float) if vector else np.asarray(v, dtype=float)
                  for v, vector in zip(values, self.vector)]
        if any(a.ndim != int(v) or not np.isfinite(a).all() for a, v in zip(arrays, self.vector)):
            raise ValueError('Finite vectors/scalars required by native ABI')
        args = [Sequence(2, a.size, a.ctypes.data_as(ct.POINTER(ct.c_double))) if v else float(a)
                for a, v in zip(arrays, self.vector)]
        with self.lock:
            out = self.result_type()
            if self.lib.sysml_run(*args, ct.byref(out)):
                raise ValueError(self.lib.sysml_error().decode())
            if self.result_type is ct.c_double:
                result = np.array([out.value])
            elif self.result_type is Number:
                result = np.array([out.value if out.real else out.integer], dtype=float)
            else:
                if out.shape != 2 or out.length < 0 or (out.length and not out.data):
                    raise ValueError('Output ABI mismatch')
                if self.spec.output_size is not None and out.length != self.spec.output_size:
                    raise ValueError('Output ABI mismatch')
                if self.result_type is NumberSequence:
                    result = np.array([out.data[i].value if out.data[i].real else out.data[i].integer for i in range(out.length)])
                else:
                    result = np.ctypeslib.as_array(out.data, shape=(out.length,)).copy() if out.length else np.empty(0)
        if not np.isfinite(result).all():
            raise ValueError('Nonfinite native output')
        return result

    def evaluate_batch(self, *, shared: Mapping[str, ArrayLike], cases: Mapping[str, ArrayLike],
                       chunk_size: int = 256, errors: str = 'raise') -> BatchResult:
        """Independent rows, stable ordering; errors='collect' marks failed rows NaN.

        Vectors are (width,) shared or (cases,width); scalars () or (cases,).
        A batch needs at least one per-case input and a declared output size.
        """
        if errors not in ('raise', 'collect') or not isinstance(chunk_size, int) or chunk_size < 1:
            raise ValueError('Invalid batch error policy or chunk size')
        if set(shared) & set(cases) or set(shared) | set(cases) != set(self.spec.arguments) or not cases:
            raise ValueError('Supply each argument exactly once in shared or cases')
        width = self.spec.output_size
        if width is None or width < 1 or (self.result_type in (ct.c_double, Number) and width != 1):
            raise ValueError('Batch requires a fixed positive output size')
        arrays = []; strides = []; widths = []; count = None
        for name, vector in zip(self.spec.arguments, self.vector):
            per_case = name in cases
            a = np.asarray(cases[name] if per_case else shared[name], dtype=float)
            if a.ndim != int(vector) + int(per_case) or not np.isfinite(a).all():
                raise ValueError(f'{name}: wrong batch shape or nonfinite input')
            if per_case:
                if count is not None and count != len(a):
                    raise ValueError('Unequal batch lengths')
                count = len(a)
            w = a.shape[-1] if vector else 1
            widths.append(w); strides.append(w if per_case else 0)
            arrays.append(np.ascontiguousarray(a).reshape(-1))
        result = np.empty((count, width)); messages = []
        pointer = ct.POINTER(ct.c_double)
        for start in range(0, count, chunk_size):
            n = min(chunk_size, count-start)
            pointers = (pointer * len(arrays))(*(a[start*s:].ctypes.data_as(pointer) for a, s in zip(arrays, strides)))
            status = np.zeros(n, dtype=np.int32); buffer = ct.create_string_buffer(n*512)
            with self.lock:
                self.lib.sysml_python_batch(n, pointers, (ct.c_int64*len(widths))(*widths),
                    (ct.c_int64*len(strides))(*strides), width, result[start:].ctypes.data_as(pointer),
                    status.ctypes.data_as(ct.POINTER(ct.c_int)), buffer)
            for i, failed in enumerate(status):
                message = buffer.raw[i*512:(i+1)*512].split(b'\0')[0].decode(errors='replace') if failed else None
                if failed and errors == 'raise':
                    raise BatchError(start+i, message)
                messages.append(message)
        return BatchResult(result, tuple(messages))


def prepare_kernels(specs):
    """Compile a project's exports and checks together, retaining separate library state."""
    kernels = [NativeKernel(spec, _defer=True) for spec in specs]
    built = build_libraries([k.wrapper for k in kernels], dependencies=[k.spec.source for k in kernels])
    for kernel in kernels:
        kernel._load(built[kernel.wrapper.resolve()])
    return {kernel.spec.source.resolve(): kernel for kernel in kernels}

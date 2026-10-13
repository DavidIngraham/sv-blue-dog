"""Contract-driven numerical calls; domain equations and checks stay in SysML."""
import json
from collections.abc import Mapping
import numpy as np
from .runtime import ROOT
from .native_kernel import KernelSpec, NativeKernel, BatchError
from ..evidence.records import digest, validate

_CONTRACTS = {'mass':'coupled-contract.json', **dict.fromkeys(
    ('operation','structure','route','concept'), 'coupled-operation-contract.json')}


def load_model(name):
    contract = json.loads((ROOT/'.tools'/_CONTRACTS[name]).read_text(encoding='utf-8'))
    validate(contract['sourceHashes'])
    if name not in contract.get('kernels', {}):
        raise ValueError('Missing generated boundary; run boat_analysis.cli prepare')
    return ModelBoundary(contract, contract['kernels'][name])


class ModelBoundary:
    def __init__(self, contract, schema):
        self.contract, self.schema = contract, schema
        source = ROOT/schema['source']
        if digest(source) != contract[schema['hashKey']]:
            raise ValueError('Stale generated model: '+str(source))
        self.names = tuple(a['name'] for a in schema['arguments'])
        self.runtime = NativeKernel(KernelSpec(source, self.names, schema['outputSize']))
        if tuple(bool(a['shape']) for a in schema['arguments']) != self.runtime.vector:
            raise ValueError('Contract dimensions differ from the compiled ABI')
        self.checks = None
        if check := schema.get('checks'):
            source = ROOT/check['source']
            if digest(source) != check['sourceHash']:
                raise ValueError('Stale generated preconditions')
            self.checks = NativeKernel(KernelSpec(source, tuple(check['arguments']), len(check['outputs'])))

    def input_vector(self, name, value):
        """Pack a named record at the ABI edge, never by dictionary insertion order."""
        if hasattr(value, 'to_mapping'):
            expected = self.schema.get('recordTypes', {}).get(name)
            if expected is not None and value.sysml_id != expected:
                raise TypeError(f'{name}: expected {expected}, got {value.sysml_id}')
            value = value.to_mapping()
        if isinstance(value, Mapping):
            key = self.schema['records'].get(name)
            if key is None:
                raise TypeError(f'{name}: no named record declared in the model')
            names = self.contract[key]
            if set(value) != set(names) or len(set(names)) != len(names):
                raise ValueError('Typed record differs from generated model fields')
            value = [value[n] for n in names]
        return value

    def _inputs(self, shared, cases):
        if set(shared)&set(cases) or (set(shared)|set(cases))-set(self.names):
            raise ValueError('Unknown or duplicate model arguments')
        shared, cases = dict(shared), dict(cases)
        for name, key in self.schema['defaults'].items():
            if name not in cases and shared.get(name) is None:
                shared[name] = self.contract[key]
        if set(shared)|set(cases) != set(self.names):
            raise ValueError('Missing model arguments: '+', '.join(set(self.names)-set(shared)-set(cases)))
        count = None
        for arg in self.schema['arguments']:
            name = arg['name']; target = cases if name in cases else shared
            value = target[name]
            if name in cases and isinstance(value, (list, tuple)):
                value = [self.input_vector(name, row) for row in value]
                if not len(value):
                    value = np.empty((0, *arg['shape']))
            else:
                value = self.input_vector(name, value)
            array = np.asarray(value, dtype=float)
            shape = tuple(arg['shape'])
            if name in cases:
                if array.ndim != len(shape)+1 or array.shape[1:] != shape:
                    raise ValueError(f'{name}: expected case rows of shape {shape}')
                if count is not None and len(array) != count:
                    raise ValueError('Unequal batch lengths')
                count = len(array)
            elif array.shape != shape:
                raise ValueError(f'{name}: expected shape {shape}')
            if not np.isfinite(array).all():
                raise ValueError(f'{name}: finite inputs required')
            target[name] = array
        return shared, cases

    def _validate(self, shared, cases, chunk_size):
        if self.checks is None:
            return
        names = self.schema['checks']['arguments']
        shared = {k:v for k,v in shared.items() if k in names}
        cases = {k:v for k,v in cases.items() if k in names}
        if cases:
            values = self.checks.evaluate_batch(shared=shared, cases=cases, chunk_size=chunk_size).values
        else:
            values = self.checks.evaluate(*(shared[n] for n in names))[None, :]
        failed = np.argwhere(values != 1)
        if len(failed):
            row, column = failed[0]
            message = 'Invalid physical inputs: '+self.schema['checks']['outputs'][column]
            if cases:
                raise BatchError(int(row), message)
            raise ValueError(message)

    def evaluate(self, **inputs):
        shared, _ = self._inputs(inputs, {})
        self._validate(shared, {}, 256)
        values = self.runtime.evaluate(*(shared[n] for n in self.names))
        names = self.schema['outputs']
        return dict(zip(names, values, strict=True)) if names else values

    def evaluate_batch(self, *, shared, cases, chunk_size=256, errors='raise'):
        if not cases:
            raise ValueError('At least one per-case input is required')
        shared, cases = self._inputs(shared, cases)
        self._validate(shared, cases, chunk_size)
        return self.runtime.evaluate_batch(shared=shared, cases=cases, chunk_size=chunk_size, errors=errors)


class ModelAdapter:
    """Small compatibility facade for named domain APIs."""
    model_name: str

    def __init__(self):
        self.kernel = load_model(self.model_name)
        self.contract = self.kernel.contract
        self.runtime = self.kernel.runtime

    def evaluate_batch(self, *, shared, cases, **options):
        return self.kernel.evaluate_batch(shared=shared, cases=cases, **options)

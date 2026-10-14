"""Named numerical boundaries shared by scalar and batched execution."""
from collections.abc import Mapping
import json
from functools import lru_cache
from pathlib import Path
import numpy as np
from .backends.opensysml import digest
from .backends.native import NativeKernel, KernelSpec, BatchError


@lru_cache(maxsize=1024)
def _digest_at_revision(path, revision):
    return digest(path)


def checked_digest(path):
    """Reuse hashes while file identity, size and filesystem timestamps agree."""
    path = Path(path)
    stat = path.stat()
    revision = (stat.st_dev, stat.st_ino, stat.st_size,
                stat.st_mtime_ns, stat.st_ctime_ns)
    return _digest_at_revision(str(path), revision)


class Calculation:
    def __init__(self, manifest, name, result_type):
        self.manifest = Path(manifest)
        self.name, self.result_type = name, result_type
        self._kernel = self._checks = self._schema_key = None

    def load(self):
        contract = json.loads(self.manifest.read_text(encoding='utf-8'))
        for path, expected in contract['sourceHashes'].items():
            if checked_digest(path) != expected:
                raise ValueError(f'Stale SysML source: {path}; prepare the project again')
        schema = contract['exports'][self.name]
        for entry in (schema, schema.get('checks')):
            if entry and checked_digest(self.manifest.parent/entry['source']) != entry['sourceHash']:
                raise ValueError('Generated source differs from prepared contract')
        key = json.dumps(schema, sort_keys=True)
        if self._kernel is None or self._schema_key != key:
            def kernel(entry):
                return NativeKernel(KernelSpec(self.manifest.parent/entry['source'],
                                    tuple(f['name'] for f in entry['inputs']),len(entry['outputs'])))
            self._kernel = kernel(schema)
            self._checks = kernel(schema['checks']) if 'checks' in schema else None
            self._schema_key = key
        return schema

    @staticmethod
    def pack(field, value):
        record = field.get('record')
        if hasattr(value, 'to_mapping'):
            if record and getattr(value,'sysml_id',None) != record['sysml_id']:
                raise TypeError(f"{field['name']}: incompatible SysML record")
            value = value.to_mapping()
        if isinstance(value, Mapping):
            if not record or set(value) != set(record['fields']):
                raise ValueError(f"{field['name']}: mapping differs from model record")
            value = [value[n] for n in record['fields']]
        return value

    def inputs(self, schema, shared, cases):
        names = {f['name'] for f in schema['inputs']}
        if set(shared)&set(cases) or (set(shared)|set(cases))-names:
            raise ValueError('Supply each argument exactly once in shared or cases')
        shared, cases = dict(shared), dict(cases)
        count = None
        for field in schema['inputs']:
            name, shape = field['name'], tuple(field['shape'])
            if name not in cases and shared.get(name) is None and 'default' in field:
                shared[name] = field['default']
            if name not in shared and name not in cases:
                raise ValueError('Missing model input: '+name)
            target = cases if name in cases else shared
            value = target[name]
            if name in cases and isinstance(value, (list,tuple)):
                value = [self.pack(field,row) for row in value]
                if not value: value = np.empty((0,*shape))
            else:
                value = self.pack(field,value)
            array = np.asarray(value,dtype=float)
            expected = (len(array),*shape) if name in cases and array.ndim else shape
            if array.shape != expected or (name in cases and array.ndim != len(shape)+1):
                raise ValueError(f'{name}: expected '+('batch rows of ' if name in cases else '')+str(shape))
            if not np.isfinite(array).all():
                raise ValueError(f'{name}: finite inputs required')
            if name in cases:
                if count is not None and count != len(array):
                    raise ValueError('Unequal batch lengths')
                count = len(array)
            target[name] = array
        return shared, cases

    def validate(self, schema, shared, cases):
        if self._checks is None: return
        names = [f['name'] for f in schema['checks']['inputs']]
        selected = {n:cases[n] for n in names if n in cases}
        if selected:
            result = self._checks.evaluate_batch(shared={n:shared[n] for n in names if n in shared},cases=selected).values
        else:
            result = self._checks.evaluate(*(shared[n] for n in names))[None,:]
        failed = np.argwhere(result != 1)
        if len(failed):
            row, column = failed[0]
            message = 'Invalid physical inputs: '+schema['checks']['outputs'][column]['name']
            if selected: raise BatchError(int(row),message)
            raise ValueError(message)

    def prepare_inputs(self, **inputs):
        """Return validated named arrays for an external numerical binding."""
        schema = self.load()
        shared, _ = self.inputs(schema, inputs, {})
        self.validate(schema, shared, {})
        return shared

    def __call__(self, **inputs):
        schema = self.load()
        shared, _ = self.inputs(schema,inputs,{})
        self.validate(schema,shared,{})
        values = self._kernel.evaluate(*(shared[f['name']] for f in schema['inputs']))
        return self.result_type(**dict(zip((f['name'] for f in schema['outputs']),values,strict=True)))

    def batch(self, *, shared, cases, **options):
        schema = self.load()
        shared, cases = self.inputs(schema,shared,cases)
        self.validate(schema,shared,cases)
        return self._kernel.evaluate_batch(shared=shared,cases=cases,**options)

"""Lazy execution of prepared project exports with stale-source protection."""
import json
from pathlib import Path
from .backends.opensysml import digest
from .backends.native import NativeKernel, KernelSpec


class Calculation:
    def __init__(self, manifest, name, result_type):
        self.manifest = Path(manifest)
        self.name, self.result_type = name, result_type
        self._kernel = None
        self._schema_key = None

    def load(self):
        contract = json.loads(self.manifest.read_text(encoding='utf-8'))
        for path, expected in contract['sourceHashes'].items():
            if digest(path) != expected:
                raise ValueError(f'Stale SysML source: {path}; prepare the project again')
        schema = contract['exports'][self.name]
        source = self.manifest.parent/schema['source']
        if digest(source) != schema['sourceHash']:
            raise ValueError('Generated C source differs from prepared contract')
        names = tuple(f['name'] for f in schema['inputs'])
        key = json.dumps(schema, sort_keys=True)
        if self._kernel is None or self._schema_key != key:
            self._kernel = NativeKernel(KernelSpec(source,names,len(schema['outputs'])))
            self._schema_key = key
        return schema, names

    def __call__(self, **inputs):
        schema, names = self.load()
        values = self._kernel.evaluate(*(inputs[n] for n in names))
        return self.result_type(**dict(zip((f['name'] for f in schema['outputs']), values, strict=True)))

    def batch(self, *, shared, cases, **options):
        schema, names = self.load()
        shared = dict(shared)
        for f in schema['inputs']:
            if f['name'] not in shared and f['name'] not in cases and 'default' in f:
                shared[f['name']] = f['default']
        return self._kernel.evaluate_batch(shared=shared,cases=cases,**options)

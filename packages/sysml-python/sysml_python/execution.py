"""Named numerical boundaries shared by scalar and batched execution."""
from collections.abc import Mapping
import json
import hashlib
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
from pathlib import Path
import numpy as np
from .provenance import digest, project_root
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


class ExecutionReport:
    """Evidence for calls made inside a verified execution session."""
    def __init__(self):
        self.status = 'running'
        self._snapshots = {}
        self._operations = {}

    def record(self, provenance, mode, rows, failed_rows=0):
        key = (provenance['manifestSha256'], provenance['export'], mode)
        if key not in self._operations:
            self._operations[key] = {'provenance': provenance, 'mode': mode, 'calls': 0, 'rows': 0, 'failedRows': 0}
        self._operations[key]['calls'] += 1
        self._operations[key]['rows'] += rows
        self._operations[key]['failedRows'] += failed_rows

    def to_mapping(self):
        # Copy so callers cannot mutate the report's underlying evidence.
        return json.loads(json.dumps({'status': self.status, 'operations': list(self._operations.values())}))


_active_session = ContextVar('sysml_execution_session', default=None)


def _validate_project(manifest, contract):
    root = project_root(manifest, contract)
    config = contract['configuration']
    if checked_digest(root / config['path']) != config['sha256']:
        raise ValueError('Stale project configuration; prepare the project again')
    files = [p for pattern in contract['modelPatterns'] for p in root.glob(pattern) if p.is_file()]
    expected_paths = set(contract['sourceHashes'])
    paths = {p.relative_to(root).as_posix() for p in files}
    # Common case: lexical paths already match. Resolve aliases only when the
    # discovered set differs, retaining the same symlink/discovery semantics.
    if paths != expected_paths:
        paths = {p.resolve().relative_to(root).as_posix() for p in files}
        if paths != expected_paths:
            raise ValueError('SysML source set changed; prepare the project again')
    for path, expected in contract['sourceHashes'].items():
        if checked_digest(root / path) != expected:
            raise ValueError(f'Stale SysML source: {path}; prepare the project again')
    runtime = Path(__file__).parent
    actual = {p.relative_to(runtime).as_posix() for p in runtime.rglob('*.py')}
    if actual != set(contract['runtime']['sourceHashes']):
        raise ValueError('Runtime implementation changed; prepare the project again')
    for path, expected in contract['runtime']['sourceHashes'].items():
        if checked_digest(runtime / path) != expected:
            raise ValueError('Runtime implementation changed; prepare the project again')
    if checked_digest(manifest.parent / '__init__.py') != contract['pythonHash']:
        raise ValueError('Generated Python differs from prepared contract')


def _validate_snapshot(manifest, contract):
    _validate_project(manifest, contract)
    for schema in contract['exports'].values():
        _validate_generated(manifest, schema)


def _validate_generated(manifest, schema):
    for entry in (schema, schema.get('checks')):
        if entry and checked_digest(manifest.parent/entry['source']) != entry['sourceHash']:
            raise ValueError('Generated source differs from prepared contract')


@contextmanager
def execution_session():
    """Execute a prepared snapshot; reject source changes before returning.

    Nested sessions share the outer snapshot. Standalone calls still check on
    every invocation. Use this context (or decorator) around a solve or campaign,
    not around a generator function whose body runs after it returns.
    """
    if (existing := _active_session.get()) is not None:
        yield existing
        return
    report = ExecutionReport()
    snapshots = report._snapshots
    token = _active_session.set(report)
    try:
        yield report
        for manifest, (fingerprint, contract) in snapshots.items():
            if checked_digest(manifest) != fingerprint:
                raise ValueError('Prepared manifest changed during execution session')
            _validate_snapshot(manifest, contract)
        report.status = 'complete'
    except BaseException:
        report.status = 'failed'
        raise
    finally:
        _active_session.reset(token)


class Calculation:
    def __init__(self, manifest, name, result_type):
        self.manifest = Path(manifest)
        self.name, self.result_type = name, result_type
        self._kernel = self._checks = self._schema_key = None

    def load(self):
        report = _active_session.get()
        snapshots = report._snapshots if report is not None else None
        if snapshots is None:
            contract = json.loads(self.manifest.read_text(encoding='utf-8'))
            _validate_project(self.manifest, contract)
            schema = contract['exports'][self.name]
            _validate_generated(self.manifest, schema)
        else:
            if self.manifest not in snapshots:
                data = self.manifest.read_bytes()
                contract = json.loads(data)
                _validate_snapshot(self.manifest, contract)
                snapshots[self.manifest] = (hashlib.sha256(data).hexdigest(), contract)
            contract = snapshots[self.manifest][1]
            schema = contract['exports'][self.name]
        self._contract = contract
        self._fingerprint = snapshots[self.manifest][0] if snapshots is not None else checked_digest(self.manifest)
        key = json.dumps(schema, sort_keys=True)
        if self._kernel is None or self._schema_key != key:
            def kernel(entry):
                return NativeKernel(KernelSpec(self.manifest.parent/entry['source'],
                                    tuple(f['name'] for f in entry['inputs']),len(entry['outputs'])))
            self._kernel = kernel(schema)
            self._checks = kernel(schema['checks']) if 'checks' in schema else None
            self._schema_key = key
        return schema

    def provenance(self):
        """Identify prepared sources, schema, runtime and the loaded native build."""
        schema = self.load()
        return json.loads(json.dumps(self._provenance(schema)))

    def _provenance(self, schema):
        return {'manifestSha256': self._fingerprint, 'export': self.name,
                'definition': schema['definition'],
                'configuration': self._contract['configuration'],
                'sourceHashes': self._contract['sourceHashes'],
                'runtime': self._contract['runtime'],
                'sysmlCompiler': self._contract['compiler'],
                'nativeBuild': self._kernel.lib._sysml_build,
                'generatedSourceSha256': schema['sourceHash'],
                'checks': ({'definition': schema['checks']['definition'],
                            'generatedSourceSha256': schema['checks']['sourceHash'],
                            'nativeBuild': self._checks.lib._sysml_build} if self._checks else None)}

    def _record(self, schema, mode, rows, failed_rows=0):
        if (report := _active_session.get()) is not None:
            report.record(self._provenance(schema), mode, rows, failed_rows)

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
        self._record(schema, 'validated-inputs', 1)
        return shared

    def __call__(self, **inputs):
        schema = self.load()
        shared, _ = self.inputs(schema,inputs,{})
        self.validate(schema,shared,{})
        values = self._kernel.evaluate(*(shared[f['name']] for f in schema['inputs']))
        result = self.result_type(**dict(zip((f['name'] for f in schema['outputs']),values,strict=True)))
        self._record(schema, 'scalar', 1)
        return result

    def batch(self, *, shared, cases, **options):
        schema = self.load()
        shared, cases = self.inputs(schema,shared,cases)
        self.validate(schema,shared,cases)
        result = self._kernel.evaluate_batch(shared=shared,cases=cases,**options)
        self._record(schema, 'batch', len(result.values), sum(error is not None for error in result.errors))
        return result

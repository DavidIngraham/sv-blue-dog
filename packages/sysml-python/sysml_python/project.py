"""Explicit project exports and generated Python entry points."""
import json
import keyword
import os
from pathlib import Path
import tomllib
from .backends.opensysml import OpenSysML
from .provenance import digest, runtime_sources
from .records import Record


def identifier(name):
    if not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError(f'Not a Python identifier: {name}')
    return name


class Project:
    def __init__(self, path, *, executable=None):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.config = tomllib.loads(self.path.read_text(encoding='utf-8'))['tool']['sysml_python']
        allowed = {'models','generated_package','backend','exports'}
        if set(self.config)-allowed:
            raise ValueError('Unknown project settings: '+str(set(self.config)-allowed))
        if self.config.get('backend','opensysml-c') != 'opensysml-c':
            raise ValueError('Unsupported backend')
        sources = sorted({p.resolve() for pattern in self.config['models'] for p in self.root.glob(pattern) if p.is_file()})
        if not sources:
            raise ValueError('No SysML source files matched')
        executable = executable or os.environ.get('OPENSYSML_BINARY')
        if not executable:
            raise ValueError('Supply executable= or OPENSYSML_BINARY for the pinned OpenSysML binary')
        self.backend = OpenSysML(executable, sources)

    def prepare(self):
        self.__init__(self.path, executable=self.backend.executable)
        package = self.config.get('generated_package','generated')
        if any(not n.isidentifier() or keyword.iskeyword(n) for n in package.split('.')):
            raise ValueError('Invalid generated package')
        directory = self.root.joinpath(*package.split('.'))
        generated_python = directory/'__init__.py'
        if generated_python.exists() and not generated_python.read_text(encoding='utf-8').startswith('# Generated from SysML. Do not edit.'):
            raise ValueError('Refusing to overwrite a non-generated Python package: '+str(directory))
        directory.mkdir(parents=True, exist_ok=True)
        definitions = {definition for settings in self.config['exports'].values()
                       for definition in settings.get('records', {}).values()}
        snapshot_source = self.backend.record_source(definitions) if definitions else ''
        manifest = {'schemaVersion':2,
                    'projectRoot':Path(os.path.relpath(self.root, directory)).as_posix(),
                    'configuration':{'path':self.path.relative_to(self.root).as_posix(),'sha256':digest(self.path)},
                    'modelPatterns':self.config['models'],
                    'runtime':{'sourceHashes':runtime_sources()},
                    'sourceHashes':{p.relative_to(self.root).as_posix():digest(p) for p in self.backend.sources},
                    'compiler':{'path':str(self.backend.executable),'sha256':digest(self.backend.executable)},'exports':{}}
        code = ['# Generated from SysML. Do not edit.', snapshot_source, 'from dataclasses import dataclass',
                'from pathlib import Path', 'from numpy.typing import ArrayLike, NDArray', 'import numpy as np', 'from typing import TypedDict, Literal, Sequence',
                'from sysml_python.backends.native import BatchResult',
                'from sysml_python.records import Record', 'from sysml_python.execution import Calculation', '']
        record_names, analyses = {}, {}
        symbols = {'dataclass', 'Path', 'ArrayLike', 'TypedDict', 'Literal', 'Sequence',
                   'BatchResult', 'Record', 'Calculation', 'NDArray', 'np'}
        def reserve(label):
            identifier(label)
            if label in symbols:
                raise ValueError('Generated symbol collision: '+label)
            symbols.add(label)
        for name in self.config['exports']:
            reserve(name)
        def emit_result(label, record):
            reserve(label)
            if len(set(record['fields'])) != len(record['fields']):
                raise ValueError('Duplicate record fields')
            for field in record['fields']:
                if field.startswith('_') or field in dir(Record) or field == 'sysml_id':
                    raise ValueError('Record field conflicts with runtime API: '+field)
            code.extend(['@dataclass(frozen=True)', f'class {label}(Record):', f"    sysml_id = {record['sysml_id']!r}"])
            for field in record['fields']:
                code.append(f'    {identifier(field)}: float')
            code.append('')
        for name, settings in self.config['exports'].items():
            identifier(name)
            allowed = {'definition','aliases','records','defaults','checks','output_definition','output_record'}
            if set(settings)-allowed:
                raise ValueError(f'{name}: unsupported settings {set(settings)-allowed}')
            schema = self.backend.describe(settings['definition'], output_definition=settings.get('output_definition'))
            aliases = settings.get('aliases', {})
            raw_names = {f['name'] for f in schema['inputs']}
            if set(aliases)-raw_names:
                raise ValueError('Alias refers to an absent parameter')
            for f in schema['inputs']:
                f['nativeName'] = f['name']
                f['name'] = identifier(aliases.get(f['name'],f['name']))
                if f['name'] == 'self':
                    raise ValueError('Input name self is reserved; supply an alias')
            if len({f['name'] for f in schema['inputs']}) != len(schema['inputs']):
                raise ValueError('Duplicate public input names')
            by_name = {f['name']:f for f in schema['inputs']}
            for argument, reference in settings.get('defaults', {}).items():
                if argument not in by_name:
                    raise ValueError('Default refers to an absent input: '+argument)
                analysis, field = reference.rsplit('.',1)
                if analysis not in analyses:
                    analyses[analysis] = self.backend.analysis_values(analysis)
                by_name[argument]['default'] = analyses[analysis][field]
                by_name[argument]['defaultSource'] = reference
            for f in schema['inputs']:
                if f['shape'] == [None]:
                    if not isinstance(f.get('default'), list):
                        raise ValueError('Unbounded vector requires a model-evaluated default to fix shape')
                    f['shape'] = [len(f['default'])]
            for argument, definition in settings.get('records', {}).items():
                record = self.backend.record(definition)
                if argument not in by_name or by_name[argument]['shape'] != [len(record['fields'])]:
                    raise ValueError('Record fields differ from input dimensions: '+argument)
                by_name[argument]['record'] = record
                if definition not in record_names:
                    label = identifier(definition.rsplit('::',1)[-1])
                    if label in record_names.values():
                        raise ValueError('Record class name collision')
                    record_names[definition] = label
                    reserve(label)
            if 'output_record' in settings:
                record = self.backend.record(settings['output_record'])
                if record['fields'] != [f['name'] for f in schema['outputs']]:
                    raise ValueError('Output record differs from named return tuple')
                schema['outputRecord'] = record
            for f in schema['outputs']: identifier(f['name'])
            source = directory/(name+'.c')
            self.backend.compile(schema['definition'],source)
            schema.update(source=source.name,sourceHash=digest(source))
            if checks := settings.get('checks'):
                check = self.backend.describe(checks)
                for f in check['inputs']:
                    f['name'] = aliases.get(f['name'],f['name'])
                    if f['name'] not in by_name or f['shape'] != by_name[f['name']]['shape']:
                        raise ValueError('Precondition input differs from calculation')
                check_source = directory/(name+'-checks.c')
                self.backend.compile(checks,check_source)
                check.update(source=check_source.name,sourceHash=digest(check_source))
                schema['checks'] = check
            manifest['exports'][name] = schema
            result = ''.join(p.capitalize() for p in name.split('_'))+'Result'
            emit_result(result, {'sysml_id':settings.get('output_record',schema['definition']+'::result'),
                                'fields':[f['name'] for f in schema['outputs']]})
            arguments, types = [], {}
            for f in schema['inputs']:
                type_name = record_names[f['record']['sysml_id']]+' | ArrayLike' if 'record' in f else ('ArrayLike' if f['shape'] else 'float')
                types[f['name']] = type_name
                arguments.append(f"{f['name']}: {type_name}" + (' | None = None' if 'default' in f else ''))
            prefix = ''.join(p.capitalize() for p in name.split('_'))
            shared_type, cases_type, calculation = prefix+'Inputs', prefix+'Cases', prefix+'Calculation'
            for label, batch in ((shared_type,False),(cases_type,True)):
                reserve(label)
                code.append(f'class {label}(TypedDict, total=False):')
                for f in schema['inputs']:
                    annotation = (('Sequence['+record_names[f['record']['sysml_id']]+'] | ArrayLike') if 'record' in f else 'ArrayLike') if batch else types[f['name']]
                    code.append(f"    {f['name']}: {annotation}")
                if not schema['inputs']: code.append('    pass')
                code.append('')
            reserve(calculation)
            signature = ('*, '+', '.join(arguments)) if arguments else ''
            forwarded = ', '.join(f"{f['name']}={f['name']}" for f in schema['inputs'])
            code += [f'class {calculation}(Calculation):',
                     f"    def __call__(self{', ' if signature else ''}{signature}) -> {result}:",
                     f"        return super().__call__({forwarded})",
                     f"    def prepare_inputs(self{', ' if signature else ''}{signature}) -> dict[str, NDArray[np.float64]]:",
                     f"        return super().prepare_inputs({forwarded})",
                     f"    def batch(self, *, shared: {shared_type}, cases: {cases_type}, chunk_size: int = 256, errors: Literal['raise', 'collect'] = 'raise') -> BatchResult:",
                     "        return super().batch(shared=shared, cases=cases, chunk_size=chunk_size, errors=errors)",
                     f"{name} = {calculation}(Path(__file__).with_name('manifest.json'), {name!r}, {result})", '']
        (directory/'__init__.py').write_text('\n'.join(code),encoding='utf-8')
        manifest['pythonHash'] = digest(directory/'__init__.py')
        (directory/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        return directory

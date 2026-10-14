"""Explicit project exports and generated Python entry points."""
import json
import keyword
import os
from pathlib import Path
import tomllib
from .backends.opensysml import OpenSysML, digest


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
        self.backend.__dict__.pop('_index', None)
        package = self.config.get('generated_package','generated')
        if any(not n.isidentifier() or keyword.iskeyword(n) for n in package.split('.')):
            raise ValueError('Invalid generated package')
        directory = self.root.joinpath(*package.split('.'))
        directory.mkdir(parents=True, exist_ok=True)
        manifest = {'schemaVersion':1,'sourceHashes':{str(p):digest(p) for p in self.backend.sources},
                    'compiler':{'path':str(self.backend.executable),'sha256':digest(self.backend.executable)},'exports':{}}
        code = ['# Generated from SysML. Do not edit.', 'from dataclasses import dataclass',
                'from pathlib import Path', 'from numpy.typing import ArrayLike',
                'from sysml_python.records import Record', 'from sysml_python.execution import Calculation', '']
        record_names, analyses = {}, {}
        def emit_record(label, record):
            identifier(label)
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
                    emit_record(label,record)
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
            emit_record(result, {'sysml_id':settings.get('output_record',schema['definition']+'::result'),
                                'fields':[f['name'] for f in schema['outputs']]})
            code += [f"_{name} = Calculation(Path(__file__).with_name('manifest.json'), {name!r}, {result})"]
            arguments = []
            for f in schema['inputs']:
                type_name = record_names[f['record']['sysml_id']]+' | ArrayLike' if 'record' in f else ('ArrayLike' if f['shape'] else 'float')
                arguments.append(f"{f['name']}: {type_name}" + (' = None' if 'default' in f else ''))
            code += [f"def {name}(*, {', '.join(arguments)}) -> {result}:",
                     f"    return _{name}("+', '.join(f"{f['name']}={f['name']}" for f in schema['inputs'])+')',
                     f'{name}.batch = _{name}.batch', f'{name}.prepare_inputs = _{name}.prepare_inputs', '']
        (directory/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        (directory/'__init__.py').write_text('\n'.join(code),encoding='utf-8')
        return directory

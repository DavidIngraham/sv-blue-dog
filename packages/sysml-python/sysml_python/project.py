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
        package = self.config.get('generated_package','generated')
        if any(not n.isidentifier() or keyword.iskeyword(n) for n in package.split('.')):
            raise ValueError('Invalid generated package')
        directory = self.root.joinpath(*package.split('.'))
        directory.mkdir(parents=True, exist_ok=True)
        exports = self.config['exports']
        manifest = {'schemaVersion':1,'sourceHashes':{str(p):digest(p) for p in self.backend.sources},
                    'compiler':{'path':str(self.backend.executable),'sha256':digest(self.backend.executable)},'exports':{}}
        code = ['# Generated from SysML. Do not edit.', 'from dataclasses import dataclass',
                'from pathlib import Path', 'from sysml_python.execution import Calculation', '']
        for name, settings in exports.items():
            identifier(name)
            if set(settings) != {'definition'}:
                raise ValueError(f'{name}: only definition is currently supported')
            schema = self.backend.describe(settings['definition'])
            for f in schema['inputs']+schema['outputs']: identifier(f['name'])
            source = directory/(name+'.c')
            self.backend.compile(schema['definition'], source)
            schema.update(source=source.name,sourceHash=digest(source))
            manifest['exports'][name] = schema
            result = ''.join(p.capitalize() for p in name.split('_'))+'Result'
            code += ['@dataclass(frozen=True)',f'class {result}:']
            code += [f"    {f['name']}: float" for f in schema['outputs']]
            code += ['',f"_{name} = Calculation(Path(__file__).with_name('manifest.json'), {name!r}, {result})"]
            arguments = [f['name'] + (f"={f['default']!r}" if 'default' in f else '') for f in schema['inputs']]
            code += [f"def {name}(*, {', '.join(arguments)}) -> {result}:",
                     f"    return _{name}("+', '.join(f"{f['name']}={f['name']}" for f in schema['inputs'])+')',
                     f'{name}.batch = _{name}.batch', '']
        (directory/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        (directory/'__init__.py').write_text('\n'.join(code),encoding='utf-8')
        return directory

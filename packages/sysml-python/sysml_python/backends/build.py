"""Meson-owned toolchain discovery and immutable native build snapshots."""
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from filelock import FileLock
from mesonbuild.coredata import version as meson_version

from ..provenance import digest


def _run(*args):
    command = [sys.executable, '-m', 'mesonbuild.mesonmain', *map(str, args)]
    env = os.environ.copy()
    # Console scripts from the active environment (notably Ninja) may not be on PATH.
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    if result.returncode:
        raise RuntimeError('Meson native build failed: ' + ' '.join(map(str, args)) + '\n' + result.stdout + result.stderr)
    return result.stdout


def _setup(build, source):
    # Explicit GNU/Clang toolchains must retain their own environment. Force
    # Visual Studio activation only for MSVC-style (or automatic) selection.
    compiler = os.environ.get('CC', '')
    activate = os.name == 'nt' and (not compiler or Path(compiler).stem.lower() in ('cl', 'clang-cl'))
    _run('setup', build, source, '--backend=ninja', *(('--vsenv',) if activate else ()))


def _info(directory, name):
    return json.loads((directory/'meson-info'/('intro-'+name+'.json')).read_text(encoding='utf-8'))


def _environment():
    return tuple((name, os.environ.get(name, '')) for name in
                 ('CC', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'PATH', 'INCLUDE', 'LIB', 'LIBPATH', 'SDKROOT', 'MACOSX_DEPLOYMENT_TARGET'))


@lru_cache(maxsize=8)
def _toolchain(environment):
    # Probe once per process/environment. Compiler identity participates in the cache key,
    # so an upgraded compiler cannot silently reuse an earlier process's binaries.
    with tempfile.TemporaryDirectory(prefix='sysml-toolchain-') as temporary:
        root = Path(temporary)
        (root/'meson.build').write_text("project('sysml_toolchain', 'c', default_options: ['c_std=c11'])\n", encoding='utf-8')
        build = root/'build'
        _setup(build, root)
        compilers = _info(build, 'compilers')['host']
        binaries = {}
        for compiler in compilers.values():
            for executable in compiler.get('exelist', []):
                path = shutil.which(executable)
                if path and Path(path).is_file():
                    binaries[str(Path(path).resolve())] = digest(path)
        return {'compilers': compilers, 'compilerBinaries': binaries,
                'machines': _info(build, 'machines'), 'mesonVersion': meson_version,
                'environment': dict(environment)}


def build_libraries(sources, *, dependencies=()):
    """Build all targets in one Meson project; return paths plus audited build metadata."""
    sources = tuple(dict.fromkeys(Path(p).resolve() for p in sources))
    if not sources:
        raise ValueError('At least one native source is required')
    paths = (*sources, *(Path(p).resolve() for p in dependencies))
    contents = {}
    for path in paths:
        data = path.read_bytes()
        if path.name in contents and contents[path.name] != data:
            raise ValueError('Conflicting native source basenames: '+path.name)
        contents[path.name] = data
    identity = _toolchain(_environment())
    recipe = ["project('sysml_kernels', 'c', default_options: ['c_std=gnu11,c11', 'optimization=2', 'debug=false'])",
              "cc = meson.get_compiler('c')", "math = cc.find_library('m', required: false)"]
    for i, source in enumerate(sources):
        if "'" in source.name or '\n' in source.name:
            raise ValueError('Unsupported native source filename')
        recipe.append(f"shared_library('kernel_{i}', '{source.name}', dependencies: math, vs_module_defs: 'exports.def', install: false)")
    recipe = '\n'.join(recipe)+'\n'
    exports = 'EXPORTS\nsysml_run\nsysml_error\nsysml_python_batch\n'
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()+recipe.encode()+exports.encode())
    for name, data in sorted(contents.items()):
        key.update(name.encode()+b'\0'+data)
    root = sources[0].parent/'.native'/key.hexdigest()[:32]
    root.mkdir(parents=True, exist_ok=True)
    with FileLock(str(root/'build.lock')):
        receipt = root/'receipt.json'
        if not receipt.exists():
            # Unique build directory also permits retry after a failed/interrupted build.
            build_source = Path(tempfile.mkdtemp(prefix='source-', dir=root))
            for name, data in contents.items():
                (build_source/name).write_bytes(data)
            (build_source/'meson.build').write_text(recipe, encoding='utf-8')
            (build_source/'exports.def').write_text(exports, encoding='utf-8')
            build = build_source/'build'
            _setup(build, build_source)
            _run('compile', '-C', build, '-j', os.environ.get('SYSML_BUILD_JOBS', '4'))
            targets = _info(build, 'targets')
            metadata = {**identity, 'platform': platform.system(), 'machine': platform.machine(),
                        'compilerTarget': _info(build, 'machines')['host'],
                        'compilerVersion': _info(build, 'compilers')['host']['c']['version'],
                        'buildOptions': _info(build, 'buildoptions'),
                        'recipeSha256': hashlib.sha256(recipe.encode()).hexdigest()}
            records = {}
            for i, source in enumerate(sources):
                target = next(t for t in targets if t['name'] == f'kernel_{i}')
                library = Path(target['filename'][0])
                records[source.name] = {'path': str(library.relative_to(root)),
                    'metadata': {**metadata, 'librarySha256': digest(library), 'target': target}}
            temporary = receipt.with_suffix('.tmp')
            temporary.write_text(json.dumps(records, indent=2), encoding='utf-8')
            os.replace(temporary, receipt)
        records = json.loads(receipt.read_text(encoding='utf-8'))
        result = {}
        for source in sources:
            record = records[source.name]
            library = root/record['path']
            if digest(library) != record['metadata']['librarySha256']:
                raise ValueError('Cached native library differs from build receipt: '+str(library))
            result[source] = (library, record['metadata'])
        return result

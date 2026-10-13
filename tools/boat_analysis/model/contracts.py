"""Generate numerical boundaries from the pinned OpenSysML API element export.

This is a deliberately narrow reader, not a SysML parser. Unsupported parameter
shapes and unnamed outputs fail preparation instead of inventing a schema.
"""
import json
from functools import lru_cache
from .runtime import ROOT, native
from ..evidence.records import digest


@lru_cache(maxsize=16)
def _elements(path, fingerprint):
    return json.loads(native('-convert', 'api-json', models=(path,)))


def describe(path, definition, *, named=True, inputs_only=False):
    elements = _elements(path, digest(path))
    by_id = {e['@id']: e for e in elements}
    resolve = lambda ref: by_id[ref['@id']]
    calculation = next(e for e in elements if e.get('qualifiedName') == definition)
    members = [resolve(r) for r in calculation['ownedMember']]
    arguments = []
    for feature in members:
        if feature.get('direction') != 'in':
            continue
        if len(feature.get('type', [])) != 1 or resolve(feature['type'][0]).get('qualifiedName') != 'ScalarValues::Real':
            raise ValueError(f'Unsupported numerical input: {definition}')
        shape = []
        if 'multiplicity' in feature:
            bound = resolve(feature['upperBound'])
            if bound['@type'] == 'LiteralInteger':
                shape = [bound['value']]
            elif bound['@type'] == 'LiteralInfinity':
                shape = [None]
            else:
                raise ValueError(f'Unresolved multiplicity: {definition}')
            if 'lowerBound' in feature and resolve(feature['lowerBound']).get('value') != shape[0]:
                raise ValueError(f'Variable multiplicity is unsupported: {definition}')
        arguments.append(dict(name=feature['declaredName'], shape=shape))
    if inputs_only:
        return arguments, []
    expression = members[-1]
    if expression.get('operator') != ',':
        raise ValueError(f'Expected explicit output tuple: {definition}')
    outputs = []
    for ref in expression['argument']:
        item = resolve(ref)
        if named:
            if item['@type'] != 'FeatureReferenceExpression':
                raise ValueError(f'Name the returned quantities in {definition}')
            outputs.append(resolve(item['referent'])['declaredName'])
        else:
            outputs.append(None)
    if named and len(set(outputs)) != len(outputs):
        raise ValueError(f'Duplicate output names: {definition}')
    return arguments, outputs


def compile_model(contract, name, *, path, definition, aliases, source, hash_key,
                  output_key=None, output_definition=None, defaults=None, records=None, checks=None):
    """Application wiring supplies aliases/defaults; the model supplies dimensions."""
    path = ROOT/path
    # Evaluate can delegate to Core, whose explicit output tuple defines labels.
    args, _ = describe(path, definition, inputs_only=True)
    _, outputs = describe(path, output_definition or definition, named=output_key is not None)
    if len(set(aliases.values())) != len(aliases) or set(aliases) != {a['name'] for a in args}:
        raise ValueError(f'{name}: aliases must cover exactly the model inputs')
    for arg in args:
        arg['name'] = aliases[arg['name']]
        if arg['shape'] == [None]:
            key = (defaults or {}).get(arg['name'])
            if key is None:
                raise ValueError(f'{name}: unbounded input needs a model-exported default')
            arg['shape'] = [len(contract[key])]
    generated = ROOT/'.tools'/source
    native('-compile', definition, '-source', '-o', str(generated))
    contract[hash_key] = digest(generated)
    entry = dict(source=generated.relative_to(ROOT).as_posix(), hashKey=hash_key,
                 arguments=args, outputs=outputs if output_key else None, outputSize=len(outputs),
                 defaults=defaults or {}, records=records or {})
    if output_key:
        contract[output_key] = outputs
    if checks:
        check_args, labels = describe(path, checks)
        check_source = generated.with_stem(generated.stem+'-checks')
        native('-compile', checks, '-source', '-o', str(check_source))
        entry['checks'] = dict(source=check_source.relative_to(ROOT).as_posix(),
            sourceHash=digest(check_source), arguments=[aliases[a['name']] for a in check_args], outputs=labels)
        shapes = {a['name']:a['shape'] for a in args}
        if any(a['shape'] != shapes[aliases[a['name']]] for a in check_args):
            raise ValueError('Precondition dimensions differ from calculation')
    contract.setdefault('kernels', {})[name] = entry
    return entry

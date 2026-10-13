"""OpenSysML semantic export and C compilation; no project conventions."""
import hashlib
import json
import math
import subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class OpenSysML:
    def __init__(self, executable, sources):
        self.executable = Path(executable).resolve()
        self.sources = tuple(Path(p).resolve() for p in sources)

    def run(self, *arguments):
        result = subprocess.run([str(self.executable), *map(str, self.sources), *map(str, arguments)],
                                capture_output=True, text=True, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(f'OpenSysML failed ({result.returncode}): {result.stdout}\n{result.stderr}')
        return result.stdout

    def elements(self):
        return json.loads(self.run('-convert', 'api-json'))

    def describe(self, definition):
        elements = self.elements()
        by_id = {e['@id']: e for e in elements}
        resolve = lambda r: by_id[r['@id']]
        matches = [e for e in elements if e.get('qualifiedName') == definition]
        if len(matches) != 1 or matches[0]['@type'] != 'CalculationDefinition':
            raise ValueError(f'Expected one calculation definition: {definition}')
        members = [resolve(r) for r in matches[0].get('ownedMember', [])]
        inputs, outputs = [], []
        for feature in members:
            if feature.get('direction') not in ('in','out'):
                continue
            if feature.get('direction') == 'out' and not feature.get('isResult'):
                continue
            types = feature.get('type', [])
            if len(types) != 1 or resolve(types[0]).get('qualifiedName') != 'ScalarValues::Real' or 'multiplicity' in feature:
                raise ValueError(f'{definition}: initial public export supports scalar Real only; unsupported feature {feature.get("declaredName")}')
            field = {'name': feature['declaredName']}
            if feature.get('direction') == 'in':
                if 'value' in feature:
                    if not feature.get('isDefault'):
                        raise ValueError('Bound input cannot be exposed as an overridable argument')
                    value = resolve(feature['value'])
                    if value['@type'] not in ('LiteralInteger', 'LiteralRational') or not isinstance(value.get('value'), (int, float)):
                        raise NotImplementedError(f'{definition}: nonliteral defaults require model evaluation')
                    if not math.isfinite(value['value']):
                        raise ValueError('Default must be finite')
                    field['default'] = value['value']
                inputs.append(field)
            else:
                outputs.append(field)
        if len(outputs) != 1:
            raise ValueError(f'{definition}: expected a named scalar return')
        return {'definition':definition, 'inputs':inputs, 'outputs':outputs}

    def compile(self, definition, output):
        # Python binds exported defaults before calling C. Remove only their
        # FeatureValues in a generated semantic projection, never in source text.
        elements = self.elements()
        by_id = {e['@id']: e for e in elements}
        calculation = next(e for e in elements if e.get('qualifiedName') == definition)
        removed = set()
        for ref in calculation.get('ownedMember', []):
            feature = by_id[ref['@id']]
            if feature.get('direction') != 'in' or not feature.get('isDefault'):
                continue
            value = by_id[feature['value']['@id']]
            removed.update((value['@id'], value['owningRelationship']['@id']))
            feature.pop('value'); feature.pop('isDefault')
            for key in ('ownedRelationship', 'ownedMembership'):
                feature[key] = [r for r in feature.get(key, []) if r['@id'] not in removed]
        if not removed:
            self.run('-compile', definition, '-source', '-o', output)
            return
        projection = Path(output).with_suffix('.api.json')
        projection.write_text(json.dumps([e for e in elements if e['@id'] not in removed]), encoding='utf-8')
        OpenSysML(self.executable, (projection,)).run('-compile', definition, '-source', '-o', output)

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

    def index(self):
        # A preparation snapshot; create a new backend when sources change.
        if not hasattr(self, '_index'):
            self._index = {e['@id']: e for e in self.elements()}
        return self._index

    def named(self, definition):
        matches = [e for e in self.index().values() if e.get('qualifiedName') == definition]
        if len(matches) != 1:
            raise ValueError(f'Expected one model element: {definition}')
        return matches[0]

    def members(self, definition):
        return [self.index()[r['@id']] for r in self.named(definition).get('ownedMember', [])]

    def real_shape(self, feature):
        resolve = lambda r: self.index()[r['@id']]
        types = feature.get('type', [])
        if len(types) != 1 or resolve(types[0]).get('qualifiedName') != 'ScalarValues::Real':
            raise ValueError(f"Unsupported numerical type: {feature.get('qualifiedName')}")
        if 'multiplicity' not in feature:
            return []
        upper = resolve(feature['upperBound'])
        if upper['@type'] == 'LiteralInfinity':
            return [None]
        if upper['@type'] != 'LiteralInteger' or upper['value'] < 1:
            raise ValueError('Numerical vector needs a positive fixed multiplicity')
        if 'lowerBound' in feature and resolve(feature['lowerBound']).get('value') != upper['value']:
            raise ValueError('Variable multiplicity is not a fixed vector')
        return [upper['value']]

    def record(self, definition):
        fields = [e for e in self.members(definition) if e['@type'] == 'AttributeUsage']
        if not fields or any(self.real_shape(e) for e in fields):
            raise ValueError(f'{definition}: record requires scalar Real attributes')
        return {'sysml_id': definition, 'fields': [e['declaredName'] for e in fields]}

    def describe(self, definition, *, output_definition=None):
        if self.named(definition)['@type'] != 'CalculationDefinition':
            raise ValueError(f'Expected a calculation: {definition}')
        members = self.members(definition)
        inputs = []
        for feature in members:
            if feature.get('direction') != 'in':
                continue
            field = {'name':feature['declaredName'], 'shape':self.real_shape(feature)}
            if 'value' in feature:
                if not feature.get('isDefault'):
                    raise ValueError('Bound input cannot be exposed as an overridable argument')
                value = self.index()[feature['value']['@id']]
                if value['@type'] not in ('LiteralInteger', 'LiteralRational') or not isinstance(value.get('value'), (int, float)):
                    raise NotImplementedError(f'{definition}: nonliteral parameter defaults require model evaluation')
                if not math.isfinite(value['value']):
                    raise ValueError('Default must be finite')
                field['default'] = value['value']
            inputs.append(field)
        members = self.members(output_definition or definition)
        results = [e for e in members if e.get('isResult')]
        if len(results) != 1:
            raise ValueError(f'{definition}: expected one declared return')
        shape = self.real_shape(results[0])
        if not shape:
            outputs = [{'name':results[0]['declaredName']}]
        else:
            expression = members[-1]
            if expression.get('operator') != ',':
                raise ValueError(f'{definition}: vector return needs an explicit named tuple or output_definition')
            outputs = []
            for ref in expression['argument']:
                item = self.index()[ref['@id']]
                if item['@type'] != 'FeatureReferenceExpression':
                    raise ValueError(f'{definition}: name each returned quantity')
                outputs.append({'name':self.index()[item['referent']['@id']]['declaredName']})
            if shape[0] is not None and shape[0] != len(outputs):
                raise ValueError('Return multiplicity differs from named tuple')
        if len({f['name'] for f in outputs}) != len(outputs):
            raise ValueError('Duplicate output names')
        return {'definition':definition, 'inputs':inputs, 'outputs':outputs}

    def analysis_values(self, definition):
        from fractions import Fraction
        import re
        report = json.loads(self.run('-analysis', definition, '-json'))
        if report.get('status') != 'holds':
            raise ValueError(f'Model default evaluation failed: {definition}')
        def value(text):
            return json.loads(re.sub(r'(-?\d+)/(\d+)', lambda m: str(float(Fraction(m[0]))), text))
        return {v['name']:value(v['value']) for v in report['checks'][0]['values']}

    def compile(self, definition, output):
        # Python binds exported defaults before calling C. Remove only their
        # FeatureValues in a generated semantic projection, never in source text.
        if not any(f.get('direction') == 'in' and f.get('isDefault')
                   for f in self.members(definition)):
            self.run('-compile', definition, '-source', '-o', output)
            return
        from copy import deepcopy
        elements = deepcopy(list(self.index().values()))
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

"""Resolve declarative study intent and delegate computation to native SysML."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

from .config import Assumption, Selector, StudyConfig, load_study, validate_study


class StudyResolutionError(ValueError):
    """A selection or binding cannot be resolved unambiguously from the model."""


class StudyExecutionError(RuntimeError):
    """Native execution failed; report retains completed and partial native results."""

    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


class StudyObjectivesError(RuntimeError):
    """Native objectives did not hold where required; all results remain inspectable."""

    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


def _equals(property_name: str, value: str) -> dict[str, Any]:
    return {'@type': 'PrimitiveConstraint', 'operator': '=',
            'property': property_name, 'value': [value]}


def _exact(model: Any, element_id: str, path: str) -> Any:
    # find(short_name) chooses a first declaration; exact get cannot do that.
    try:
        symbol = model.get(element_id)
    except Exception as error:
        raise StudyResolutionError(f'{path}: native lookup of {element_id!r} failed: {error}') from error
    if symbol is None or symbol.id != element_id:
        raise StudyResolutionError(f'{path}: no exact native element ID {element_id!r}')
    return symbol


def resolve_selector(model: Any, selector: Selector | dict[str, Any], *, path: str = 'select') -> list[str]:
    if not isinstance(selector, Selector):
        selector = Selector.model_validate(selector)
    if selector.id is not None:
        ids = [_exact(model, selector.id, path+'.id').id]
    else:
        constraints = [_equals('@type', selector.kind)]
        for field in ('owner', 'type', 'general'):
            value = getattr(selector, field)
            if value is not None:
                _exact(model, value, path+'.'+field)
                constraints.append(_equals(field, value))
        where = constraints[0] if len(constraints) == 1 else {
            '@type': 'CompositeConstraint', 'operator': 'and', 'constraint': constraints}
        try:
            ids = sorted({row.id for row in model.query(where=where)})
        except Exception as error:
            raise StudyResolutionError(f'{path}: native selection failed: {error}') from error
    if not ids:
        raise StudyResolutionError(f'{path}: no native elements matched {selector.model_dump(exclude_none=True)}')
    if selector.cardinality == 'one' and len(ids) != 1:
        raise StudyResolutionError(f'{path}: expected one native element; matched {len(ids)}: {ids}')
    return ids


def _native_json(value: Any) -> Any:
    """JSON projection of native values; no objective or equation is recomputed."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, dict):
        return {str(key): _native_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_native_json(item) for item in value]
    from opensysml.verdict import CaseEvaluation
    if isinstance(value, CaseEvaluation):
        return {name: _native_json(getattr(value, name)) for name in
                ('function_id', 'arguments', 'result', 'error', 'selected', 'tied')}
    if is_dataclass(value):
        return _native_json(asdict(value))
    if hasattr(value, '_pb'):
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(value._pb, preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)
    # Quantity and Unit are native client types, whose units must survive export.
    from opensysml.values import Quantity
    if isinstance(value, Quantity):
        return {'magnitude': _native_json(value.magnitude), 'unit': _native_json(value.unit)}
    if isinstance(value, Exception):
        return {'error': type(value).__name__, 'message': str(value)}
    raise TypeError(f'Unsupported native JSON value {type(value).__name__}')


def _output_errors(value: Any, path: str = 'outputs', seen: set[int] | None = None) -> list[str]:
    """The client can retain unsupported/error-valued outputs instead of raising."""
    if isinstance(value, Exception):
        return [f'{path}: {type(value).__name__}: {value}']
    if value is None or isinstance(value, (str, bool, int, float, Fraction)):
        return []
    seen = set() if seen is None else seen
    if id(value) in seen:
        return []
    seen.add(id(value))
    if isinstance(value, dict):
        return [error for key, item in value.items() for error in _output_errors(item, path+'.'+str(key), seen)]
    if isinstance(value, (list, tuple)):
        return [error for index, item in enumerate(value) for error in _output_errors(item, f'{path}.{index}', seen)]
    from opensysml.instance import Instance
    if isinstance(value, Instance):
        return _output_errors(value.features, path, seen)
    return []


def _native_report(result: Any) -> dict[str, Any]:
    return {'outputs': _native_json(result.outputs),
            'verdicts': [_native_json(item) for item in result.verdicts],
            'instances': [_native_json(item) for item in result.instances],
            'diagnostics': [_native_json(item) for item in result.diagnostics],
            'verifications': [_native_json(item) for item in result.verifications],
            'evaluations': [_native_json(item) for item in result.evaluations],
            'standing': _native_json(result.standing)}


def _attributes(model: Any, case_id: str) -> dict[str, Any]:
    # The service exposes resolved own/inherited attributes, not a complete
    # analysis parameter-direction schema. Native execution owns that check.
    try:
        return {fact.name: fact for fact in _exact(model, case_id, case_id).attribute_facts()}
    except Exception as error:
        raise StudyResolutionError(f'{case_id}: native attribute discovery failed: {error}') from error


def _check_arguments(arguments: dict[str, Assumption], facts: dict[str, Any], path: str) -> None:
    for name, assumption in arguments.items():
        location = path+'.arguments.'+name
        if name not in facts:
            raise StudyResolutionError(f'{location}: no native attribute named {name!r}')
        fact = facts[name]
        native_type = fact.type
        value = assumption.value
        valid = ((native_type == 'ScalarValues::Boolean' and type(value) is bool)
                 or (native_type == 'ScalarValues::String' and type(value) is str)
                 or (native_type == 'ScalarValues::Integer' and type(value) is int)
                 or (native_type == 'ScalarValues::Natural' and type(value) is int and value >= 0)
                 or (native_type in ('ScalarValues::Real', 'ScalarValues::Rational', 'ScalarValues::Number') and type(value) in (int, float)))
        if not valid:
            raise StudyResolutionError(f'{location}: supplied {type(value).__name__} is unsupported for native type {fact.type!r}; scalar Boolean/String/Integer/Natural/Real/Rational/Number only')
        if fact.unit:
            # Dimensional native values need Quantity/Unit binding support;
            # bare numbers plus a YAML label must not masquerade as quantities.
            raise StudyResolutionError(f'{location}: native quantity [{fact.unit}] is unsupported by scalar scenario bindings; bind the value in SysML')


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def _label(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)


def _provenance(config: StudyConfig, model: Any, files: tuple[Path, ...]) -> dict[str, Any]:
    from ..model.runtime import ROOT
    from ..model.install import REVISION, binary_path
    normalized = json.dumps(config.model_dump(), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    drivers = [Path(__file__), Path(__file__).with_name('config.py'), Path(__file__).with_name('__init__.py'),
               ROOT/'tools/boat_analysis/model/runtime.py', ROOT/'tools/boat_analysis/model/install.py',
               ROOT/'pyproject.toml', ROOT/'uv.lock']
    return {'configuration': {'path': str(config._source_path) if config._source_path else None,
                              'sha256': config._source_sha256,
                              'validatedSha256': hashlib.sha256(normalized).hexdigest()},
            'modelHash': model.hash,
            'sourceHashes': {_label(path, ROOT): _digest(path) for path in files},
            'driverHashes': {_label(path, ROOT): _digest(path) for path in drivers},
            'runtimeRevision': REVISION,
            'executableSha256': hashlib.sha256(binary_path('sysml-grpc').read_bytes()).hexdigest(),
            'sourceRevision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'sourceTreeModified': bool(subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=ROOT, text=True).strip()),
            'groups': [],
            'interpretation': 'Native analysis execution and explicitly supplied assumptions. Native objective verdicts are preserved; software results do not establish physical qualification. Scalar unit labels are provenance only; no conversion or dimension check is inferred.'}


def run_study(config_or_path: StudyConfig | str | Path | dict[str, Any], *, model: Any = None,
              models: Any = None) -> dict[str, Any]:
    """Validate, resolve all bindings, then execute native analyses deterministically.

    Failed assertions remain native results. Execution errors and required
    objectives that do not hold raise different exceptions carrying ``report``.
    """
    if isinstance(config_or_path, (str, Path)):
        config = load_study(config_or_path)
    elif isinstance(config_or_path, StudyConfig):
        # Revalidation catches mutations of an already constructed configuration.
        config = validate_study(config_or_path.model_dump())
        config._source_path = config_or_path._source_path
        config._source_sha256 = config_or_path._source_sha256
    else:
        config = validate_study(config_or_path)
    if config._source_path is not None:
        actual = hashlib.sha256(config._source_path.read_bytes()).hexdigest()
        if actual != config._source_sha256:
            raise StudyResolutionError(f'{config._source_path}: study file changed after validation; reload the configuration')
    from ..model.runtime import ROOT, load_model, model_files
    before_loading = None
    if model is None:
        files = tuple(Path(p).resolve() for p in (model_files() if models is None else models))
        before_loading = {_label(path, ROOT): _digest(path) for path in files}
        model = load_model(files)
    else:
        files = tuple(Path(p).resolve() for p in (models if models is not None else model.documents))
        if not files or any(not path.is_file() for path in files):
            raise StudyResolutionError('model: injected native model requires all source files for verified provenance; supply models= with the original source files')
        # A native snapshot is immutable even when the files it came from change.
        # Reusing it must not attach newer on-disk hashes to the older model.
        before_loading = {_label(path, ROOT): _digest(path) for path in files}
        pinned_model = load_model(files)
        if pinned_model.hash != model.hash:
            raise StudyResolutionError('model: injected native snapshot differs from the supplied source files')
        if model.connection is not pinned_model.connection:
            raise StudyResolutionError('model: injected native snapshot uses a different connection from the pinned local runtime; load it with model.runtime.load_model')
    provenance = _provenance(config, model, files)
    if before_loading != provenance['sourceHashes']:
        raise StudyResolutionError('Model sources changed while the native model was loading')
    report: dict[str, Any] = {'name': config.name, 'schemaVersion': config.schema_version,
                              'nativeAnalyses': {}, 'nativeOutputs': {}, 'provenance': provenance}
    plan = []
    for group_index, group in enumerate(config.groups):
        group_path = f"{config._source_path or '<study>'}: groups.{group_index}"
        case_ids = resolve_selector(model, group.select, path=group_path+'.select')
        subject = resolve_selector(model, group.subject, path=group_path+'.subject')[0] if group.subject else None
        resolved = {'name': group.name, 'analyses': case_ids, 'subject': subject, 'runs': []}
        provenance['groups'].append(resolved)
        for scenario_index, scenario in enumerate(group.scenarios):
            scenario_path = f'{group_path}.scenarios.{scenario_index}'
            for case_id in case_ids:
                native_rows = model.query(where=_equals('@id', case_id))
                if len(native_rows) != 1 or native_rows[0].type not in ('AnalysisCaseUsage', 'AnalysisCaseDefinition'):
                    raise StudyResolutionError(f'{group_path}.select: {case_id!r} is not a native analysis case')
                facts = _attributes(model, case_id)
                _check_arguments(scenario.arguments, facts, scenario_path)
                key = '/'.join((group.name, scenario.name, case_id))
                if key in {item[0] for item in plan}:
                    raise StudyResolutionError(f'{scenario_path}: duplicate run key {key!r}; avoid ambiguous slash-separated names')
                run = {'key': key, 'case': case_id, 'scenario': scenario.name,
                       'arguments': {name: value.model_dump() for name, value in scenario.arguments.items()},
                       'attributes': [_native_json(fact) for fact in facts.values()]}
                resolved['runs'].append(run)
                plan.append((key, case_id, subject, scenario, group.require_holds, scenario_path))
    failures = []
    objectives = []
    for key, case_id, subject, scenario, require_holds, path in plan:
        result = None
        error_message = ''
        try:
            result = model.run_analysis(case_id, subject=subject,
                named_arguments={name: assumption.value for name, assumption in scenario.arguments.items()} or None)
        except Exception as error:
            result = getattr(error, 'result', None)
            error_message = f'{path} ({case_id}): native execution failed: {type(error).__name__}: {error}'
        if result is not None:
            try:
                report['nativeOutputs'][key] = _native_json(result.outputs)
                report['nativeAnalyses'][key] = _native_report(result)
            except Exception as error:
                failures.append(f'{path} ({case_id}): native result export failed: {type(error).__name__}: {error}')
                provenance.setdefault('projectionErrors', {})[key] = str(result)
            native_errors = ([verdict.error for verdict in result.verdicts if verdict.error]
                             + [item.error for item in result.evaluations if item.error]
                             + [str(item) for item in result.diagnostics if item.severity.lower() == 'error']
                             + _output_errors(result.outputs))
            if native_errors:
                error_message = f'{path} ({case_id}): native verdict evaluation error: '+ '; '.join(native_errors)
            elif require_holds and not result:
                objectives.append(f'{path} ({case_id}): required native objectives did not hold')
        elif not error_message:
            error_message = f'{path} ({case_id}): native execution returned no result'
        if error_message:
            failures.append(error_message)
    # Sources and driver bytes are checked again so a run cannot present stale
    # hashes when input files change during native execution.
    for label, expected in provenance['sourceHashes'].items():
        path = Path(label)
        try:
            current = _digest(path if path.is_absolute() else ROOT/path)
        except OSError as error:
            failures.append(f'Source became unreadable during study execution: {label}: {error}')
            continue
        if current != expected:
            failures.append('Source changed during study execution: '+label)
    for label, expected in provenance['driverHashes'].items():
        path = Path(label)
        try:
            current = _digest(path if path.is_absolute() else ROOT/path)
        except OSError as error:
            failures.append(f'Driver became unreadable during study execution: {label}: {error}')
            continue
        if current != expected:
            failures.append('Driver changed during study execution: '+label)
    if config._source_path is not None:
        try:
            if hashlib.sha256(config._source_path.read_bytes()).hexdigest() != config._source_sha256:
                failures.append('Study configuration changed during execution: '+str(config._source_path))
        except OSError as error:
            failures.append(f'Study configuration became unreadable during execution: {config._source_path}: {error}')
    provenance['executionErrors'] = failures
    provenance['requiredObjectivesNotHeld'] = objectives
    if failures:
        raise StudyExecutionError('; '.join(failures), report)
    if objectives:
        raise StudyObjectivesError('; '.join(objectives), report)
    return report

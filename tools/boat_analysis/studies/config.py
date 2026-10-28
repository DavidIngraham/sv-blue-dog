"""Validated study intent; model semantics remain in SysML."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, StringConstraints, ValidationError, field_validator, model_validator
import yaml


Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ArgumentName = Annotated[str, StringConstraints(min_length=1)]
Scalar = bool | int | Annotated[float, Field(allow_inf_nan=False)] | str


class StudyConfigError(ValueError):
    """A study file is unsafe, malformed or outside the versioned schema."""


class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', validate_default=True)


class Selector(StrictModel):
    """Exact native identity or an intersection of native semantic properties."""

    id: Text | None = None
    kind: Text | None = None
    owner: Text | None = None
    type: Text | None = None
    general: Text | None = None
    cardinality: Literal['one', 'many'] = 'one'

    @model_validator(mode='after')
    def selection_form(self) -> Self:
        filters = (self.kind, self.owner, self.type, self.general)
        if self.id is not None:
            if any(value is not None for value in filters):
                raise ValueError('id cannot be combined with kind/owner/type/general')
        elif self.kind is None:
            raise ValueError('supply exact id or kind with optional owner/type/general')
        return self


class Assumption(StrictModel):
    """An explicit external scalar, never a model equation or expression."""

    value: Scalar
    rationale: Text
    unit: Text | None = None


class Scenario(StrictModel):
    name: Text = 'default'
    arguments: dict[ArgumentName, Assumption] = Field(default_factory=dict)


class AnalysisGroup(StrictModel):
    name: Text
    select: Selector
    subject: Selector | None = None
    scenarios: Annotated[list[Scenario], Field(min_length=1)] = Field(default_factory=lambda: [Scenario()])
    require_holds: bool = True

    @model_validator(mode='after')
    def distinct_scenarios_and_subject(self) -> Self:
        names = [scenario.name for scenario in self.scenarios]
        if len(names) != len(set(names)):
            raise ValueError('scenario names must be unique within the group')
        if self.subject is not None and self.subject.cardinality != 'one':
            raise ValueError('subject requires cardinality one')
        return self


class StudyConfig(StrictModel):
    schema_version: Literal[1]
    name: Text
    groups: Annotated[list[AnalysisGroup], Field(min_length=1)]
    _source_path: Path | None = PrivateAttr(default=None)
    _source_sha256: str | None = PrivateAttr(default=None)

    @field_validator('schema_version', mode='before')
    @classmethod
    def integer_version(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError('schema_version must be integer 1')
        return value

    @model_validator(mode='after')
    def distinct_groups(self) -> Self:
        names = [group.name for group in self.groups]
        if len(names) != len(set(names)):
            raise ValueError('group names must be unique')
        return self


class _UniqueSafeLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        # Reject merges rather than letting them obscure duplicate bindings.
        result = {}
        for key_node, value_node in node.value:
            if key_node.tag == 'tag:yaml.org,2002:merge':
                raise StudyConfigError(f'line {key_node.start_mark.line+1}: YAML merge keys are unsupported')
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise StudyConfigError(f'line {key_node.start_mark.line+1}: mapping keys must be strings')
            if key in result:
                raise StudyConfigError(f'line {key_node.start_mark.line+1}: duplicate mapping key {key!r}')
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def validate_study(value: object, *, source: str = '<study>') -> StudyConfig:
    """Validate every configuration field before a native model is loaded."""
    try:
        return StudyConfig.model_validate(value)
    except ValidationError as error:
        details = '; '.join('.'.join(map(str, item['loc'])) + ': ' + item['msg']
                            for item in error.errors(include_url=False))
        raise StudyConfigError(f'{source}: {details}') from error


def load_study(path: str | Path) -> StudyConfig:
    path = Path(path).resolve()
    raw = path.read_bytes()
    try:
        value = yaml.load(raw.decode('utf-8'), Loader=_UniqueSafeLoader)
    except (yaml.YAMLError, UnicodeError, StudyConfigError) as error:
        raise StudyConfigError(f'{path}: {error}') from error
    config = validate_study(value, source=str(path))
    config._source_path = path
    config._source_sha256 = hashlib.sha256(raw).hexdigest()
    return config

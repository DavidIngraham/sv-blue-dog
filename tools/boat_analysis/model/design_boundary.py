"""Named model records cross Python boundaries; only this adapter packs arrays."""
from collections.abc import Sequence, Mapping
from typing import Protocol, TypeVar
import numpy as np
from tools.boat_analysis.generated import Design, Parameters


class NumericalRecord(Protocol):
    def to_mapping(self) -> Mapping[str, object]: ...

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]): ...


T = TypeVar("T", bound=NumericalRecord)


def pack(record: NumericalRecord, names: Sequence[str]) -> np.ndarray:
    values = record.to_mapping()
    if len(names) != len(set(names)) or set(names) != set(values):
        raise ValueError("Native input order differs from the generated model fields")
    return np.ascontiguousarray([values[name] for name in names], dtype=float)


def unpack(record_type: type[T], values, names: Sequence[str]) -> T:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (len(names),) or len(set(names)) != len(names):
        raise ValueError("Native vector shape or field order is invalid")
    return record_type.from_mapping(dict(zip(names, vector.tolist(), strict=True)))


def design_vector(value, contract):
    return pack(value, contract['designNames']) if isinstance(value, Design) else value


def parameter_vector(value, contract):
    return pack(value, contract['parameterNames']) if isinstance(value, Parameters) else value

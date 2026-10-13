"""Named model records cross Python boundaries; only this adapter packs arrays."""
from collections.abc import Sequence
import numpy as np
from .design_types import Design, Parameters


def pack(record: Design | Parameters, names: Sequence[str]) -> np.ndarray:
    values = record.to_mapping()
    if len(names) != len(set(names)) or set(names) != set(values):
        raise ValueError("Native input order differs from the generated model fields")
    return np.ascontiguousarray([values[name] for name in names], dtype=float)


def unpack(record_type: type[Design] | type[Parameters], values, names: Sequence[str]):
    vector = np.asarray(values, dtype=float)
    if vector.shape != (len(names),) or len(set(names)) != len(names):
        raise ValueError("Native vector shape or field order is invalid")
    return record_type.from_mapping(dict(zip(names, vector.tolist(), strict=True)))


def design_vector(value, contract):
    return pack(value, contract['designNames']) if isinstance(value, Design) else value


def parameter_vector(value, contract):
    return pack(value, contract['parameterNames']) if isinstance(value, Parameters) else value

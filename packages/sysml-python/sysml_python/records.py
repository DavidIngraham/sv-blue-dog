"""Named records at the public boundary; vectors belong to the backend."""
from collections.abc import Mapping
from dataclasses import fields
import numpy as np
from numbers import Real
from math import isfinite


def from_array(cls, values):
    """Decode a numerical vector in the generated record's declaration order."""
    names = [f.metadata.get('sysml_name', f.name) for f in fields(cls)]
    array = np.asarray(values)
    if array.shape != (len(names),):
        raise ValueError(f'{cls.__name__}: expected vector of length {len(names)}')
    return cls.from_mapping(dict(zip(names, array, strict=True)))


def as_array(record):
    """Copy a model record's values at the NumPy boundary."""
    return np.asarray(tuple(record.to_mapping().values()), dtype=float)


class Record(Mapping):
    sysml_id: str

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(f'{field.name}: expected a Real number')
            if not isfinite(value):
                raise ValueError(f'{field.name}: expected a finite Real')
            object.__setattr__(self, field.name, float(value))

    def to_mapping(self):
        return {f.name:getattr(self, f.name) for f in fields(self)}

    def as_array(self):
        """Copy model-ordered values for a NumPy algorithm."""
        return as_array(self)

    @classmethod
    def from_mapping(cls, values):
        return cls(**values)

    @classmethod
    def from_array(cls, values):
        """Decode a numerical vector in generated model field order."""
        return from_array(cls, values)

    def __getitem__(self, name):
        if name not in {f.name for f in fields(self)}:
            raise KeyError(name)
        return getattr(self, name)

    def __iter__(self):
        return (f.name for f in fields(self))

    def __len__(self):
        return len(fields(self))

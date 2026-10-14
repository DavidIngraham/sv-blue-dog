"""Named records at the public boundary; vectors belong to the backend."""
from collections.abc import Mapping
from dataclasses import fields
import numpy as np


class Record(Mapping):
    sysml_id: str

    def to_mapping(self):
        return {f.name:getattr(self, f.name) for f in fields(self)}

    def as_array(self):
        """Copy model-ordered values for a NumPy algorithm."""
        return np.asarray(tuple(self.values()), dtype=float)

    @classmethod
    def from_mapping(cls, values):
        return cls(**values)

    def __getitem__(self, name):
        if name not in {f.name for f in fields(self)}:
            raise KeyError(name)
        return getattr(self, name)

    def __iter__(self):
        return (f.name for f in fields(self))

    def __len__(self):
        return len(fields(self))

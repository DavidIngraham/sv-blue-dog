"""Small, serial ABI adapter for the pinned OpenSysML C sequence interface."""
import ctypes as ct
import hashlib
import json
import subprocess
import threading
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
_RUNTIME_LOCK = threading.Lock()


class Sequence(ct.Structure):
    _fields_ = [("shape", ct.c_int8), ("length", ct.c_int64), ("data", ct.POINTER(ct.c_double))]


class Kernel:
    def __init__(self):
        self.contract = json.loads((ROOT / ".tools/design-search-contract.json").read_text())
        for name, digest in self.contract["sourceHashes"].items():
            if hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() != digest:
                raise ValueError("Stale native contract: " + name)
        source = ROOT / ".tools/design-physics.c"
        if hashlib.sha256(source.read_bytes()).hexdigest() != self.contract["generatedCHash"]:
            raise ValueError("Compiled-source provenance mismatch")
        library = ROOT / ".tools/design-physics.so"
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", str(source), "-lm", "-o", str(library)], check=True)
        self.lib = ct.CDLL(str(library))
        self.lib.sysml_run.argtypes = [Sequence, Sequence, Sequence, ct.POINTER(Sequence)]
        self.lib.sysml_run.restype = ct.c_int
        self.lib.sysml_error.restype = ct.c_char_p
        self.parameters = np.asarray(self.contract["parameterValues"], dtype=np.float64)
        self.lock = _RUNTIME_LOCK

    def evaluate(self, design, scenario):
        arrays = [np.ascontiguousarray(a, dtype=np.float64) for a in (design, self.parameters, scenario)]
        if [a.size for a in arrays] != [len(self.contract["designNames"]), len(self.contract["parameterNames"]), 9]:
            raise ValueError("Invalid kernel input shape")
        if any(a.ndim != 1 or not np.isfinite(a).all() for a in arrays):
            raise ValueError("Nonfinite or multidimensional kernel input")
        args = [Sequence(2, a.size, a.ctypes.data_as(ct.POINTER(ct.c_double))) for a in arrays]
        with self.lock:
            output = Sequence()
            if self.lib.sysml_run(*args, ct.byref(output)):
                raise ValueError(self.lib.sysml_error().decode())
            if output.length != len(self.contract["outputNames"]):
                raise ValueError("Native output contract mismatch")
            # Copy before the next call releases the generated runtime's allocation arena.
            result = np.ctypeslib.as_array(output.data, shape=(output.length,)).copy()
        if not np.isfinite(result).all():
            raise ValueError("Nonfinite native output")
        return result

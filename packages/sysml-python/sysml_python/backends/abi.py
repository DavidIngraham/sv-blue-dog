"""The pinned OpenSysML homogeneous Real sequence ABI."""
import ctypes as ct


class Sequence(ct.Structure):
    _fields_ = [("shape", ct.c_int8), ("length", ct.c_int64), ("data", ct.POINTER(ct.c_double))]

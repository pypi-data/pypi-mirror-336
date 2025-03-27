from __future__ import annotations
import desbordante.fd

__all__ = [
    "Aid",
    "DFD",
    "Default",
    "Depminer",
    "EulerFD",
    "FDep",
    "FUN",
    "FastFDs",
    "FdMine",
    "HyFD",
    "PFDTane",
    "Pyro",
    "Tane",
]

class Aid(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    """
    def __init__(self) -> None: ...

class DFD(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class Depminer(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class EulerFD(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    custom_random_seed: seed for the custom random generator. Used for consistency of results across platforms.
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class FDep(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    """
    def __init__(self) -> None: ...

class FUN(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class FastFDs(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class FdMine(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class HyFD(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class PFDTane(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    error: error threshold value for Approximate FD algorithms
    is_null_equal_null: specify whether two NULLs should be considered equal
    pfd_error_measure: PFD error measure to use
    [per_tuple|per_value]
    """
    def __init__(self) -> None: ...

class Pyro(desbordante.fd.FdAlgorithm):
    """
    Options:
    error: error threshold value for Approximate FD algorithms
    is_null_equal_null: specify whether two NULLs should be considered equal
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    seed: RNG seed
    """
    def __init__(self) -> None: ...

class Tane(desbordante.fd.FdAlgorithm):
    """
    Options:
    max_lhs: max considered LHS size
    table: table processed by the algorithm
    error: error threshold value for Approximate FD algorithms
    is_null_equal_null: specify whether two NULLs should be considered equal
    afd_error_measure: AFD error measure to use
    [g1|pdep|tau|mu_plus|rho]
    """
    def __init__(self) -> None: ...

Default = HyFD

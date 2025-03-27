from __future__ import annotations
import desbordante.ucc

__all__ = ["Default", "HPIValid", "HyUCC", "PyroUCC"]

class HPIValid(desbordante.ucc.UccAlgorithm):
    """
    Options:
    table: table processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class HyUCC(desbordante.ucc.UccAlgorithm):
    """
    Options:
    table: table processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    is_null_equal_null: specify whether two NULLs should be considered equal
    """
    def __init__(self) -> None: ...

class PyroUCC(desbordante.ucc.UccAlgorithm):
    """
    Options:
    table: table processed by the algorithm
    error: error threshold value for Approximate FD algorithms
    seed: RNG seed
    is_null_equal_null: specify whether two NULLs should be considered equal
    max_lhs: max considered LHS size
    """
    def __init__(self) -> None: ...

Default = HPIValid

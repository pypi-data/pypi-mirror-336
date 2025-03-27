from __future__ import annotations
import desbordante.ind

__all__ = ["Default", "Faida", "Mind", "Spider"]

class Faida(desbordante.ind.IndAlgorithm):
    """
    Options:
    tables: table collection processed by the algorithm
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    hll_accuracy: HyperLogLog approximation accuracy. Must be positive
    Closer to 0 - higher accuracy, more memory needed and slower the algorithm.

    max_arity: max considered arity
    ignore_null_cols: Ignore INDs which contain columns filled only with NULLs. May increase performance but impacts the result. [true|false]
    sample_size: Size of a table sample. Greater value - more correct answers, but higher memory consumption.
     Applies to all tables
    ignore_constant_cols: Ignore INDs which contain columns filled with only one value. May increase performance but impacts the result. [true|false]
    """
    def __init__(self) -> None: ...

class Mind(desbordante.ind.IndAlgorithm):
    """
    Options:
    tables: table collection processed by the algorithm
    error: error threshold value for Approximate FD algorithms
    max_arity: max considered arity
    """
    def __init__(self) -> None: ...

class Spider(desbordante.ind.IndAlgorithm):
    """
    Options:
    tables: table collection processed by the algorithm
    is_null_equal_null: specify whether two NULLs should be considered equal
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    error: error threshold value for Approximate FD algorithms
    mem_limit: memory limit im MBs
    """
    def __init__(self) -> None: ...

Default = Spider

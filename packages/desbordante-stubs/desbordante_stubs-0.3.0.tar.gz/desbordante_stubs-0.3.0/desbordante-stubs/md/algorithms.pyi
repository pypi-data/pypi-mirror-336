from __future__ import annotations
import desbordante.md

__all__ = ["Default", "HyMD"]

class HyMD(desbordante.md.MdAlgorithm):
    """
    Options:
    right_table: second table processed by the algorithm
    left_table: first table processed by the algorithm
    min_support: minimum support for a dependency's LHS
    column_matches: column matches to examine
    level_definition: MD lattice level definition to use
    [cardinality|lattice]
    prune_nondisjoint: don't search for dependencies where the LHS decision boundary at the same index as the RHS decision boundary limits the number of records matched
    max_cardinality: maximum number of MD matching classifiers
    threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
    """
    def __init__(self) -> None: ...

Default = HyMD

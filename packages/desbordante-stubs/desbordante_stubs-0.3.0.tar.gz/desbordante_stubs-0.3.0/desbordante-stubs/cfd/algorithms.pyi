from __future__ import annotations
import desbordante.cfd

__all__ = ["Default", "FDFirst"]

class FDFirst(desbordante.cfd.CfdAlgorithm):
    """
    Options:
    columns_number: Number of columns in the part of the dataset if you want to use algo not on the full dataset, but on its part
    tuples_number: Number of tuples in the part of the dataset if you want to use algo not on the full dataset, but on its part
    cfd_minsup: minimum support value (integer number between 1 and number of tuples in dataset)
    table: table processed by the algorithm
    cfd_minconf: cfd minimum confidence value (between 0 and 1)
    cfd_max_lhs: cfd max considered LHS size
    cfd_substrategy: CFD lattice traversal strategy to use
    [dfs|bfs]
    """
    def __init__(self) -> None: ...

Default = FDFirst

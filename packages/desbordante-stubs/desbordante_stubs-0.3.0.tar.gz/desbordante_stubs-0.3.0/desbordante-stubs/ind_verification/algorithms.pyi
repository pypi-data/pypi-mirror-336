from __future__ import annotations
import desbordante

__all__ = ["Default", "INDVerifier"]

class INDVerifier(desbordante.Algorithm):
    """
    Options:
    tables: table collection processed by the algorithm
    lhs_indices: LHS column indices
    rhs_indices: RHS column indices
    """
    def __init__(self) -> None: ...
    def get_error(self) -> float: ...
    def get_violating_clusters(self) -> list[list[int]]: ...
    def get_violating_clusters_count(self) -> int: ...
    def get_violating_rows_count(self) -> int: ...
    def ind_holds(self) -> bool: ...

Default = INDVerifier

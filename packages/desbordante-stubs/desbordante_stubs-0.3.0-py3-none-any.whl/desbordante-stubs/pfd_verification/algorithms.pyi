from __future__ import annotations
import desbordante

__all__ = ["Default", "PFDVerifier"]

class PFDVerifier(desbordante.Algorithm):
    """
    Options:
    table: table processed by the algorithm
    lhs_indices: LHS column indices
    is_null_equal_null: specify whether two NULLs should be considered equal
    pfd_error_measure: PFD error measure to use
    [per_tuple|per_value]
    rhs_indices: RHS column indices
    """
    def __init__(self) -> None: ...
    def get_error(self) -> float: ...
    def get_num_violating_clusters(self) -> int: ...
    def get_num_violating_rows(self) -> int: ...
    def get_violating_clusters(self) -> list[list[int]]: ...

Default = PFDVerifier

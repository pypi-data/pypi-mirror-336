from __future__ import annotations
import desbordante
import desbordante.nd_verification

__all__ = ["Default", "NDVerifier"]

class NDVerifier(desbordante.Algorithm):
    """
    Options:
    table: table processed by the algorithm
    lhs_indices: LHS column indices
    is_null_equal_null: specify whether two NULLs should be considered equal
    rhs_indices: RHS column indices
    weight: Weight of ND to verify (positive integer)
    """
    def __init__(self) -> None: ...
    def get_lhs_frequencies(self) -> dict[str, int]: ...
    def get_rhs_frequencies(self) -> dict[str, int]: ...
    @property
    def global_min_weight(self) -> int: ...
    @property
    def highlights(self) -> list[desbordante.nd_verification.Highlight]: ...
    @property
    def nd_holds(self) -> bool: ...
    @property
    def real_weight(self) -> int: ...

Default = NDVerifier

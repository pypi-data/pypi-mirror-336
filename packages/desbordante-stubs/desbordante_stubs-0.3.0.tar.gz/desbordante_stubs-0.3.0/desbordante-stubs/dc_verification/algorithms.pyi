from __future__ import annotations
import desbordante

__all__ = ["DCVerification", "Default"]

class DCVerification(desbordante.Algorithm):
    """
    Options:
    denial_constraint: String representation of a Denial Constraint
    table: table processed by the algorithm
    """
    def __init__(self) -> None: ...
    def dc_holds(self) -> bool: ...

Default = DCVerification

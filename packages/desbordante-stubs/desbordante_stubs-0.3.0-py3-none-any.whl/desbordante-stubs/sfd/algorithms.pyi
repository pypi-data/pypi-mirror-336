from __future__ import annotations
import desbordante.fd
import desbordante.sfd

__all__ = ["Default", "SFDAlgorithm"]

class SFDAlgorithm(desbordante.fd.FdAlgorithm):
    def __init__(self) -> None: ...
    def get_correlations(self) -> list[desbordante.sfd.Correlation]: ...

Default = SFDAlgorithm

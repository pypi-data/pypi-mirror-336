from __future__ import annotations
import desbordante
import desbordante.ac

__all__ = ["AcAlgorithm", "Default"]

class AcAlgorithm(desbordante.Algorithm):
    """
    Options:
    table: table processed by the algorithm
    bumps_limit: max considered intervals amount. Pass 0 to remove limit
    fuzziness: fraction of exceptional records, lies in (0, 1]
    ac_seed: seed, needed for choosing a data sample
    iterations_limit: limit for iterations of sampling
    p_fuzz: probability, the fraction of exceptional records that lie outside the bump intervals is at most Fuzziness, lies in (0, 1]
    weight: value lies in (0, 1]. Closer to 0 - many short intervals. Closer to 1 - small number of long intervals
    bin_operation: one of available operations: /, *, +, -
    """
    def __init__(self) -> None: ...
    def get_ac_exceptions(self) -> list[desbordante.ac.ACException]: ...
    def get_ac_ranges(self) -> list[desbordante.ac.ACRanges]: ...

Default = AcAlgorithm

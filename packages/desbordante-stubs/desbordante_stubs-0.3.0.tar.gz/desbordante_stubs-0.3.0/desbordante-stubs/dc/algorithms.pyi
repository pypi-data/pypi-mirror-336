from __future__ import annotations
import desbordante
import desbordante.dc

__all__ = ["Default", "FastADC"]

class FastADC(desbordante.Algorithm):
    """
    Options:
    table: table processed by the algorithm
    shard_length: Number of rows each shard will cover when building PLI shards. Determines the segmentation of rows for parallel processing in the FastADC algorithm
    minimum_shared_value: Minimum threshold for the shared percentage of values between two columns
    comparable_threshold: Threshold for the ratio of smaller to larger average values between two numeric columns
    allow_cross_columns: Specifies whether to allow the construction of Denial Constraints between different attributes
    evidence_threshold: Denotes the maximum fraction of evidence violations allowed for a Denial Constraint to be considered approximate.
    """
    def __init__(self) -> None: ...
    def get_dcs(self) -> list[desbordante.dc.DC]: ...

Default = FastADC

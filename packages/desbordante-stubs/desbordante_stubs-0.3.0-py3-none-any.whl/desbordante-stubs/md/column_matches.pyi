from __future__ import annotations
import typing

__all__ = [
    "ColumnMatch",
    "Custom",
    "Equality",
    "Jaccard",
    "LVNormDateDistance",
    "LVNormNumberDistance",
    "Lcs",
    "Levenshtein",
    "MongeElkan",
]

class ColumnMatch:
    pass

class Custom(ColumnMatch):
    """
    Defines a column match with a custom similarity measure.
    """
    @typing.overload
    def __init__(
        self,
        comparer: typing.Callable[[typing.Any, typing.Any], float],
        left_column: str | int,
        right_column: str | int,
        *,
        column_functions: typing.Callable[[str], typing.Any]
        | tuple[
            typing.Callable[[str], typing.Any], typing.Callable[[str], typing.Any]
        ] = None,
        symmetrical: bool = False,
        equality_is_max: bool = False,
        min_sim: float = 0.7,
        measure_name: str = "custom_measure",
        size_limit: int = 0,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        comparer: typing.Any,
        left_column: str | int,
        right_column: str | int,
        classic_measure: bool,
        *,
        column_functions: typing.Callable[[str], typing.Any]
        | tuple[
            typing.Callable[[str], typing.Any], typing.Callable[[str], typing.Any]
        ] = None,
        min_sim: float = 0.7,
        measure_name: str = "custom_measure",
        size_limit: int = 0,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        comparer: typing.Callable[[typing.Any, typing.Any], float],
        left_column: str | int,
        right_column: str | int,
        *,
        column_functions: typing.Callable[[str], typing.Any]
        | tuple[
            typing.Callable[[str], typing.Any], typing.Callable[[str], typing.Any]
        ] = None,
        symmetrical: bool = False,
        equality_is_max: bool = False,
        min_sim: float = 0.7,
        measure_name: str = "custom",
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
    ) -> None: ...

class Equality(ColumnMatch):
    def __init__(self, left_column: str | int, right_column: str | int) -> None: ...

class Jaccard(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...

class LVNormDateDistance(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], ...]
        | tuple[typing.Callable[[str], ...], typing.Callable[[str], ...]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], ...]
        | tuple[typing.Callable[[str], ...], typing.Callable[[str], ...]] = None,
    ) -> None: ...

class LVNormNumberDistance(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], float]
        | tuple[typing.Callable[[str], float], typing.Callable[[str], float]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], float]
        | tuple[typing.Callable[[str], float], typing.Callable[[str], float]] = None,
    ) -> None: ...

class Lcs(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...

class Levenshtein(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...

class MongeElkan(ColumnMatch):
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        bound_number_limit: int = 0,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        left_column: str | int,
        right_column: str | int,
        minimum_similarity: float = 0.7,
        *,
        pick_lhs_indices: typing.Callable[[list[float]], list[int]] = ...,
        column_functions: typing.Callable[[str], str]
        | tuple[typing.Callable[[str], str], typing.Callable[[str], str]] = None,
    ) -> None: ...

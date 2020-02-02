from typing import Dict, List, Union

__all__ = ("PlaylistBreakdownType", "TierBreakdownType")

_PlaylistBreakdownIntType = Dict[int, Dict[int, List[int]]]
_PlaylistBreakdownFloatType = Dict[int, Dict[int, List[int]]]

PlaylistBreakdownType = Union[_PlaylistBreakdownIntType, _PlaylistBreakdownFloatType]

TierBreakdownType = Union[
    Dict[int, _PlaylistBreakdownIntType], Dict[int, _PlaylistBreakdownFloatType]
]

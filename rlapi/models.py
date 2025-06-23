from typing import Any, Dict


class PlayerTitle:
    """
    Represents a player title.

    Attributes
    ----------
    id: str
        The ID of the player title.
    """

    def __init__(self, title_id: str):
        self.id = title_id

    def __repr__(self) -> str:
        return f"<PlayerTitle id={self.id!r}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PlayerTitle):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, PlayerTitle):
            return self.id != other.id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.id)


class Population:
    """
    Represents the player population across different platforms and playlists.

    Attributes
    ----------
    data: Dict[str, Any]
        The raw data for the population.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def __repr__(self) -> str:
        return f"<Population data={self.data!r}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Population):
            return self.data == other.data
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, Population):
            return self.data != other.data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(frozenset(self.data.items()))

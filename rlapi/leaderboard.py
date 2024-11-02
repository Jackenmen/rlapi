from typing import Any, Dict, Optional

from .enums import Platform, PlaylistKey, Stat

__all__ = (
    "SkillLeaderboardPlayer",
    "SkillLeaderboard",
    "StatLeaderboardPlayer",
    "StatLeaderboard",
)


class SkillLeaderboardPlayer:
    """SkillLeaderboardPlayer()
    Represents Rocket League Player on a platform's skill leaderboard.

    Attributes
    ----------
    platform: Platform
        Platform that this leaderboard entry refers to.
    playlist_key: PlaylistKey
        Playlist that this leaderboard entry refers to.
    user_id: str, optional
        Player's user ID.
        Only present for Steam and Epic Games players.
    user_name: str
        Player's username (display name).
    tier: int
        Player's tier on the specified playlist.
    skill: int
        Player's skill rating on the specified playlist.

    """

    __slots__ = ("platform", "playlist_key", "user_name", "user_id", "tier", "skill")

    def __init__(
        self,
        platform: Platform,
        playlist_key: PlaylistKey,
        data: Dict[str, Any],
    ) -> None:
        self.platform = platform
        self.playlist_key = playlist_key
        self.user_name: str = data["user_name"]
        self.user_id: Optional[str] = data.get("user_id")
        if (
            self.user_id is not None
            and self.user_id.startswith(f"{platform.value}|")
            and self.user_id.endswith("|0")
        ):
            self.user_id = self.user_id[len(platform.value) + 1 : -2]
        self.tier: int = data["tier"]
        self.skill: int = data["skill"]

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        return (
            f"<{self.__class__.__name__}"
            f" {self.playlist_key}"
            f" platform={platform_repr}"
            f" user_name={self.user_name!r}"
            f" user_id={self.user_id!r}"
            f" tier={self.tier}"
            f" skill={self.skill}"
            ">"
        )


class SkillLeaderboard:
    """SkillLeaderboard()
    Represents Rocket League playlist's skill leaderboard for a single platform.

    Attributes
    ----------
    platform: Platform
        Platform that this leaderboard refers to.
    playlist_key: PlaylistKey
        Playlist that this leaderboard refers to.
    players: list of `StatLeaderboardPlayer`
        List of playlist's top 100 players on the platform.

    """

    __slots__ = ("platform", "playlist_key", "players")

    def __init__(
        self,
        platform: Platform,
        playlist_key: PlaylistKey,
        data: Dict[str, Any],
    ) -> None:
        self.platform = platform
        self.playlist_key = playlist_key
        self.players = [
            SkillLeaderboardPlayer(platform, playlist_key, player_data)
            for player_data in data["leaderboard"]
        ]

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        return (
            f"<{self.__class__.__name__} {self.playlist_key} platform={platform_repr}>"
        )


class StatLeaderboardPlayer:
    """StatLeaderboardPlayer()
    Represents Rocket League Player on a platform's stat leaderboard.

    Attributes
    ----------
    platform: Platform
        Platform that this leaderboard entry refers to.
    stat: Stat
        Stat that this leaderboard entry refers to.
    user_id: str, optional
        Player's user ID.
        Only present for Steam and Epic Games players.
    user_name: str
        Player's username (display name).
    value: int
        Value of the specified stat for the player.

    """

    __slots__ = ("platform", "stat", "user_name", "user_id", "value")

    def __init__(
        self,
        platform: Platform,
        stat: Stat,
        data: Dict[str, Any],
    ) -> None:
        self.platform = platform
        self.stat = stat
        self.user_name: str = data["user_name"]
        self.user_id: Optional[str] = data.get("user_id")
        if (
            self.user_id is not None
            and self.user_id.startswith(f"{platform.value}|")
            and self.user_id.endswith("|0")
        ):
            self.user_id = self.user_id[len(platform.value) + 1 : -2]
        self.value: int = data[stat.value]

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        stat_repr = f"{self.stat.__class__.__name__}.{self.stat._name_}"
        return (
            f"<{self.__class__.__name__}"
            f" platform={platform_repr}"
            f" user_name={self.user_name!r}"
            f" user_id={self.user_id!r}"
            f" stat={stat_repr}"
            f" value={self.value}"
            ">"
        )


class StatLeaderboard:
    """StatLeaderboard()
    Represents Rocket League stat leaderboard for a single platform.

    Attributes
    ----------
    platform: Platform
        Platform that this leaderboard refers to.
    stat: Stat
        Stat that this leaderboard refers to.
    players: list of `StatLeaderboardPlayer`
        List of stat's top 100 players on the platform.

    """

    __slots__ = ("platform", "stat", "players")

    def __init__(
        self,
        platform: Platform,
        stat: Stat,
        data: Dict[str, Any],
    ) -> None:
        self.platform = platform
        self.stat = stat
        self.players = [
            StatLeaderboardPlayer(platform, stat, player_data)
            for player_data in data[stat.value]
        ]

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        stat_repr = f"{self.stat.__class__.__name__}.{self.stat._name_}"
        return f"<{self.__class__.__name__} platform={platform_repr} stat={stat_repr}>"

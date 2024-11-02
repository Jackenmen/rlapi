# Copyright 2018-present Jakub Kuczys (https://github.com/Jackenmen)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Dict, Final, List, Optional, Union

from .enums import Platform, PlaylistKey, Stat
from .player_titles import PlayerTitle
from .tier_estimates import TierEstimates
from .typedefs import PlaylistBreakdownType, TierBreakdownType

if TYPE_CHECKING:
    from .client import Client

# The documentation of below constants needs to be manually repeated in docs/api.rst
# due to: https://github.com/sphinx-doc/sphinx/issues/6495

#: A sequence of rank names, indexed by the value of `Playlist.tier`.
#:
#: Rank names are only provided in the English language.
RANKS = (
    "Unranked",
    "Bronze I",
    "Bronze II",
    "Bronze III",
    "Silver I",
    "Silver II",
    "Silver III",
    "Gold I",
    "Gold II",
    "Gold III",
    "Platinum I",
    "Platinum II",
    "Platinum III",
    "Diamond I",
    "Diamond II",
    "Diamond III",
    "Champion I",
    "Champion II",
    "Champion III",
    "Grand Champion I",
    "Grand Champion II",
    "Grand Champion III",
    "Supersonic Legend",
)
#: A sequence of roman numerals for divisions,
#: indexed by the value of `Playlist.division`.
DIVISIONS = ("I", "II", "III", "IV")
#: A sequence of season reward level names, indexed by the value of
#: `SeasonRewards.level`.
#:
#: Season reward level names are only provided in the English language.
SEASON_REWARDS = (
    "Unranked",
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond",
    "Champion",
    "Grand Champion",
    "Supersonic Legend",
)
#: A sequence of playlists that can advance player's season rewards.
PLAYLISTS_WITH_SEASON_REWARDS = (
    PlaylistKey.solo_duel,
    PlaylistKey.doubles,
    PlaylistKey.standard,
    PlaylistKey.hoops,
    PlaylistKey.rumble,
    PlaylistKey.dropshot,
    PlaylistKey.snow_day,
)

__all__ = (
    "RANKS",
    "DIVISIONS",
    "SEASON_REWARDS",
    "PLAYLISTS_WITH_SEASON_REWARDS",
    "Playlist",
    "SeasonRewards",
    "Player",
)


class Playlist:
    """Playlist()
    Represents Rocket League playlist stats data.

    .. container:: operations

        ``str(x)``
            Returns playlist's rank string, e.g. "Champion I Div III".

            This is only provided in the English language.

    Attributes
    ----------
    key: `PlaylistKey` or `int`
        Playlist's key. Might be `int`, if that key
        is not within the ones recognised by the enumerator.
    tier: int
        Tier on this playlist.
    division: int
        Division on this playlist.
    mu: float
        Mu on this playlist.
    skill: int
        Skill rating on this playlist.
    sigma: float
        Sigma on this playlist.
    win_streak: int
        Win streak on this playlist.
    matches_played: int
        Number of matches played on this playlist during the current season.
    lifetime_matches_played: int
        Number of matches played on this playlist since player started playing the game.

        .. note::

            This number does not seem to include some of the earlier seasons.
            It is estimated that it include all matches played in Season 4
            (before Free To Play update) and later.

    placement_matches_played: int
        Number of placement matches played on this playlist during the current season.
        Maxes out at 10.
    breakdown: dict
        Playlist tier breakdown.
    tier_estimates: `TierEstimates`
        Tier estimates for this playlist.

    """

    #: Max tier, i.e. Supersonic Legend
    TIER_MAX: Final[int] = 22
    #: Max division, i.e. Division IV
    DIVISION_MAX: Final[int] = 3

    __slots__ = (
        "key",
        "tier",
        "division",
        "mu",
        "skill",
        "sigma",
        "win_streak",
        "matches_played",
        "lifetime_matches_played",
        "placement_matches_played",
        "breakdown",
        "tier_estimates",
    )

    def __init__(
        self,
        *,
        breakdown: Optional[PlaylistBreakdownType] = None,
        playlist_key: Union[PlaylistKey, int],
        data: Dict[str, Any],
    ):
        self.key = playlist_key
        # only mu and sigma always exist, rest might be None or not be part of the dict
        self.tier: int = data.get("tier") or 0
        self.division: int = data.get("division") or 0

        mu: Optional[float] = data.get("mu")
        self.mu: float
        if mu is not None:
            self.mu = mu
        else:
            self.mu = 25
        skill: Optional[int] = data.get("skill")
        self.skill: int
        if skill is not None:
            self.skill = skill
        else:
            self.skill = int(self.mu * 20 + 100)

        self.sigma: float = data.get("sigma") or 8.333
        self.win_streak: int = data.get("win_streak") or 0
        self.matches_played: int = data.get("matches_played") or 0
        self.lifetime_matches_played: int = data.get("lifetime_matches_played") or 0
        self.placement_matches_played: int = data.get("placement_matches_played") or 0
        self.breakdown = breakdown if breakdown is not None else {}
        self.tier_estimates = TierEstimates(self)

    def __str__(self) -> str:
        try:
            if self.tier in {0, self.TIER_MAX}:
                return RANKS[self.tier]
            return f"{RANKS[self.tier]} Div {DIVISIONS[self.division]}"
        except IndexError:
            return "Unknown"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" {self.key};"
            f" Rank {self};"
            f" mu={self.mu}"
            f" skill={self.skill}"
            f" win_streak={self.win_streak}"
            f" matches_played={self.matches_played}"
            f">"
        )


class SeasonRewards:
    """SeasonRewards()
    Represents season rewards informations.

    Attributes
    ----------
    level: int
        Player's season reward level.
    wins: int
        Player's season reward wins.
    can_advance: bool
        Tells if player can advance to `next_level`.
    next_level: int, optional
        Next level of season rewards or ``None`` if max level has already been reached.

    """

    #: Max season reward level, i.e. Supersonic Legend
    MAX_LEVEL: Final[int] = 8

    __slots__ = ("level", "wins", "can_advance", "next_level")

    def __init__(self, *, highest_tier: int = 0, data: Dict[str, Any]) -> None:
        self.level: int = data.get("level") or 0
        self.wins: int = data.get("wins") or 0
        self.can_advance: bool
        if self.level == 0 or self.level * 3 < highest_tier:
            self.can_advance = True
        else:
            self.can_advance = False
        self.next_level = self.level + 1 if self.level != self.MAX_LEVEL else None

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" level={self.level}"
            f" wins={self.wins}"
            f" can_advance={self.can_advance}"
            f" next_level={self.next_level}"
            f">"
        )


class PlayerStats:
    """PlayerStats()
    Represents player stats (assists, goals, MVPs, etc.).

    .. container:: operations

        ``x[key]``
            Lookup player's stat value by `Stat` enum.

    Attributes
    ----------
    assists: int
        Number of player's assists.
    goals: int
        Number of player's goals.
    mvps: int
        Number of player's MVPs.
    saves: int
        Number of player's saves.
    shots: int
        Number of player's shots.
    wins: int
        Number of player's wins.
    """

    __slots__ = (
        "assists",
        "goals",
        "mvps",
        "saves",
        "shots",
        "wins",
    )

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        stats = {stat["stat_type"]: stat["value"] for stat in data}
        self.assists: int = stats.get("assists", 0)
        self.goals: int = stats.get("goals", 0)
        self.mvps: int = stats.get("mvps", 0)
        self.saves: int = stats.get("saves", 0)
        self.shots: int = stats.get("shots", 0)
        self.wins: int = stats.get("wins", 0)

    def __getitem__(self, stat: Stat) -> int:
        return int(getattr(self, stat.name))

    def __repr__(self) -> str:
        attrs = " ".join(f"{key}={getattr(self, key)}" for key in self.__slots__)
        return f"<{self.__class__.__name__} {attrs}>"


class Player:
    """Player()
    Represents Rocket League Player

    Attributes
    ----------
    platform: `Platform`
        Player's platform.
    user_id: str, optional
        Player's user ID.
        Present when the data was looked up by user ID
        or when the lookup platform was Steam or Epic Games.
    user_name: str
        Player's username (display name).
    playlists: dict
        Dictionary mapping `PlaylistKey` with `Playlist`.
    tier_breakdown: dict
        Tier breakdown.
    highest_tier: int
        Highest tier of the player.
        Doesn't include the playlists that don't count towards season rewards.
    season_rewards: `SeasonRewards`
        Season rewards info.
    stats: `PlayerStats`
        Player's stats (assists, goals, MVPs, etc.).

    """

    __slots__ = (
        "_client",
        "platform",
        "user_id",
        "user_name",
        "playlists",
        "tier_breakdown",
        "highest_tier",
        "season_rewards",
        "stats",
    )

    def __init__(
        self,
        *,
        client: Client,
        tier_breakdown: Optional[TierBreakdownType] = None,
        platform: Platform,
        data: Dict[str, Any],
    ) -> None:
        self._client = client
        self.platform = platform
        self.user_id: Optional[str] = data.get("player_id")
        self.user_name: str = data["player_name"]

        self.playlists: Dict[Union[PlaylistKey, int], Playlist] = {}
        player_skills = data.get("player_skills", [])
        self.tier_breakdown = tier_breakdown if tier_breakdown is not None else {}
        self._prepare_playlists(player_skills)

        self.highest_tier = max(
            (
                playlist.tier
                for playlist in self.playlists.values()
                if playlist.key in PLAYLISTS_WITH_SEASON_REWARDS
            ),
            default=0,
        )

        season_rewards = data.get("season_rewards", {})
        self.season_rewards = SeasonRewards(
            highest_tier=self.highest_tier, data=season_rewards
        )

        player_stats = data.get("player_stats", [])
        self.stats = PlayerStats(player_stats)

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        return (
            f"<{self.__class__.__name__}"
            f" platform={platform_repr}"
            f" user_id={self.user_id!r}"
            f" user_name={self.user_name!r}"
            f">"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self.platform is not other.platform:
            return False

        # both object have `user_id` so we can just compare those
        if None not in (self.user_id, other.user_id):
            return self.user_id == other.user_id

        # it's rather unlikely that only one `user_id` is None if platforms are equal,
        # but checking equality of both `user_id` and `user_name` just in case
        return (self.user_id, self.user_name) == (other.user_id, other.user_name)

    def __hash__(self) -> int:
        if self.user_id is not None:
            return hash((self.platform, "by_user_id", self.user_id))
        return hash((self.platform, "by_user_name", self.user_name))

    async def titles(self) -> List[PlayerTitle]:
        """
        Get player's titles.

        .. note::

            Some titles that the player has may not be included in the response.

        Returns
        -------
        `list` of `PlayerTitle`
            List of player's titles.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        """
        if self.platform in (Platform.steam, Platform.epic):
            assert self.user_id is not None
            return await self._client.get_player_titles(self.platform, self.user_id)
        return await self._client.get_player_titles(self.platform, self.user_name)

    def get_playlist(self, playlist_key: PlaylistKey) -> Optional[Playlist]:
        """
        Get playlist for the player.

        Parameters
        ----------
        playlist_key: PlaylistKey
            `PlaylistKey` for playlist to get.

        Returns
        -------
        `Playlist`, optional
            Playlist object for provided playlist key.

        """
        return self.playlists.get(playlist_key)

    def add_playlist(self, playlist: Dict[str, Any]) -> None:
        playlist_key = playlist.pop("playlist")
        breakdown = self.tier_breakdown.get(playlist_key, {})
        with contextlib.suppress(ValueError):
            playlist_key = PlaylistKey(playlist_key)

        self.playlists[playlist_key] = Playlist(
            breakdown=breakdown, playlist_key=playlist_key, data=playlist
        )

    def _prepare_playlists(self, player_skills: List[Dict[str, Any]]) -> None:
        for playlist in player_skills:
            self.add_playlist(playlist)

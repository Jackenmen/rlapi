# Copyright 2018-2020 Jakub Kuczys (https://github.com/jack1142)
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

import contextlib
from typing import Any, Dict, List, Optional, Union

from .enums import Platform, PlaylistKey
from .tier_estimates import TierEstimates
from .typedefs import PlaylistBreakdownType, TierBreakdownType

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
DIVISIONS = ("I", "II", "III", "IV")
PLAYLISTS_WITH_SEASON_REWARDS = (
    PlaylistKey.solo_duel,
    PlaylistKey.doubles,
    PlaylistKey.standard,
    PlaylistKey.hoops,
    PlaylistKey.rumble,
    PlaylistKey.dropshot,
    PlaylistKey.snow_day,
)

__all__ = ("Playlist", "SeasonRewards", "Player")


class Playlist:
    """Playlist()
    Represents Rocket League playlist stats data.

    .. container:: operations

        ``str(x)``
            Returns playlist's rank string, e.g. "Champion I Div III"

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
        Amount of matches played on this playlist.
    tier_max: int
        Maximum tier that can be achieved on this playlist.
    breakdown: dict
        Playlist tier breakdown.
    tier_estimates: `TierEstimates`
        Tier estimates for this playlist.

    """

    __slots__ = (
        "key",
        "tier",
        "division",
        "mu",
        "skill",
        "sigma",
        "win_streak",
        "matches_played",
        "tier_max",
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
        self.tier_max = 22
        # This is how it should be done, but API returns old max value right now
        # While I could just have what API returns here,
        # some parts of library depend on this being the proper value
        #
        # self.tier_max: int = data.get("tier_max", 22)
        self.breakdown = breakdown if breakdown is not None else {}
        self.tier_estimates = TierEstimates(self)

    def __str__(self) -> str:
        try:
            if self.tier in {0, self.tier_max}:
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
        Tells if player can advance in season rewards.

    """

    __slots__ = ("level", "wins", "can_advance")

    def __init__(self, *, highest_tier: int = 0, data: Dict[str, Any]) -> None:
        self.level: int = data.get("level", 0)
        if self.level is None:
            self.level = 0
        self.wins: int = data.get("wins", 0)
        if self.wins is None:
            self.wins = 0
        self.can_advance: bool
        if self.level == 0 or self.level * 3 < highest_tier:
            self.can_advance = True
        else:
            self.can_advance = False

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f" level={self.level}"
            f" wins={self.wins}"
            f" can_advance={self.can_advance}"
            f">"
        )


class Player:
    """Player()
    Represents Rocket League Player

    Attributes
    ----------
    platform: `Platform`
        Player's platform.
    player_id: str
        ``player_id`` as passed to `Client.get_player()`.
    user_id: str, optional
        Player's user ID, ``None`` for non-Steam players.
    user_name: str
        Player's username (display name)
    playlists: dict
        Dictionary mapping `PlaylistKey` with `Playlist`.
    tier_breakdown: dict
        Tier breakdown.
    highest_tier: int
        Highest tier of the player.
        Doesn't include the playlists that don't count towards season rewards.
    season_rewards: `SeasonRewards`
        Season rewards info.

    """

    __slots__ = (
        "platform",
        "player_id",
        "user_id",
        "user_name",
        "playlists",
        "tier_breakdown",
        "highest_tier",
        "season_rewards",
    )

    def __init__(
        self,
        *,
        tier_breakdown: Optional[TierBreakdownType] = None,
        platform: Platform,
        player_id: str,
        data: Dict[str, Any],
    ) -> None:
        self.platform = platform
        self.player_id = player_id
        self.user_id: Optional[str] = data.get("user_id")
        self.user_name: str = data["user_name"]

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

    def __repr__(self) -> str:
        platform_repr = f"{self.platform.__class__.__name__}.{self.platform._name_}"
        return (
            f"<{self.__class__.__name__}"
            f" platform={platform_repr}"
            f" player_id={self.player_id!r}"
            f">"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        # I could just check `player_id`, but it's user provided
        # so two objects could potentially be equal even if `player_id` isn't

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

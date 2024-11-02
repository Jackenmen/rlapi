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

import asyncio
import itertools
import logging
import re
import time
import warnings
from typing import (
    Any,
    AsyncIterable,
    Dict,
    Iterable,
    Iterator,
    List,
    Match,
    Optional,
    Set,
    Union,
    cast,
)

import aiohttp
from lxml import etree

from . import errors
from ._utils import TokenInfo, json_or_text
from .enums import Platform, PlaylistKey, Stat
from .leaderboard import SkillLeaderboard, StatLeaderboard
from .player import Player
from .player_titles import PlayerTitle
from .population import Population
from .typedefs import TierBreakdownType

log = logging.getLogger(__name__)

__all__ = ("Client",)

# valid regexes per platform represented as tuple of (id_pattern, name_pattern)
_PLATFORM_PATTERNS = {
    Platform.steam: (
        # Unlike on other platforms, this matches both IDs and names
        # since usernames and profile URLs get processed to an ID for use with RL API.
        # Matches profile URL, steamID64, or customURL.
        re.compile(
            r"""
            (?:
                (?:https?:\/\/(?:www\.)?)?steamcommunity\.com\/
                (id|profiles)\/         # group 1 - None if input is only a username/id
            )?
            ([a-zA-Z0-9_-]{2,32})\/?    # group 2
            """,
            re.VERBOSE,
        ),
        # never-matching pattern
        re.compile(r"$^"),
    ),
    Platform.ps4: (
        # PSN Account ID
        re.compile(r"\d{19}"),
        # PSN username (Online ID)
        re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,15}"),
    ),
    Platform.xboxone: (
        # Xbox services ID (XUID) in decimal format
        # (16 digits or 15 digits prefixed with 0)
        re.compile(r"\d{16}"),
        # Gamertag
        re.compile(r"[a-zA-Z](?=.{0,15}$)([a-zA-Z0-9-_]+ ?)+"),
    ),
    Platform.epic: (
        # Epic Account ID
        re.compile(r"[0-9a-f]{32}"),
        # Epic Display Name (unique but the API ignores some accented characters)
        re.compile(r".{3,16}"),
    ),
    Platform.switch: (
        # never-matching pattern
        re.compile(r"$^"),
        # Nintendo nickname (not unique)
        re.compile(r".{1,10}"),
    ),
}


class Client:
    RLAPI_BASE = "https://api.rlpp.psynet.gg/public/v1"
    STEAM_BASE = "https://steamcommunity.com"
    EPIC_OAUTH_URL = "https://api.epicgames.dev/epic/oauth/v1/token"
    SEARCH_QUERY_LIMIT = 10

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        tier_breakdown: Optional[TierBreakdownType] = None,
    ):
        self._session = aiohttp.ClientSession()
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_info: Optional[TokenInfo] = None
        self._xml_parser = etree.XMLParser(resolve_entities=False)
        self.tier_breakdown: TierBreakdownType
        if tier_breakdown is None:
            # cast of empty list to a type needed here
            # see https://github.com/python/mypy/issues/3283
            self.tier_breakdown = cast(TierBreakdownType, {})
        else:
            self.tier_breakdown = tier_breakdown

    async def close(self) -> None:
        """
        Close underlying session.

        Release all acquired resources.
        """
        await self._session.close()

    def destroy(self) -> None:
        """
        Detach underlying session.

        The `close()` method should be used instead when possible as
        this function does not close the session's connector.
        """
        self._session.detach()

    def __del__(self) -> None:
        if not self._session.closed:
            warnings.warn(
                f"Unclosed Rocket League API client {self!r}",
                ResourceWarning,
                source=self,
            )
            self.destroy()

    def update_client_credentials(self, *, client_id: str, client_secret: str) -> None:
        """
        Update client ID and client secret.

        Parameters
        ----------
        client_id: str
            New client ID.
        client_secret: str
            New client secret.

        """
        self._client_id = client_id
        self._client_secret = client_secret

    async def _get_access_token(self, *, force_refresh: bool = False) -> str:
        if (
            self._token_info is not None
            and self._token_info.expires_at - time.time() > 60
            and not force_refresh
        ):
            return self._token_info.access_token

        self._token_info = await self._request_token()
        return self._token_info.access_token

    async def _request_token(self) -> TokenInfo:
        expires_at = int(time.time())
        async with self._session.post(
            self.EPIC_OAUTH_URL,
            data={"grant_type": "client_credentials"},
            auth=aiohttp.BasicAuth(self._client_id, self._client_secret),
        ) as resp:
            data = await json_or_text(resp)
            if resp.status != 200:
                raise errors.HTTPException(resp, data)

        assert data["token_type"] == "bearer"
        expires_at += data["expires_in"]
        return TokenInfo(data["access_token"], expires_at)

    async def _rlapi_request(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, str]] = None,
        force_refresh_token: bool = False,
    ) -> Any:
        url = self.RLAPI_BASE + endpoint
        token = await self._get_access_token(force_refresh=force_refresh_token)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            data = await self._request(url, headers, params=params)
        except errors.Unauthorized:
            if force_refresh_token:
                raise
            data = await self._rlapi_request(
                endpoint, params=params, force_refresh_token=True
            )
        return data

    async def _request(
        self,
        url: str,
        headers: Optional[aiohttp.typedefs.LooseHeaders] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> Any:
        for tries in range(5):
            async with self._session.get(url, headers=headers, params=params) as resp:
                data = await json_or_text(resp)
                search_query_limit = int(resp.headers.get("X-Search-Query-Limit", 0))
                if search_query_limit > 0:  # avoid infinite loops due to limit == 0
                    self.SEARCH_QUERY_LIMIT = search_query_limit
                if resp.status == 200:
                    return data

                # response data should only be one of those types if error occurs
                data: Union[Dict[str, Any], str]  # type: ignore

                # received 500 or 502 error, API has some troubles, retrying
                if resp.status in {500, 502}:
                    await asyncio.sleep(1 + tries * 2)
                    continue
                # token is invalid
                if resp.status == 401:
                    raise errors.Unauthorized(resp, data)
                # generic error
                raise errors.HTTPException(resp, data)
        # still failed after 5 tries
        raise errors.HTTPException(resp, data)

    def _generate_request_chunks(
        self, platform: Platform, ids: Iterable[str], names: Iterable[str]
    ) -> Iterator[Dict[str, Any]]:
        common_params = {"platform": platform.value}
        count = 0
        id_list: List[str] = []
        params = {**common_params, "id[]": id_list}

        for id_ in ids:
            if count >= self.SEARCH_QUERY_LIMIT:
                yield params
                count = 0
                id_list = []
                params = {**common_params, "id[]": id_list}

            id_list.append(id_)
            count += 1

        name_list: List[str]
        params["name[]"] = name_list = []
        for name_ in names:
            if count >= self.SEARCH_QUERY_LIMIT:
                yield params
                count = 0
                name_list = []
                params = {**common_params, "name[]": name_list}

            name_list.append(name_)
            count += 1

        if count:
            yield params

    async def _get_profiles(
        self,
        platform: Platform,
        *,
        ids: Iterable[str] = (),
        names: Iterable[str] = (),
    ) -> List[Player]:
        return [
            player
            async for player in self._iter_get_profiles(platform, ids=ids, names=names)
        ]

    async def _iter_get_profiles(
        self,
        platform: Platform,
        *,
        ids: Iterable[str] = (),
        names: Iterable[str] = (),
        limit_reached: bool = False,
    ) -> AsyncIterable[Player]:
        """
        Get an asynchronous iterable of player profiles for given player IDs
        and names on the selected platform.

        See `platform-player-ids` section for supported lookup identifiers.

        .. note::

            This function will not raise when any of the given IDs/names
            could not be found and will simply not include them in the results.
            It isn't possible to easily map the returned players to given names (if any)
            and thus it's also not easily possible to determine which (if any) names
            are missing (and whether any identifiers were duplicated in the parameters).

        Parameters
        ----------
        platform: Platform
            Platform to search.
        ids: str
            IDs of the players to find.
            This can be used on all platforms provided that you know the ID
            but the API only returns it for Steam and Epic and therefore
            you'll probably be limited to using it on those two platforms.
        names: str
            Names of the players to find.
            This can be used on all platforms and does some kind of equality check
            on display names, ignoring case-sensitivity and other undocumented things
            such as some kind of accent-sensitivity. This means that you simply can't
            lookup some players on non-Steam platforms because the query could sometimes
            be fulfilled by multiple players.
        limit_reached: bool
            When search query imposed by the API is reached unexpectedly, the function
            calls itself again accounting for the newly learnt search query limit.
            When ``limit_reached=True`` is passed (as is the case when the function
            calls itself, now knowing the proper limit), this behavior will be skipped.

        Yields
        ------
        Player
            The requested player profile.
            The order the player profiles are yielded in should not be depended on.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League API failed.

        """
        endpoint = "/player/profile"

        ids = iter(ids)
        names = iter(names)
        chunks_it = self._generate_request_chunks(platform, ids, names)

        try:
            first = next(chunks_it)
        except StopIteration:
            raise TypeError("either ids or names must be specified") from None
        else:
            chunks_it = itertools.chain([first], chunks_it)

        for params in chunks_it:
            try:
                raw_players = await self._rlapi_request(endpoint, params=params)
            except errors.HTTPException as e:
                if e.status != 400:
                    raise
                if limit_reached:
                    raise
                headers = e.response.headers
                if headers["X-Search-Query-Limit"] < headers["X-Search-Query-Count"]:
                    async for player in self._iter_get_profiles(
                        platform,
                        ids=itertools.chain(params.get("id[]", []), ids),
                        names=itertools.chain(params.get("name[]", []), names),
                        limit_reached=True,
                    ):
                        yield player
                    return

                raise

            for player_data in raw_players:
                yield Player(
                    client=self,
                    platform=platform,
                    tier_breakdown=self.tier_breakdown,
                    data=player_data,
                )

    async def get_player_by_id(self, platform: Platform, id_: str, /) -> Player:
        """
        Get player profile on the given platform matching the specified ID.

        See `platform-player-ids` section for supported lookup identifiers.

        Parameters
        ----------
        id: str
            ID of player to find.

        Returns
        -------
        Player
            Requested player profile.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        PlayerNotFound
            The player could not be found.

        """
        players = await self._get_profiles(platform, ids=[id_])
        try:
            return players[0]
        except IndexError:
            raise errors.PlayerNotFound(
                "Player with provided ID could not be found on the given platform."
            ) from None

    async def get_player_by_name(self, platform: Platform, name: str, /) -> Player:
        """
        Get player profile on the given platform matching the specified name.

        See `platform-player-ids` section for supported lookup identifiers.

        Parameters
        ----------
        name: str
            Display name of player to find.

        Returns
        -------
        Player
            Requested player profile.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        PlayerNotFound
            The player could not be found.

        """

        players = await self._get_profiles(platform, names=[name])
        try:
            return players[0]
        except IndexError:
            raise errors.PlayerNotFound(
                "Player with provided name could not be found on the given platform."
            ) from None

    async def find_player(self, player_id: str, /) -> List[Player]:
        """
        Get player profiles for given player ID by searching in all platforms.

        See `platform-player-ids` section for supported lookup identifiers.

        Parameters
        ----------
        player_id: str
            ID of player to find.

        Returns
        -------
        `list` of `Player`
            Requested player profiles.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League or Steam API failed.
        PlayerNotFound
            The player could not be found on any platform.

        """
        players: List[Player] = []
        for platform in Platform:
            try:
                players += await self._find_profile(player_id, platform)
            except errors.IllegalUsername as e:
                log.debug(str(e))
        if not players:
            raise errors.PlayerNotFound(
                "Player with provided ID could not be found on any platform."
            ) from None

        return players

    def get_players(
        self,
        platform: Platform,
        *,
        ids: Iterable[str] = (),
        names: Iterable[str] = (),
    ) -> AsyncIterable[Player]:
        """
        Get an asynchronous iterable of player profiles for given player IDs
        and names on the selected platform.

        See `platform-player-ids` section for supported lookup identifiers.

        .. note::

            This function will not raise when any of the given IDs/names
            could not be found and will simply not include them in the results.
            It isn't possible to easily map the returned players to given names (if any)
            and thus it's also not easily possible to determine which (if any) names
            are missing (and whether any identifiers were duplicated in the parameters).

        Parameters
        ----------
        platform: Platform
            Platform to search.
        ids: str
            IDs of the players to find.
            This can be used on all platforms provided that you know the ID
            but the API only returns it for Steam and Epic and therefore
            you'll probably be limited to using it on those two platforms.
        names: str
            Names of the players to find.
            This can be used on all platforms and does some kind of equality check
            on display names, ignoring case-sensitivity and other undocumented things
            such as some kind of accent-sensitivity. This means that you simply can't
            lookup some players on non-Steam platforms because the query could sometimes
            be fulfilled by multiple players.

        Yields
        ------
        Player
            The requested player profile.
            The order the player profiles are yielded in should not be depended on.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League API failed.

        """
        return self._iter_get_profiles(platform, ids=ids, names=names)

    async def _find_profile(self, player_id: str, platform: Platform) -> Set[Player]:
        ids: List[str] = []
        names: List[str] = []

        id_pattern, name_pattern = _PLATFORM_PATTERNS[platform]
        id_match = id_pattern.fullmatch(player_id)
        if id_match:
            if platform == Platform.steam:
                ids = await self._find_steam_ids(id_match)
            else:
                ids.append(player_id)

        name_match = name_pattern.fullmatch(player_id)
        if name_match:
            names.append(player_id)

        if not ids and not names:
            raise errors.IllegalUsername(
                "Provided ID or username doesn't match provided pattern:"
                f" {id_pattern}|{name_pattern}"
            )

        return set(await self._get_profiles(platform, ids=ids, names=names))

    async def _find_steam_ids(self, match: Match[str]) -> List[str]:
        player_id = match.group(2)
        search_type = match.group(1)
        if search_type is None:
            search_types = ["profiles", "id"]
        else:
            search_types = [search_type]
        ids: List[str] = []
        for search_type in search_types:
            url = self.STEAM_BASE + f"/{search_type}/{player_id}/?xml=1"
            async with self._session.get(url) as resp:
                if resp.status >= 400:
                    raise errors.HTTPException(resp, await resp.text())
                steam_profile = etree.fromstring(await resp.read(), self._xml_parser)

            error = steam_profile.find("error")
            if error is None:
                steam_id_element = steam_profile.find("steamID64")
                if steam_id_element is None:
                    log.debug(
                        "Steam didn't include 'steamID64' element"
                        " in response (profile found using '%s' method).",
                        search_type,
                    )
                    continue
                steam_id: Optional[str] = steam_id_element.text  # type: ignore
                if steam_id is None:
                    log.debug(
                        "'steamID64' element in response is empty"
                        " (profile found using '%s' method).",
                        search_type,
                    )
                    continue
                ids.append(steam_id)
            elif error.text != "The specified profile could not be found.":
                log.debug(
                    "Steam threw error while searching profile using '%s' method: %s",
                    search_type,
                    error.text,
                )

        return ids

    async def get_player_titles(
        self, platform: Platform, player_id: str
    ) -> List[PlayerTitle]:
        """
        Get player's titles.

        .. note::

            Some titles that the player has may not be included in the response.

        Parameters
        ----------
        platform: Platform
            Platform to lookup the player on.
        player_id: str
            Identifier to lookup the player by.
            This needs to be a user ID for the Steam and Epic platforms
            and a name for the rest of the platforms.

        Returns
        -------
        `list` of `PlayerTitle`
            List of player's titles.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        """
        endpoint = f"/player/titles/{platform.value}/{player_id}"
        data = await self._rlapi_request(endpoint)
        return [PlayerTitle(title_id) for title_id in data["titles"]]

    async def get_population(self) -> Population:
        """
        Get population across different platforms and playlists.

        Returns
        -------
        Population
            Player population across different platforms and playlists.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.

        """
        data = await self._rlapi_request("/population")
        return Population(data)

    async def get_skill_leaderboard(
        self, platform: Platform, playlist_key: PlaylistKey
    ) -> SkillLeaderboard:
        """
        Get skill leaderboard for the playlist on the given platform.

        Parameters
        ----------
        platform: Platform
            Platform to get the leaderboard for.
        playlist_key: PlaylistKey
            Playlist to get the leaderboard for.

        Returns
        -------
        SkillLeaderboard
            Skill leaderboard for the playlist on the given platform.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        """
        endpoint = f"/leaderboard/skill/{platform.value}/{playlist_key.value}"
        data = await self._rlapi_request(endpoint)
        return SkillLeaderboard(platform, playlist_key, data)

    async def get_stat_leaderboard(
        self, platform: Platform, stat: Stat
    ) -> StatLeaderboard:
        """
        Get leaderboard for the specified stat on the given platform.

        Parameters
        ----------
        platform: Platform
            Platform to get the leaderboard for.
        stat: Stat
            Stat to get the leaderboard for.

        Returns
        -------
        StatLeaderboard
            Leaderboard for the specified stat on the given platform.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League failed.
        """
        endpoint = f"/leaderboard/stat/{platform.value}/{stat.value}"
        data = await self._rlapi_request(endpoint)
        return StatLeaderboard(platform, stat, data)

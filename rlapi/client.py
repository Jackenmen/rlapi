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

import asyncio
import logging
import re
from typing import Any, Dict, List, Match, Optional, Set, Tuple, Union, cast

import aiohttp
from lxml import etree

from . import errors
from .enums import Platform
from .player import Player
from .typedefs import TierBreakdownType
from .utils import json_or_text

log = logging.getLogger(__name__)

__all__ = ("Client",)

# valid username regexes per platform
_PLATFORM_PATTERNS = {
    Platform.steam: re.compile(
        r"""
        (?:
            (?:https?:\/\/(?:www\.)?)?steamcommunity\.com\/
            (id|profiles)\/         # group 1 - None if input is only a username/id
        )?
        ([a-zA-Z0-9_-]{2,32})\/?    # group 2
        """,
        re.VERBOSE,
    ),
    Platform.ps4: re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,15}"),
    Platform.xboxone: re.compile(r"[a-zA-Z](?=.{0,15}$)([a-zA-Z0-9-_]+ ?)+"),
    Platform.epic: re.compile(r".{3,16}"),
    Platform.switch: re.compile(
        r"""
        [a-zA-Z0-9]  # first character can't be punctuation
        (?:
            [a-zA-Z0-9]        # non-punctuation character
            |[_\-.](?![_\-.])  # or punctuation character that isn't repeated in a row
        ){4,14}
        [a-zA-Z0-9]  # last character can't be punctuation
        """,
        re.VERBOSE,
    ),
}


class Client:
    RLAPI_BASE = "https://api.rocketleague.com/api/v1"
    STEAM_BASE = "https://steamcommunity.com"

    def __init__(
        self, token: str, *, tier_breakdown: Optional[TierBreakdownType] = None
    ):
        self._session = aiohttp.client.ClientSession()
        self._token = token
        self._xml_parser = etree.XMLParser(resolve_entities=False)
        self.tier_breakdown: TierBreakdownType
        if tier_breakdown is None:
            # cast of empty list to a type needed here
            # see https://github.com/python/mypy/issues/3283
            self.tier_breakdown = cast(TierBreakdownType, {})
        else:
            self.tier_breakdown = tier_breakdown

    def destroy(self) -> None:
        self._session.detach()

    __del__ = destroy

    def change_token(self, token: str) -> None:
        """
        Change client's token.

        Parameters
        ----------
        token: str
            New token

        """
        self._token = token

    async def _rlapi_request(self, endpoint: str) -> List[Dict[str, Any]]:
        url = self.RLAPI_BASE + endpoint
        headers = {"Authorization": f"Token {self._token}"}
        # RL API returns JSON list on success
        data: List[Dict[str, Any]] = await self._request(url, headers)
        return data

    async def _request(
        self, url: str, headers: Optional[aiohttp.typedefs.LooseHeaders] = None
    ) -> Any:
        for tries in range(5):
            async with self._session.get(url, headers=headers) as resp:
                data = await json_or_text(resp)
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

    async def _get_stats(self, player_id: str, platform: Platform) -> Player:
        """
        Get player skills for player ID in selected platform.

        Parameters
        ----------
        player_id: str
            ID of player to find.
        platform: Platform
            Platform to search.

        Returns
        -------
        Player
            Requested player skills.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League API failed.
        PlayerNotFound
            The player could not be found.

        """
        endpoint = f"/{platform.name}/playerskills/{player_id}/"
        try:
            player = await self._rlapi_request(endpoint)
        except errors.HTTPException as e:
            if e.status == 400 and "not found" in e.message:
                raise errors.PlayerNotFound(
                    "Player with provided ID could not be "
                    f"found on platform {platform.name}"
                )
            raise

        return Player(
            player_id=player_id,
            platform=platform,
            tier_breakdown=self.tier_breakdown,
            data=player[0],
        )

    async def get_player(
        self, player_id: str, platform: Optional[Platform] = None
    ) -> Tuple[Player, ...]:
        """
        Get player skills for player ID by searching in all platforms.

        Parameters
        ----------
        player_id: str
            ID of player to find.
        platform: Platform, optional
            Platform to search, if not provided
            client will search on all platforms.

        Returns
        -------
        `tuple` of `Player`
            Requested player skills.

        Raises
        ------
        HTTPException
            HTTP request to Rocket League or Steam API failed.
        PlayerNotFound
            The player could not be found on any platform.

        """
        if platform is not None:
            return (await self._get_stats(player_id, platform),)

        players: List[Player] = []
        for platform in Platform:
            try:
                players += await self._find_profile(player_id, platform)
            except errors.IllegalUsername as e:
                log.debug(str(e))
        if not players:
            raise errors.PlayerNotFound(
                "Player with provided ID could not be found on any platform."
            )

        return tuple(players)

    async def _find_profile(self, player_id: str, platform: Platform) -> Set[Player]:
        pattern = _PLATFORM_PATTERNS[platform]
        match = pattern.fullmatch(player_id)
        if not match:
            raise errors.IllegalUsername(
                f"Provided username doesn't match provided pattern: {pattern}"
            )

        players = set()
        if platform == Platform.steam:
            ids = await self._find_steam_ids(match)
        else:
            ids = [player_id]

        for player_id_to_find in ids:
            try:
                player = await self._get_stats(player_id_to_find, platform)
                players.add(player)
            except errors.PlayerNotFound as e:
                log.debug(str(e))
        return players

    async def _find_steam_ids(self, match: Match[str]) -> List[str]:
        player_id = match.group(2)
        search_type = match.group(1)
        if search_type is None:
            # code unreachable bug for Match[str]
            # see https://github.com/python/mypy/issues/7363
            search_types = ["profiles", "id"]  # type: ignore # mypy bug
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

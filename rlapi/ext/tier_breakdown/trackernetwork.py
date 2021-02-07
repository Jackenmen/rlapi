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

import logging
from collections import defaultdict
from typing import Any, Dict, List

from rlapi import Client, PlaylistKey, errors

log = logging.getLogger(__name__)

__all__ = ("get_tier_breakdown",)


async def get_tier_breakdown(
    client: Client,
) -> Dict[int, Dict[int, Dict[int, List[int]]]]:
    """
    Get tier breakdown from rocketleague.tracker.network.

    Parameters
    ----------
    client: `Client`
        Client object.

    Returns
    -------
    `dict`
        Tier breakdown.

    Raises
    ------
    HTTPException
        Downloading tier breakdown did not succeed.

    """
    tier_breakdown: Dict[int, Dict[int, Dict[int, List[int]]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for playlist_key in PlaylistKey:
        playlist_id = playlist_key.value
        try:
            result = await _get_playlist_breakdown(client, playlist_id)
        except errors.HTTPException:
            log.error("Downloading tier breakdown did not succeed.")
            raise

        data = result["data"]["data"]

        for breakdown in data:
            tier_id = breakdown["tier"]
            playlist_id = breakdown["playlist"]
            division_id = breakdown["division"]
            begin = breakdown["minMMR"]
            end = breakdown["maxMMR"]

            tier_breakdown[playlist_id][tier_id][division_id] = [begin, end]

        tier_breakdown[playlist_id].pop(0, None)

    return tier_breakdown


async def _get_playlist_breakdown(client: Client, playlist_id: int) -> Dict[str, Any]:
    url = f"https://api.tracker.gg/api/v1/rocket-league/distribution/{playlist_id}"
    # Tracker Network request returns html code
    text: Dict[str, Any] = await client._request(url)
    return text

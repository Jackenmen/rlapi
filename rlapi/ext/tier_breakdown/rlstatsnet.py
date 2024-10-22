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

import logging
import re
from collections import defaultdict
from typing import Dict, List

from lxml import etree

from rlapi import Client, PlaylistKey, errors
from rlapi.player import DIVISIONS, RANKS

log = logging.getLogger(__name__)

__all__ = ("get_tier_breakdown",)

_TIER_MAX = len(RANKS)
_DIVISION_MAX = len(DIVISIONS)
_TIER_IMAGE_PATH_RE = re.compile(r"/images/ranks/s\d+rank(?P<tier_id>\d+)\.png")
_DIVISION_RANGE_RE = re.compile(
    r"Division (?P<division>[IV]+)\W+(?P<begin>\d+) +to +(?P<end>-?\d+)"
)


async def get_tier_breakdown(
    client: Client,
) -> Dict[int, Dict[int, Dict[int, List[int]]]]:
    """
    Get tier breakdown from rlstats.net.

    Parameters
    ----------
    client: `rlapi.Client`
        Client object.

    Returns
    -------
    `dict`
        Tier breakdown.

    Raises
    ------
    HTTPException
        Downloading tier breakdown failed.
    ValueError
        Parsing downloaded tier breakdown failed.

    """
    tier_breakdown: Dict[int, Dict[int, Dict[int, List[int]]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    try:
        text = await client._request("https://rlstats.net/distribution")
    except errors.HTTPException:
        log.error("Downloading tier breakdowns did not succeed.")
        raise

    playlist_nodes = etree.HTML(text).findall(
        './/section[@id="distribution"]/div[2]/div[@data-playlist]'
    )

    for playlist_node in playlist_nodes:
        data_playlist = playlist_node.attrib["data-playlist"]
        try:
            playlist_id = PlaylistKey(int(data_playlist)).value
        except ValueError:
            # not a valid playlist
            log.warning("Found an unknown playlist: %s", data_playlist)
            continue

        # 3 `item`s per row, first row only has the max tier, rest of the rows are full
        tier_nodes = playlist_node.findall("./div[2]/div/div/div/item")

        # max tier only has one division with no upper bound
        tier_id = _TIER_MAX
        division_id = 0
        begin = int(tier_nodes[1].find("pre").text[:-1])
        end = 9999
        tier_breakdown[playlist_id][tier_id][division_id] = [begin, end]

        # rest of the tiers have normal ranges and 4 divisions
        for tier_node in tier_nodes[3:]:
            img_src = tier_node.find("img").attrib["src"]
            match = _TIER_IMAGE_PATH_RE.fullmatch(img_src)
            if match is None:
                raise ValueError(f"Unexpected tier image path: {img_src!r}")
            tier_id = int(match["tier_id"])

            for division_node in tier_node.findall("pre"):
                match = _DIVISION_RANGE_RE.fullmatch(division_node.text)
                if match is None:
                    raise ValueError(
                        f"Unexpected division range text: {division_node.text!r}"
                    )
                try:
                    division_id = DIVISIONS.index(match["division"])
                except ValueError:
                    # found a division in V-VIII range for some strange reason, ignore
                    continue
                begin = int(match["begin"])
                end = int(match["end"])
                tier_breakdown[playlist_id][tier_id][division_id] = [begin, end]

    return tier_breakdown

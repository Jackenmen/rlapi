import logging
from collections import defaultdict
from typing import Any, Dict, List

from rlapi import Client, errors
from rlapi.player import RANKS

log = logging.getLogger(__name__)

__all__ = ("get_tier_breakdown",)

TIER_MAX = len(RANKS)


async def get_tier_breakdown(
    client: Client,
) -> Dict[int, Dict[int, Dict[int, List[float]]]]:
    """
    Get tier breakdown from rltracker.pro.

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
    tier_breakdown: Dict[int, Dict[int, Dict[int, List[float]]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for tier_id in range(1, TIER_MAX):
        try:
            tier = await _get_division_stats(client, tier_id)
        except errors.HTTPException:
            log.error("Downloading tier breakdown did not succeed.")
            raise

        for breakdown in tier:
            playlist_id: int = breakdown["playlist_id"]
            division: int = breakdown["division"]
            begin = float(breakdown["from"])
            end = float(breakdown["to"])
            tier_breakdown[playlist_id][tier_id][division] = [begin, end]

    return tier_breakdown


async def _get_division_stats(client: Client, tier_id: int) -> List[Dict[str, Any]]:
    url = f"http://rltracker.pro/tier_breakdown/get_division_stats?tier_id={tier_id}"
    # RLTracker.pro API returns JSON list on success
    text: List[Dict[str, Any]] = await client._request(url)
    return text

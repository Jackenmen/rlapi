import asyncio
import logging
import time
from typing import Any, Dict, Optional, cast

import aiohttp

from ._utils import json_or_text
from .errors import HTTPException


log = logging.getLogger(__name__)


class PsynetConfig:
    BASE_URL = "https://config.psynet.gg/v2/Config/BattleCars"
    # This build ID is taken from the GitHub issue, noted as stable.
    # It can be made configurable later if needed.
    BUILD_ID = "-691922347"
    PLATFORM = "Prod"
    REGION = "Steam"  # The issue mentions Steam, so we'll use this for now.
    LANGUAGE = "INT"  # International

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._config_data: Optional[Dict[str, Any]] = None
        self._last_fetch_time: Optional[float] = None
        self._cache_duration = 3600  # Cache for 1 hour (in seconds)

    async def fetch_config(self, force_refresh: bool = False) -> Dict[str, Any]:
        if (
            self._config_data is not None
            and self._last_fetch_time is not None
            and (time.time() - self._last_fetch_time) < self._cache_duration
            and not force_refresh
        ):
            return cast(Dict[str, Any], self._config_data)

        url = (
            f"{self.BASE_URL}/{self.BUILD_ID}/"
            f"{self.PLATFORM}/{self.REGION}/{self.LANGUAGE}/"
        )
        log.debug(f"Fetching Psynet config from: {url}")

        for tries in range(5):
            async with self._session.get(url) as resp:
                data = await json_or_text(resp)
                if resp.status == 200:
                    self._config_data = data
                    self._last_fetch_time = time.time()
                    self._config_data = data
                    self._last_fetch_time = time.time()
                    return cast(Dict[str, Any], self._config_data)
                elif resp.status in {500, 502}:
                    log.warning(
                        f"Psynet config request failed with status {resp.status},"
                        f" retrying in {1 + tries * 2} seconds."
                    )
                    await asyncio.sleep(1 + tries * 2)
                    continue
                else:
                    raise HTTPException(resp, data)
        raise HTTPException(resp, data)

    def get_player_titles_data(self) -> Dict[str, Any]:
        if self._config_data is None:
            raise RuntimeError("Psynet config not fetched yet. Call fetch_config first.")
        # Assuming player titles data is under a specific key, e.g., "PlayerTitles"
        # This will need to be confirmed once we have a sample response.
        return cast(Dict[str, Any], self._config_data.get("PlayerTitles", {}))

    def get_population_data(self) -> Dict[str, Any]:
        if self._config_data is None:
            raise RuntimeError(
                "Psynet config not fetched yet. Call fetch_config first."
            )
        # Assuming population data is under a specific key, e.g., "Population"
        # This will need to be confirmed once we have a sample response.
        return cast(Dict[str, Any], self._config_data.get("Population", {}))

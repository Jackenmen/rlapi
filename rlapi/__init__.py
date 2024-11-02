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

__author__ = "Jakub Kuczys (Jackenmen)"

__license__ = "Apache License 2.0"
__copyright__ = "Copyright (c) 2018-present Jakub Kuczys"

import logging
import pkgutil

from . import errors as errors  # noqa
from .client import Client as Client  # noqa
from .enums import Platform as Platform, PlaylistKey as PlaylistKey  # noqa
from .errors import (  # noqa
    HTTPException as HTTPException,
    IllegalUsername as IllegalUsername,
    PlayerNotFound as PlayerNotFound,
    RLApiException as RLApiException,
    Unauthorized as Unauthorized,
)
from .player import (  # noqa
    DIVISIONS as DIVISIONS,
    PLAYLISTS_WITH_SEASON_REWARDS as PLAYLISTS_WITH_SEASON_REWARDS,
    RANKS as RANKS,
    SEASON_REWARDS as SEASON_REWARDS,
    Player as Player,
    PlayerStats as PlayerStats,
    Playlist as Playlist,
    SeasonRewards as SeasonRewards,
)
from .population import (  # noqa
    KNOWN_POPULATION_PLAYLISTS as KNOWN_POPULATION_PLAYLISTS,
    PlatformPopulation as PlatformPopulation,
    Population as Population,
    PopulationEntry as PopulationEntry,
    PopulationPlaylist as PopulationPlaylist,
)

pkg = pkgutil.get_data(__package__, "VERSION")
__version__ = pkg.decode("ascii").strip() if pkg is not None else ""

del pkg
del pkgutil

log = logging.getLogger(__name__)

__all__ = (
    "errors",
    "log",
    # client
    "Client",
    # enums
    "Platform",
    "PlaylistKey",
    # errors
    "HTTPException",
    "IllegalUsername",
    "PlayerNotFound",
    "RLApiException",
    "Unauthorized",
    # player
    "DIVISIONS",
    "PLAYLISTS_WITH_SEASON_REWARDS",
    "RANKS",
    "SEASON_REWARDS",
    "Player",
    "PlayerStats",
    "Playlist",
    "SeasonRewards",
    # population
    "KNOWN_POPULATION_PLAYLISTS",
    "PlatformPopulation",
    "Population",
    "PopulationEntry",
    "PopulationPlaylist",
)

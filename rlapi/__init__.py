__author__ = "Jakub Kuczys (jack1142)"

__license__ = "MIT License"
__copyright__ = "Copyright (c) 2018-2020 Jakub Kuczys"

import logging
import pkgutil

from . import errors as errors  # noqa
from .client import Client as Client  # noqa
from .enums import Platform as Platform  # noqa
from .enums import PlaylistKey as PlaylistKey  # noqa
from .errors import HTTPException as HTTPException  # noqa
from .errors import IllegalUsername as IllegalUsername  # noqa
from .errors import PlayerNotFound as PlayerNotFound  # noqa
from .errors import RLApiException as RLApiException  # noqa
from .errors import Unauthorized as Unauthorized  # noqa
from .player import Player as Player  # noqa
from .player import Playlist as Playlist  # noqa
from .player import SeasonRewards as SeasonRewards  # noqa

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
    "Player",
    "Playlist",
    "SeasonRewards",
)

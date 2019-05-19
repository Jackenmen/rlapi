__author__ = 'Jakub Kuczys (jack1142)'

__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 Jakub Kuczys'

import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()

import logging

from .client import Client  # noqa
from .errors import *  # noqa
from . import errors  # noqa
from .enums import Platform, PlaylistKey  # noqa
from .player import Playlist, SeasonRewards, Player  # noqa

log = logging.getLogger(__name__)

del pkgutil

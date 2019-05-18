__author__ = 'Jakub Kuczys (jack1142)'

__version__ = '0.1.0a1'

__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 Jakub Kuczys'

import logging

from .client import Client  # noqa
from .errors import *  # noqa
from . import errors  # noqa
from .enums import Platform, PlaylistKey  # noqa
from .player import Playlist, SeasonRewards, Player  # noqa

log = logging.getLogger(__name__)

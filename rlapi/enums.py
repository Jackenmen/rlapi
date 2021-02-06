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

from enum import Enum, IntEnum

__all__ = ("PlaylistKey", "Platform")


class PlaylistKey(IntEnum):
    """Represents playlist's key.

    .. container:: operations

        ``str(x)``
            Returns playlist's friendly name, e.g. "Solo Duel"
    """

    #: The Solo Duel playlist.
    solo_duel = 10
    #: The Doubles playlist.
    doubles = 11
    #: The Standard playlist.
    standard = 13
    #: The Hoops playlist.
    hoops = 27
    #: The Rumble playlist.
    rumble = 28
    #: The Dropshot playlist.
    dropshot = 29
    #: The Snow Day playlist.
    snow_day = 30
    #: The Tournaments "playlist".
    #: This is used to determine the rank for automatic tournaments.
    tournaments = 34

    def __str__(self) -> str:
        # pylint: disable=no-member
        return self.name.replace("_", " ").title()


class Platform(Enum):
    """Represents platform name.

    .. container:: operations

        ``str(x)``
            Returns platform's friendly name, e.g. "Xbox One"
    """

    value: str
    #: The Steam platform.
    steam = "Steam"
    #: The Playstation 4 platform.
    ps4 = "Playstation 4"
    #: The Xbox One platform.
    xboxone = "Xbox One"
    #: The Epic Games platform.
    epic = "Epic Games"
    #: The Nintendo Switch platform.
    switch = "Nintendo Switch"

    def __str__(self) -> str:
        return self.value

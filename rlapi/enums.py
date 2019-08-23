from enum import Enum

__all__ = ("PlaylistKey", "Platform")


class PlaylistKey(Enum):
    """Represents playlist's key.

    .. container:: operations

        ``str(x)``
            Returns playlist's friendly name, e.g. "Solo Standard"
    """

    #: The Solo Duel playlist.
    solo_duel = 10
    #: The Doubles playlist.
    doubles = 11
    #: The Solo Standard playlist.
    solo_standard = 12
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

    def __str__(self) -> str:
        return self.value

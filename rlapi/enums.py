from enum import Enum

__all__ = ('PlaylistKey', 'Platform')


class PlaylistKey(Enum):
    """
    Represents playlist's key.
    """
    solo_duel = 10
    doubles = 11
    solo_standard = 12
    standard = 13
    hoops = 27
    rumble = 28
    dropshot = 29
    snow_day = 30

    def __str__(self) -> str:
        # pylint: disable=no-member
        return self.name.replace('_', ' ').title()


class Platform(Enum):
    """Represents platform name."""
    steam = 'Steam'
    ps4 = 'Playstation 4'
    xboxone = 'Xbox One'

    def __str__(self) -> str:
        return self.value

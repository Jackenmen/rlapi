API Reference
=============

The following section outlines the API of rlapi.

.. note::

    This module uses the Python logging module to log diagnostic and errors
    in an output independent way.  If the logging module is not configured,
    these logs will not be output anywhere.

Client
------

.. autoclass:: rlapi.Client
    :members:

Enumerations
------------

The API provides some enumerations for certain types of string to avoid the API
from being stringly typed in case the strings change in the future.

All enumerations are subclasses of `enum.Enum`.

.. autoclass:: rlapi.PlaylistKey
    :members:

.. autoclass:: rlapi.Platform
    :members:

Rocket League API Models
------------------------

Models are classes that are received from Rocket League API
and are not meant to be created by the user of the library.

.. autoclass:: rlapi.Player
    :members:

.. autoclass:: rlapi.PlayerStats
    :members:

.. autoclass:: rlapi.SeasonRewards
    :members:

.. autoclass:: rlapi.Playlist
    :members:

.. autoclass:: rlapi.tier_estimates.TierEstimates
    :members:

Useful Constants
----------------

The package provides a few constants that can be useful
when interpreting data from the API.

.. data:: rlapi.RANKS
    :value: ('Unranked', 'Bronze I', ..., 'Supersonic Legend')

    A sequence of rank names, indexed by the value of `Playlist.tier`.

    Rank names are only provided in the English language.

.. data:: rlapi.DIVISIONS
    :value: ('I', 'II', 'III', 'IV')

    A sequence of roman numerals for divisions,
    indexed by the value of `Playlist.division`.

.. data:: rlapi.SEASON_REWARDS
    :value: ('Unranked', 'Bronze', 'Silver', ..., 'Supersonic Legend')

    A sequence of season reward level names, indexed by the value of
    `SeasonRewards.level`.

    Season reward level names are only provided in the English language.

.. data:: rlapi.PLAYLISTS_WITH_SEASON_REWARDS
    :value: (PlaylistKey.solo_duel, PlaylistKey.doubles, ..., PlaylistKey.snow_day)

    A sequence of playlists that can advance player's season rewards.

Exceptions
----------

The following exceptions are thrown by the library.

.. automodule:: rlapi.errors
    :members:
    :show-inheritance:

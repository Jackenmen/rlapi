API Reference
=============

The following section outlines the API of rlapi.

.. note::

    This module uses the Python logging module to log diagnostic and errors
    in an output independent way.  If the logging module is not configured,
    these logs will not be output anywhere.

.. _platform-player-ids:

Platform Player IDs
-------------------

The API requires certain identifiers to be used when looking up the names
on each platform:

.. list-table:: Lookup identifiers per platform
    :widths: 7 15 15
    :header-rows: 1

    * - Platform name
      - Lookup by ID
      - Lookup by name
    * - Steam
      - Supported

        `SteamID <https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC>`__ (also known as steamID64)
      - Not recommended

        API matches the given name against non-unique display names cached by Rocket League's database.

        Note: This identifier is omitted by `Client.find_player()`.
    * - Epic Games
      - Supported

        `Epic Account ID <https://epicgames.com/help/c74/c79/a3659>`__
      - Supported

        `Epic Account display name <https://epicgames.com/help/c74/c79/a3260>`__

        Note: This is unique but may change over time.
    * - PlayStation
      - Supported

        `PSN Account ID <https://psn.flipscreen.games>`__ (not exposed by PSN / RL API)
      - Supported

        `PSN username (Online ID) <https://www.playstation.com/en-us/support/account/change-psn-online-id>`__

        Note: This is unique but may change over time.
    * - Xbox One
      - Supported

        `Xbox services ID (XUID) <https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/system/overviews/user/player-identity-xuser#xuser-identifiers>`__ (not exposed by Xbox network / RL API)
      - Supported

        `Xbox Gamertag <https://support.xbox.com/help/account-profile/profile/gamertag-update-faq>`__

        Note: This is unique but may change over time.
    * - Nintendo Switch
      - Unsupported by the API
      - Not recommended

        `Nintendo Nickname <https://www.nintendo.com/en-gb/Support/Nintendo-Account/How-to-Change-Nintendo-Account-Nickname-2482804.html>`__

        Note: The nicknames are not unique, it's recommended to use the linked Epic account instead.

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

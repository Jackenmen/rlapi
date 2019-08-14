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

All enumerations are subclasses of `enum`_.

.. _enum: https://docs.python.org/3/library/enum.html

.. class:: rlapi.PlaylistKey

    Represents playlist's key.

    .. container:: operations

        ``str(x)``
            Returns playlist's friendly name, e.g. "Solo Standard"

    .. attribute:: solo_duel

        The Solo Duel playlist.
    .. attribute:: doubles

        The Doubles playlist.
    .. attribute:: solo_standard

        The Solo Standard playlist.
    .. attribute:: standard

        The Standard playlist.
    .. attribute:: hoops

        The Hoops playlist.
    .. attribute:: rumble

        The Rumble playlist.
    .. attribute:: dropshot

        The Dropshot playlist.
    .. attribute:: snow_day

        The Snow Day playlist.

.. class:: rlapi.Platform

    Specifies :class:`rlapi.Player`'s platform.

    .. container:: operations

        ``str(x)``
            Returns platform's friendly name, e.g. "Xbox One"

    .. attribute:: steam

        Steam platform.
    .. attribute:: ps4

        Playstation 4 platform.
    .. attribute:: xboxone

        Xbox One platform.


Rocket League API Models
------------------------

Models are classes that are received from Rocket League API
and are not meant to be created by the user of the library.

.. automodule:: rlapi.player
    :members:

.. automodule:: rlapi.tier_estimates
    :members:

Exceptions
----------

The following exceptions are thrown by the library.

.. automodule:: rlapi.errors
    :members:
    :show-inheritance:

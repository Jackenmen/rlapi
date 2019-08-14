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

Introduction
============

This is the documentation for rlapi, a library for Python assisting
in creating applications using Rocket League API.

Prerequisites
-------------

rlapi works with Python 3.7 or higher. Support for earlier versions of Python is not provided.

Installing
----------

You can get the library directly from PyPI.

.. code-block:: shell

    python3.7 -m pip install -U rlapi

If you are using Windows, then the following should be used instead.

.. code-block:: shell

    py -3.7 -m pip install -U rlapi

Usage example
-------------

You can easily create a client using the class `rlapi.Client`.
Here's simple example showing how you can get player stats with this library:

.. code-block:: python3

    import asyncio
    import rlapi


    loop = asyncio.get_event_loop()

    client = rlapi.Client("token")
    players = loop.run_until_complete(client.get_player("kuxir97", None))

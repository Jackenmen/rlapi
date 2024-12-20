Introduction
============

This is the documentation for rlapi, a library for Python assisting
in creating applications using Rocket League API.

Prerequisites
-------------

rlapi works with Python 3.8 or higher. Support for earlier versions of Python is not provided.

Installing
----------

You can get the library directly from PyPI.

.. code-block:: shell

    python3.8 -m pip install -U rlapi

If you are using Windows, then the following should be used instead.

.. code-block:: shell

    py -3.8 -m pip install -U rlapi

Usage example
-------------

You can easily create a client using the class `rlapi.Client`.
Here's simple example showing how you can get player stats with this library:

.. code-block:: python3

    import asyncio

    import rlapi


    async def main():
        client = rlapi.Client(client_id="client id", client_secret="client secret")
        players = await client.get_player("kuxir97", None)


    asyncio.run(main())

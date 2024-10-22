# rlapi
> Async ready API wrapper for Rocket League API written in Python.

[![Sponsor on GitHub](https://img.shields.io/github/sponsors/Jackenmen?logo=github)](https://github.com/sponsors/Jackenmen)
[![Documentation Status](https://readthedocs.org/projects/rlapi/badge/)](https://rlapi.readthedocs.io/en/latest/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

> **Rocket League API is currently in closed beta and Psyonix doesn't give out access to it easily.**
>
> To request API access, you should contact Psyonix by email RLPublicAPI@psyonix.com and hope for positive response.

## Installation

**Python 3.8 or higher is required**

To install the library, you can just run the following command:

```sh
# Linux/OS X
python3.8 -m pip install -U rlapi

# Windows
py -3.8 -m pip install -U rlapi
```

To install the development version, replace `rlapi` with `git+https://github.com/Jackenmen/rlapi`

## Usage example

You can easily create a client using the class `Client`. Here's simple example showing how you can get player stats with this library:
```py
import asyncio

import rlapi


async def main():
    client = rlapi.Client(client_id="client id", client_secret="client secret")
    players = await client.get_player("kuxir97", None)


asyncio.run(main())
```

## Documentation

Read [rlapi's documentation](https://rlapi.readthedocs.io/en/latest/).

## Contributing

Please take a look at our [contributing guidelines](https://github.com/Jackenmen/rlapi/blob/main/.github/CONTRIBUTING.md) if you're interested in helping!


## License

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.

This project bundles [lxml-stubs](https://github.com/JelleZijlstra/lxml-stubs) which are distributed on Apache License 2.0

Contributing guidelines and issue templates are taken from [discord.py project](https://github.com/Rapptz/discord.py)

---

> Jakub Kuczys &nbsp;&middot;&nbsp;
> GitHub [@Jackenmen](https://github.com/Jackenmen)

# rlapi
> Async ready API wrapper for Rocket League API written in Python.

[![Build Status](https://travis-ci.com/jack1142/rlapi.svg)](https://travis-ci.com/jack1142/rlapi)
[![Documentation Status](https://readthedocs.org/projects/rlapi/badge/)](https://rlapi.readthedocs.io/en/latest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Installation

**Python 3.7 or higher is required**

To install the library, you can just run the following command:

```sh
# Linux/OS X
python3.7 -m pip install -U rlapi

# Windows
py -3.7 -m pip install -U rlapi
```

To install the development version, replace `rlapi` with `git+https://github.com/jack1142/rlapi`

## Usage example

You can easily create a client using the class `Client`. Here's simple example showing how you can get player stats with this library:
```py
import asyncio
import rlapi


loop = asyncio.get_event_loop()

client = rlapi.Client('token')
players = loop.run_until_complete(
    client.get_player('kuxir97', rlapi.Platform.steam)
)
```

## Documentation

Read [rlapi's documentation](https://rlapi.readthedocs.io/en/latest/).

## Contributing

Please take a look at our [contributing guidelines](https://github.com/jack1142/rlapi/blob/master/.github/CONTRIBUTING.md) if you're interested in helping!


## License

Distributed under the MIT license. See ``LICENSE`` for more information.

Contributing guidelines and issue templates are taken from [discord.py project](https://github.com/Rapptz/discord.py)

---

> Jakub Kuczys &nbsp;&middot;&nbsp;
> GitHub [@jack1142](https://github.com/jack1142)

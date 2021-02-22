# Copyright 2018-2020 Jakub Kuczys (https://github.com/jack1142)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
from typing import Any

import aiohttp

if sys.version_info[:2] >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("json_or_text",)


class AlwaysGreaterOrEqual:
    def __ge__(self, other: Any) -> Literal[True]:
        return True


async def json_or_text(resp: aiohttp.ClientResponse) -> Any:
    """
    Returns json dict, if response's content type is json,
    or raw text otherwise.

    Parameters
    ----------
    resp: `aiohttp.ClientResponse`
        Response object

    Returns
    -------
    `dict` or `str`
        Response data.

    """
    text: str = await resp.text(encoding="utf-8")
    if "application/json" in resp.headers[aiohttp.hdrs.CONTENT_TYPE]:
        return json.loads(text)
    return text

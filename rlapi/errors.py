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

from typing import Any, Dict, Union

import aiohttp

__all__ = (
    "RLApiException",
    "IllegalUsername",
    "PlayerNotFound",
    "HTTPException",
    "Unauthorized",
)


class RLApiException(Exception):
    """Base exception class for Rocket League API."""


class IllegalUsername(RLApiException):
    """Username has unallowed characters."""


class PlayerNotFound(RLApiException):
    """Username could not be found."""


class HTTPException(RLApiException):
    """Exception that's thrown when an HTTP request operation fails.

    Attributes
    ----------
    response: aiohttp.ClientResponse
        The response of the failed HTTP request.
    status: int
        The status code of the HTTP request.
    message: Union[str, dict]
        Details about error.
    """

    def __init__(
        self, response: aiohttp.ClientResponse, data: Union[Dict[str, Any], str]
    ) -> None:
        self.response = response
        self.status = response.status
        if isinstance(data, dict):
            self.message = data.get("detail", data)
        else:
            self.message = data
        super().__init__(
            f"{self.response.reason} (status code: {self.status}): {self.message}"
        )


class Unauthorized(HTTPException):
    """Exception that's thrown when status code 401 occurs."""

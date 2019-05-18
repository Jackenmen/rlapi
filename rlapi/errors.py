from typing import Union

import aiohttp

__all__ = (
    'RLApiException',
    'IllegalUsername',
    'PlayerNotFound',
    'HTTPException',
    'Unauthorized'
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
    def __init__(self, response: aiohttp.ClientResponse, data: Union[str, dict]):
        self.response = response
        self.status = response.status
        if isinstance(data, dict):
            self.message = data.get('detail', data)
        else:
            self.message = data
        super().__init__(
            f"{self.response.reason} (status code: {self.status}): {self.message}"
        )


class Unauthorized(HTTPException):
    """Exception that's thrown when status code 401 occurs."""

import json
import sys
from typing import Any, Callable

import aiohttp
from lxml import etree

if sys.version_info[:2] >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("json_or_text", "stringify")


_stringify: Callable[[etree._Element], str] = etree.XPath(  # type: ignore
    "string()", smart_strings=False
)


class AlwaysGreaterOrEqual:
    def __ge__(self, other: Any) -> Literal[True]:
        return True


def stringify(element: etree._Element) -> str:
    """
    Returns element node's text, stripped from whitespace.

    Parameters
    ----------
    element: `etree._Element`
        Element node object.

    Returns
    -------
    `str`
        Element node's text.

    """
    return _stringify(element).strip()


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

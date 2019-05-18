import json
from typing import Union

import aiohttp
from lxml import etree

__all__ = ('json_or_text', 'stringify')


_stringify = etree.XPath("string()")


def stringify(element: etree._Element):
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


async def json_or_text(resp: aiohttp.ClientResponse) -> Union[dict, str]:
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
    text = await resp.text(encoding='utf-8')
    if 'application/json' in resp.headers[aiohttp.hdrs.CONTENT_TYPE]:
        return json.loads(text)
    return text

import asyncio
from collections.abc import Awaitable
from typing import Any, Self, Tuple

import httpx
from bs4 import BeautifulSoup

from crawl.selector import HtmlNode, HtmlNodes, JsonNode, JsonNodes


class Response:
    def __init__(self, adaptee: httpx.Response) -> None:
        self.__adaptee = adaptee

    @property
    def adaptee(self) -> httpx.Response:
        return self.__adaptee

    @property
    def request(self) -> httpx.Request:
        return self.adaptee.request

    @property
    def url(self) -> httpx.URL:
        return self.__adaptee.url

    @property
    def status_code(self) -> Any:
        return self.__adaptee.status_code

    @property
    def encoding(self) -> Any:
        return self.__adaptee.encoding

    @property
    def headers(self) -> httpx.Headers:
        return self.__adaptee.headers

    @property
    def cookies(self) -> httpx.Cookies:
        return self.__adaptee.cookies

    @property
    def content(self) -> Any:
        return self.__adaptee.content

    @property
    def text(self) -> Any:
        return self.__adaptee.text

    @property
    def dom(self) -> HtmlNode:
        return HtmlNode.from_string(self.text, base_url=str(self.url))

    @property
    def bs4(self) -> BeautifulSoup:
        return BeautifulSoup(self.text, "lxml")

    @property
    def json(self) -> Any:
        return self.__adaptee.json()

    def xpath(self, query: str) -> HtmlNodes:
        return self.dom.xpath(query)

    def css(self, query: str) -> HtmlNodes:
        return self.dom.css(query)

    def jsonpath(self, query: str) -> Any:
        return JsonNode(self.json).jsonpath(query)

    def jmespath(self, query: str) -> Any:
        return JsonNode(self.json).jmespath(query)


class Session:
    """asyncio http client

    Returns:
        _type_: _description_
    """

    @property
    def session(self) -> httpx.AsyncClient:
        return self._

    def __init__(self, http2: bool = True, *args: Any, **kws: Any) -> None:
        self._: httpx.AsyncClient = httpx.AsyncClient(*args, **kws)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.session.aclose()

    async def request(self, method: str, url: str, **kws: Any) -> Response:
        request = self.session.build_request(method, url, **kws)
        response = await self.session.send(request)
        return Response(response)

    def connect(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("CONNECT", url, **kws)

    def delete(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("DELETE", url, **kws)

    def get(self, url: str, **kws: Any) -> Awaitable[Response]:
        return self.request("GET", url, **kws)

    def head(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("HEAD", url, **kws)

    def options(self, url: str, **kws: Any) -> Awaitable[Response]:
        return self.request("OPTIONS", url, **kws)

    def patch(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("PATCH", url, **kws)

    def post(self, url: str, **kws: Any) -> Awaitable[Response]:
        return self.request("POST", url, **kws)

    def put(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("PUT", url, **kws)

    def trace(self, url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
        return self.request("TRACE", url, **kws)


async def request(method: str, url: str, **kws: Tuple[str, ...]) -> Response:
    async with Session(http1=False, http2=True) as session:
        return await session.request(method, url, **kws)


def connect(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("CONNECT", url, **kws)


def delete(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("DELETE", url, **kws)


def get(url: str, **kws: Any) -> Awaitable[Response]:
    return request("GET", url, **kws)


def head(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("HEAD", url, **kws)


def options(url: str, **kws: Any) -> Awaitable[Response]:
    return request("OPTIONS", url, **kws)


def patch(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("PATCH", url, **kws)


def post(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("POST", url, **kws)


def put(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("PUT", url, **kws)


def trace(url: str, **kws: Tuple[str, ...]) -> Awaitable[Response]:
    return request("TRACE", url, **kws)

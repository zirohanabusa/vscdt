import asyncio
import typing

import pytest
from aiohttp import web


def test_import_requests_module() -> None:
    imported: bool = False
    try:
        from crawl.aiorequests import Response, Session, connect, delete, get, head, options, patch, post, put, request

        imported = True
    except BaseException:
        pass
    assert imported is True


@pytest.mark.asyncio  # Error: unused "type: ignore[misc]"
async def test_http_requests(aiohttp_server: typing.Callable[[typing.Any], typing.Any]) -> None:
    from crawl.aiorequests import request

    app = web.Application()
    methods = (
        "delete",
        "get",
        "head",
        "options",
        "patch",
        "post",
        "put",
    )
    for method in methods:
        app.router.add_route(method, f"/{method}", recieve_request)
    srv = await aiohttp_server(app)
    for method in methods:
        url: str = f"http://{srv.host}:{srv.port}/{method}"
        res = await request(method, url)
        if method == "head":
            assert res.status_code == 200
        else:
            assert res.status_code == 200
            tag = res.bs4.title
            assert tag is not None
            title = tag.string
            assert isinstance(title, str) and title == method.upper()
            assert res.xpath("//ul/li").css(".http-request-method").get_text() == method.upper()


async def recieve_request(request: typing.Any) -> web.Response:
    return web.Response(
        text=f"""
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>{request.method}</title>
</head>
<body>
  <ul>
    <li>hoge</li>
    <li class="http-request-method">{request.method}</li>
  </ul>
</body>
</html>
"""
    )

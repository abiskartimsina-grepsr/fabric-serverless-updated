"""Implementation of the Request handler."""

import aiohttp
from typing import Dict, Final, Optional, Any

from proxy.handler import ProxyHandler
from options.options import RequestHandlerOptions

from dataclasses import dataclass

_DEFAULT_OPTIONS: Final[RequestHandlerOptions] = RequestHandlerOptions(
    auto_retry=True, crawl_delay_seconds=10, use_proxy=True, max_retries=5
)


@dataclass(frozen=True)
class Response:
    status: int
    body: str

    __slots__ = ("status", "body")


class RequestHandler:
    def __init__(self, config: Optional[RequestHandlerOptions] = None) -> None:
        self.options: RequestHandlerOptions = {**_DEFAULT_OPTIONS, **(config or {})}
        self.current_proxy: Optional[Dict] = None
        self.__proxy: Optional[ProxyHandler] = None

    async def requestGet(self, url: str, params: Optional[dict] = {}):
        async with aiohttp.ClientSession(
            proxy=self.proxy.current_proxy_as_string()
        ) as session:
            async with session.get(url, params=params, ssl=False) as response:
                return Response(status=response.status, body=await response.text())

    @property
    def proxy(self):
        if self.__proxy is None:
            self.__proxy = ProxyHandler()
        return self.__proxy

    @proxy.setter
    def proxy(self, _: Any) -> Exception:
        raise RuntimeError(
            "Do not set the proxy manually, use the `<handler>.proxy.switch()` method instead."
        )

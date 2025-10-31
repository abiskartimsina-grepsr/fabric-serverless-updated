from request_handler.proxy.proxy_providers.brightdata import BrightdataProxy
from request_handler.proxy.proxy_providers.oxylabs import OxylabsProxy
from enum import StrEnum
from typing import Any, Optional, Union


class ProxyVendors(StrEnum):
    BRIGHTDATA = "brightdata"
    OXYLABS = "oxylabs"


class ProxyProvider:
    def __init__(self, proxy_provider: ProxyVendors) -> None:
        self.provider: Optional[Union[OxylabsProxy, BrightdataProxy]] = None
        match proxy_provider.value:
            case "oxylabs":
                self.provider = OxylabsProxy()
                return
            case "brightdata":
                self.provider = BrightdataProxy()
                return

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.provider

from .abstract.provider import ProxyProviderAbstract
from typing import Dict


class OxylabsProxy(ProxyProviderAbstract):
    def __init__(self) -> None:
        super().__init__()

    def get_proxy_details() -> Dict[str, str]:
        pass

    def get_proxy_string() -> str:
        pass

    def vendor_name(self) -> str:
        return __class__.__name__

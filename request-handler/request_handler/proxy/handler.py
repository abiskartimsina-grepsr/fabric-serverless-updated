"""Proxy Handler."""

from typing import Optional, TypedDict
from enum import StrEnum

from request_handler.proxy.proxy_providers import ProxyVendors, ProxyProvider


class CurrentProxy(TypedDict):
    username: str
    password: str
    hostname: str
    port: str
    country: str
    proxy_zone: str
    provider: str


class ProxyZones(StrEnum):
    UNBLOCKER = "unblocker"
    RESIDENTIAL = "residential"
    GENERAL = "general"
    DATA_CENTER = "data_center"
    GREPSR = "grepsr"


class ProxyHandler:
    def __init__(self) -> None:
        self.zone: Optional[ProxyZones] = None
        self.__proxy_provider: ProxyProvider = ProxyProvider(ProxyVendors.BRIGHTDATA)
        self.current_proxy: Optional[CurrentProxy] = None

    def enable(self, zone: str, country: Optional[str] = None) -> None:
        if country is None:
            country = "US"

        try:
            self.zone = ProxyZones(zone.strip().lower())
        except ValueError:
            raise Exception(f"`{zone}` is not a supported zone.")

        self.__proxy_provider().country = country
        self.__proxy_provider().zone = self.zone.value

    def use_vendor(self, proxy_vendor: str) -> None:
        try:
            provider = ProxyVendors(proxy_vendor.strip())
            self.__proxy_provider = ProxyProvider(provider)
        except ValueError:
            raise Exception(f"`{proxy_vendor}` is not a supported proxy provider.")

    def switch(self):
        """Switch to a different proxy."""
        self.current_proxy = self.__proxy_provider().get_proxy_details()
        print(f"Switching Proxy Z:{self.__proxy_provider().zone} | C:{self.__proxy_provider().country}")

    def current_proxy_as_string(self):
        if self.current_proxy is not None:
            return f"http://{self.current_proxy['username']}:{self.current_proxy['password']}@{self.current_proxy['hostname']}:{self.current_proxy['port']}"
        return None

    def get_config(self):
        return self.current_proxy

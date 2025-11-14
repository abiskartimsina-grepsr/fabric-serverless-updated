from request_handler.proxy.proxy_providers.abstract.provider import ProxyProviderAbstract
from typing import Dict, TypedDict, Union
import os
from uuid import uuid4
import copy
import json


class _ProxyDetails(TypedDict):
    username: str
    password: str
    hostname: str
    port: Union[str, int]
    country: str
    proxy_zone: str
    provider: str


class BrightdataProxy(ProxyProviderAbstract):
    def __init__(self) -> None:
        super().__init__()
        self.__country: str = "US"
        self.__zone: str = "grepsr"
        self.secure_credentials = json.loads(os.getenv("BD_PROXY_CREDS",{}))
        self.__proxy_details = _ProxyDetails(
            username=self.secure_credentials.get("BD_PROXY_USERNAME"),
            password=self.secure_credentials.get("BD_PROXY_PASSWORD"),
            hostname=self.secure_credentials.get("BD_PROXY_HOSTNAME"),
            port=self.secure_credentials.get("BD_PROXY_PORT"),
            country=self.country,
            proxy_zone=self.zone,
            provider=self.vendor_name(),
        )

    def get_proxy_details(self) -> Dict[str, str]:
        __proxy_details = copy.copy(self.__proxy_details)
        __proxy_details["username"] = __proxy_details["username"].replace(
            "%ZONE%", self.zone
        )
        __proxy_details["username"] = __proxy_details["username"].replace(
            "%COUNTRY%", self.country
        )
        __proxy_details["username"] = __proxy_details["username"].replace(
            "%SESSION%", str(uuid4()).replace("-", "")
        )
        __proxy_details["country"] = self.country
        return __proxy_details

    @property
    def country(self):
        return self.__country.lower()

    @property
    def zone(self):
        return self.__zone.lower()

    @zone.setter
    def zone(self, zone: str):
        self.__zone = zone.strip().lower()

    @country.setter
    def country(self, country_code: str):
        if len(country_code) > 2:
            raise Exception("Country Code cannot be more than 2 letters long.")

        self.__country = country_code.lower()

    def vendor_name(self) -> str:
        return __class__.__name__

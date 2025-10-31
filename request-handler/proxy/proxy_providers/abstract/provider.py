from abc import ABC, abstractmethod, abstractproperty
from typing import Dict


class ProxyProviderAbstract(ABC):
    @abstractproperty
    def country(self):
        """Return the selected country."""

    @abstractproperty
    def zone(self):
        """Return the Proxy zone to use."""

    @abstractmethod
    def get_proxy_details() -> Dict[str, str]:
        """Return the Proxy Connection and Auth details."""

    @abstractmethod
    def vendor_name() -> str:
        """Return the current proxy vendor name."""

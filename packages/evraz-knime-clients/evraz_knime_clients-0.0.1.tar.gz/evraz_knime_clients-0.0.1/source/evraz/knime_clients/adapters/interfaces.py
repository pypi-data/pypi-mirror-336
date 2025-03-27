from abc import ABC, abstractmethod

from evraz.knime_clients.adapters.integration.sap_api import models
from evraz.knime_clients.adapters.integration.sap_api.params import (
    ReportFilter,
)


class CacheOperations(ABC):

    @abstractmethod
    def create_scheme(self, data, filename) -> None:
        ...

    @abstractmethod
    def get_scheme(self, filename) -> dict | None:
        ...


class ClientSAP(ABC):

    @abstractmethod
    def get_report(self, report_filter: ReportFilter) -> models.ReportSap:
        ...

    @abstractmethod
    def get_scheme(self, report_id: int) -> models.SchemeSap:
        ...

    @abstractmethod
    def set_auth(self, user: str, password: str) -> None:
        ...

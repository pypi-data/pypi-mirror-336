import logging

from jsonschema import validate

from evraz.knime_clients.adapters import interfaces
from evraz.knime_clients.adapters.integration.sap_api.models import ReportSap
from evraz.knime_clients.adapters.integration.sap_api.params import ReportFilter


class RequestsSAP:

    def __init__(
        self,
        client_sap: interfaces.ClientSAP,
        cache: interfaces.CacheOperations,
    ):
        self.client_sap = client_sap
        self.cache = cache
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_report_avl(self, idrep: int, month: int, year: int) -> ReportSap:
        self.logger.info(f'Request report {idrep} for a period {year}.{month})')
        # параметры запроса
        report_filter = ReportFilter(idrep=idrep, month=month, year=year)
        # получение схемы json для валидации данных из кэша или из SAP
        scheme = self.cache.get_scheme(idrep)

        if not scheme:
            scheme = self.client_sap.get_scheme(idrep).metadata
            self.cache.create_scheme(scheme, idrep)

        # получение данных по отчету и валидация
        report = self.client_sap.get_report(report_filter)
        report_data = report.data
        validate(instance=report_data, schema=scheme)
        self.logger.info(f'The report {idrep} is valid.')

        return report

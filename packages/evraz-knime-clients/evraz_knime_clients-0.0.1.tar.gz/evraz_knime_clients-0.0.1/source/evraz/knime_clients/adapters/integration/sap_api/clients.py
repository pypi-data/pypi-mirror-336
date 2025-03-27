import logging

import requests

from evraz.knime_clients.adapters import interfaces

from . import errors, models
from .params import ReportFilter


class ClientSAP(interfaces.ClientSAP):

    def __init__(
        self,
        url: str,
        client_id: int,
        password_sap: str,
        user_sap: str,
    ):
        self.url = url

        self._auth = password_sap, user_sap
        self._params = {'sap-client': client_id, 'json': 'X'}
        self._logger = logging.getLogger('ClientSAP')

    def set_auth(self, user_sap: str, password_sap: str):
        self._auth = user_sap, password_sap

    def get_report(self, report_filter: ReportFilter) -> models.ReportSap:
        """Запрашивает AVL отчет из SAP."""
        response = requests.post(
            self.url,
            json=report_filter.as_json,
            params=self._params,
            auth=self._auth
        )
        if not response.ok:
            raise errors.ResponseCodeError(
                response_code=response.status_code, text=response.text
            )

        return models.ReportSap.model_validate(response.json())

    def get_scheme(self, report_id: int) -> models.SchemeSap:
        """Запрашивает схему AVL отчета из SAP."""
        response = requests.get(
            url='/'.join([self.url, str(report_id)]),
            params=self._params,
            auth=self._auth
        )
        return models.SchemeSap.model_validate(response.json())

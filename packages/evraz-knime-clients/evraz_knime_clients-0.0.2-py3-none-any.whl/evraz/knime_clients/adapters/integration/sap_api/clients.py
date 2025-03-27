import logging

import requests

from evraz.knime_clients.adapters import interfaces

from . import errors, models
from .params import ReportFilter

SAP_STATUS_CODE_ERROR = '51'


class ClientSAP(interfaces.ClientSAP):

    def __init__(
        self,
        url: str,
        client_id: int,
        password_sap: str,
        user_sap: str,
    ):
        self.url = url
        self._auth = user_sap, password_sap
        self._params = {'sap-client': client_id, 'json': 'X'}
        self._logger = logging.getLogger('ClientSAP')

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
        response_sap = response.json()
        self._validate_response_sap(response_sap)

        return models.ReportSap.model_validate(response_sap)

    def get_scheme(self, report_id: int) -> models.SchemeSap:
        """Запрашивает схему AVL отчета из SAP."""
        response = requests.get(
            url='/'.join([self.url, str(report_id)]),
            params=self._params,
            auth=self._auth
        )
        if not response.ok:
            raise errors.ResponseCodeError(
                response_code=response.status_code, text=response.text
            )
        response_sap = response.json()
        self._validate_response_sap(response_sap)
        return models.SchemeSap.model_validate(response_sap)

    @staticmethod
    def _validate_response_sap(response_json) -> None:
        sap_header = models.HeaderSap.model_validate(response_json).header
        if sap_header.statusCode == SAP_STATUS_CODE_ERROR:
            raise errors.SapStatusException(
                message=sap_header.model_dump_json()
            )

from evraz.knime_clients.adapters.utils import AppError


class ResponseCodeError(AppError):
    msg_template = "Error response_code={response_code} text={text}))"
    code = 'knime_clients.sap.http_side_error'


class SapStatusException(AppError):
    msg_template = "Execution error on the SAP side {message}))"
    code = 'knime_clients.sap.sap_side_error'

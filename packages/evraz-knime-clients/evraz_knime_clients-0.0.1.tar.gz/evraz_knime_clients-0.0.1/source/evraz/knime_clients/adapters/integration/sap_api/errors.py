from evraz.knime_clients.adapters.utils import AppError


class ResponseCodeError(AppError):
    msg_template = "Error response_code={response_code} text={text}))"
    code = 'knime_clients.sap.response_code_error'

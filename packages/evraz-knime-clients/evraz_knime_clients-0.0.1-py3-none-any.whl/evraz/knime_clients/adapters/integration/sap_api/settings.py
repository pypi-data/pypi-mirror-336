from pydantic_settings import BaseSettings, SettingsConfigDict


class SapAuth(BaseSettings):
    PASSWORD: str | None = None
    USER: str | None = None
    CLIENT_ID: int = 550
    model_config = SettingsConfigDict(env_prefix='SAP_')


class SapUrls(BaseSettings):
    READREP: str = 'http://dvk.ur.evraz.com:8025/sap_erp/readrep'

    model_config = SettingsConfigDict(env_prefix='SAP_URL_')

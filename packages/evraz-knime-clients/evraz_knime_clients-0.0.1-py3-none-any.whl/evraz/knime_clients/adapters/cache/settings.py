from pydantic_settings import BaseSettings


class SettingsCache(BaseSettings):
    ROOT_PATH: str = 'metadata/'

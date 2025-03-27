import json
from pathlib import Path

from evraz.knime_clients.adapters import interfaces


class LocalCache(interfaces.CacheOperations):

    def __init__(self, root_cache: str):
        self.root_cache = root_cache
        self.extension = 'json'

    def create_scheme(self, data, report_id) -> None:
        """Сохраняет JSON схему данных."""
        filename = self.get_path(report_id)
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_scheme(self, report_id) -> dict | None:
        """Загружает JSON схему данных."""
        filename = self.get_path(report_id)
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return None

    def get_path(self, object_id: str) -> str:
        return f'{self.root_cache}{object_id}.{self.extension}'

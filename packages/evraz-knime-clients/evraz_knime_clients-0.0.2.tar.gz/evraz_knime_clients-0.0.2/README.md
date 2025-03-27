### Knime Clients
Библиотека дает класс для запросов к SAP.

### Пример использования
```
from evraz.knime_clients import create_sap_client

sap = create_sap_client(
    user='user',
    password=password1!',
    cache_path='metadata/',
)

report = sap.get_report_avl(
    idrep=1,
    month=3,
    year=2025,
)
```
### Сборка
```
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```
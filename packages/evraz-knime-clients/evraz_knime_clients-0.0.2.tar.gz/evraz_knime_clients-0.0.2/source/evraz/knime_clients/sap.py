from evraz.knime_clients.adapters import (
    SapAuth,
    SapUrls,
    SettingsCache,
    logging,
)
from evraz.knime_clients.adapters.cache.local_cache import LocalCache
from evraz.knime_clients.adapters.integration import tasks
from evraz.knime_clients.adapters.integration.sap_api.clients import ClientSAP

logging.configure()
sap_auth = SapAuth()
sap_urls = SapUrls()
settings_cache = SettingsCache()


def create_sap_client(
    user=sap_auth.USER,
    password=sap_auth.PASSWORD,
    cache_path=settings_cache.ROOT_PATH,
    url=sap_urls.READREP,
    client_id=sap_auth.CLIENT_ID,
):
    client_sap = ClientSAP(
        url=url,
        password_sap=password,
        user_sap=user,
        client_id=client_id,
    )
    cache = LocalCache(root_cache=cache_path)
    return tasks.RequestsSAP(client_sap, cache)

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

sap_auth, sap_urls = SapAuth(), SapUrls()
client_sap = ClientSAP(
    url=sap_urls.READREP,
    password_sap=sap_auth.PASSWORD,
    user_sap=sap_auth.USER,
    client_id=sap_auth.CLIENT_ID,
)

settings_cache = SettingsCache()
cache = LocalCache(root_cache=settings_cache.ROOT_PATH)


def create_sap_requests(user, password, cache_path):
    requests_sap = tasks.RequestsSAP(client_sap, cache)
    requests_sap.set_auth(user, password)
    cache.root_cache = cache_path
    return requests_sap

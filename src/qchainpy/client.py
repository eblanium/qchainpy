from .providers.authorization_provider import AuthorizationProvider
from .qdt import Qdt


class Client:
    __doc__ = """"""

    def __init__(self, api_url, key_path, passphrase=None):
        self._api_url = api_url if api_url.endswith('/') else api_url + '/'
        self._key_path = key_path
        self._authorization_provider = AuthorizationProvider(
            key_path=key_path,
            passphrase=passphrase
        )

    def get_client(self):
        return Qdt(
            api_url=self._api_url,
            authorization_provider=self._authorization_provider
        )

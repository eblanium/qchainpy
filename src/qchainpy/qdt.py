import json
from collections import OrderedDict
from urllib.parse import urlencode

import requests


class Qdt:
    __doc__ = """"""

    def __init__(self, api_url, authorization_provider):
        self._api_url = api_url
        self._authorization_provider = authorization_provider

    def transfer(self, token, amount, recipient):
        token = token.lower()
        request_url = self._api_url + 'transfer?' + urlencode(OrderedDict(token=token, amount=amount))
        if recipient.isdigit() or type(recipient) == int:
            data = {'account': recipient, 'signdata': {'account': recipient}}
        else:
            data = {'address': recipient, 'signdata': {'address': recipient}}
        sign = self._authorization_provider.get_sign(data)
        data = {'data': data, 'sign': sign}
        response = requests.post(
            url=request_url,
            data=json.dumps(data)
        )
        if response.ok:
            r = response.json()
            if r.get('success') == 'false':
                error = r.get('error')
                r.setdefault('explanation', self._map_error(error))
            return r
        return None

    def _map_error(self, error):
        if error == 'The specified file was not found':
            return 'Put your private key inside qnode folder'
        else:
            return 'Unknown'

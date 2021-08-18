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
        if str(recipient).isdigit() or type(recipient) == int:
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
        return response.json()

    def create_payment(self, payment_index, contract, token, amount, sender, recipient):
        token = token.lower()
        request_url = self._api_url + contract + '/new'
        data = {'payment': payment_index}
        if str(recipient).isdigit() or type(recipient) == int:
            data = {**data, **{'accountfrom': sender, 'accountto': recipient}}
        else:
            data = {**data, **{'addressfrom': sender, 'addressto': recipient}}
        data = {**data, **{
            'token': token,
            'amount': amount
        }}
        data = {**data, **{'signdata': data}}
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
        return response.json()

    def get_payment(self, payment_index, contract):
        request_url = self._api_url + contract + '/pay?' + urlencode(OrderedDict(index=payment_index))
        data = {'index': payment_index}
        response = requests.get(
            url=request_url
        )
        new_payment_index = response.json().get('index')
        if response.ok:
            r = response.json()
            if r.get('success') == 'false':
                error = r.get('error')
                r.setdefault('explanation', self._map_error(error))
            else:
                payments = r.get('payments')
                success = {'success': 'true'}
                if payment_index == 0:
                    r = {**success, **r}
                else:
                    payment = payments[0] if len(payments) == 1 else next((item for item in payments if item["index"] == payment_index), None)
                    r = {**success, **{
                        'payment': payment,
                        'index': r.get('index')
                    }}
            return r
        return response.json()

    def get_payments(self, contract):
        return self.get_payment(0, contract)

    def _map_error(self, error):
        if error == 'The specified file was not found':
            return 'Put your private key inside qnode folder'
        if error == 'must logged in':
            return 'Login into your node'
        if error == 'Insufficient funds':
            return 'Put some tokens on your node'
        if error == 'transfer yourself':
            return 'You cannot transfer funds from your node to your node'
        else:
            return 'Unknown'

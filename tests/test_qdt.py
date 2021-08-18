import os
import unittest
from pathlib import Path

from src.qchainpy.providers.authorization_provider import AuthorizationProvider
from src.qchainpy.qdt import Qdt


class TestQdtMethods(unittest.TestCase):
    def setUp(self):
        key_path = os.path.join(Path(__file__).resolve().parent, 'keys/private.key')
        passphrase = None
        self.ap = AuthorizationProvider(
            key_path=key_path,
            passphrase=passphrase
        )
        key_path = os.path.join(Path(__file__).resolve().parent, 'keys/contract.key')
        passphrase = None
        self.ap_contract = AuthorizationProvider(
            key_path=key_path,
            passphrase=passphrase
        )

    def test_transfer_to_node_id(self):
        url = os.getenv('API_URL', default=None)
        qdt = Qdt(
            api_url=url,
            authorization_provider=self.ap
        )
        response = qdt.transfer(
            token=os.getenv('TOKEN', default=None),
            amount=0.01,
            recipient='37542'
        )
        self.assertEqual(response.get('success'), 'true')

    def test_transfer_to_address(self):
        # This method doesn't work and API error is unknown
        url = os.getenv('API_URL', default=None)
        qdt = Qdt(
            api_url=url,
            authorization_provider=self.ap
        )
        response = qdt.transfer(
            token=os.getenv('TOKEN', default=None),
            amount=0.01,
            recipient='jFyrepKHm7F1MHN0kH0sfqLJn8H5WPU3'
        )
        self.assertEqual(response.get('success'), 'true')

    def test_no_private_key_on_api_node(self):
        url = 'http://212.8.240.85/api/'  # This public API url
        qdt = Qdt(
            api_url=url,
            authorization_provider=self.ap
        )
        response = qdt.transfer(
            token=os.getenv('TOKEN', default=None),
            amount=0.01,
            recipient='37542'
        )
        self.assertEqual(response.get('success'), 'false')

    def test_create_payment(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.create_payment(
            payment_index=0,
            contract='payments/eblanium',
            token='ebl',
            amount=0.01,
            sender=0,
            recipient=1
        )
        self.assertEqual(response.get('success'), 'true')

    def test_get_payments_eblanium(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/eblanium',
        )
        print(response)
        self.assertEqual(response.get('success'), 'true')

    def test_get_payment_powersmart(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payment(
            payment_index=3949652,
            contract='payments/powersmart',
        )
        payment = response.get('payment')
        paid = payment.get('status')
        new_payment_index = response.get('index')
        self.assertEqual(paid, 'paid')
        self.assertEqual(type(new_payment_index), int)


if __name__ == '__main__':
    unittest.main()

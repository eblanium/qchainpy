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
            contract='payments/eblanium',
            token='ebl',
            amount=0.01,
            sender=0,
            recipient=1,
            local_payment_id=4
        )
        self.assertEqual(response.get('success'), 'true')

    def test_get_payments_eblanium_all(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/eblanium',
        )
        self.assertGreater(len(response.get('payments')), 1)

    def test_get_payments_eblanium_one_without_index(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/eblanium',
            local_payment_id=3
        )
        self.assertEqual(response.get('payments')[0].get('payment'), 3)

    def test_get_payments_eblanium_two_with_index(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/eblanium',
            local_payment_id=4,
            index=3000000
        )
        self.assertEqual(len(response.get('payments')), 2)

    def test_get_payments_eblanium_not_found(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/eblanium',
            local_payment_id=99999,
            index=3000000
        )
        self.assertEqual(len(response.get('payments')), 0)

    def test_get_payment_powersmart(self):
        qdt = Qdt(
            api_url=os.getenv('API_URL', default=None),
            authorization_provider=self.ap_contract
        )
        response = qdt.get_payments(
            contract='payments/powersmart',
            local_payment_id=10115,
            index=3949652
        )
        self.assertEqual(response.get('payments')[0].get('account'), 30109)


if __name__ == '__main__':
    unittest.main()

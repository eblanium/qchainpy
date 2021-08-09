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


if __name__ == '__main__':
    unittest.main()

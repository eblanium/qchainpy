import os
import unittest
from pathlib import Path
from src.qchainpy.client import Client


class TestClientMethods(unittest.TestCase):
    def setUp(self):
        key_path = os.path.join(Path(__file__).resolve().parent, 'keys/private.key')
        self.client = Client(
            api_url=os.getenv('API_URL', default=None),
            key_path=key_path,
            passphrase=None
        ).get_client()

    def test_transfer_to_node_id(self):
        response = self.client.transfer(
            token=os.getenv('TOKEN', default=None),
            amount=0.01,
            recipient='37542'
        )
        self.assertEqual(response.get('success'), 'true')


if __name__ == '__main__':
    unittest.main()

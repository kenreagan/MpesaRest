import unittest
from MpesaRest import Mpesa
import os


class TestRestServices(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            'business_code': os.environ.get('BUSINESS_CODE') or '174379',
            'consumer_key': os.environ.get('CONSUMER_KEY') or 'GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
            'consumer_secret': os.environ.get('CONSUMER_SECRET') or "66olbx4MCiDMfoIz"
        }
        self.app = Mpesa(**config)

    def tearDown(self) -> None:
        pass

    def testApplicationCreation(self):
        self.assertIsNotNone(self.app.consumer_secret)
        self.assertIsNotNone(self.app.consumer_key)
        self.assertIsNotNone(self.app.business_code)

    def testValidityOfToken(self):
        self.assertTrue(self.app.isvalid_client())

    def testValidationOfPayload(self):
        pass


if __name__ == '__main__':
    unittest.main()

import unittest
from MpesaRest import Mpesa
import os


class TestRestServices(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            'business_code': os.environ.get('BUSINESS_CODE'),
            'consumer_key': os.environ.get('CONSUMER_KEY'),
            'consumer_secret': os.environ.get('CONSUMER_SECRET')
        }
        self.app = Mpesa(**config)

    def tearDown(self) -> None:
        pass

    def testApplicationCreation(self):
        self.assertIsNone(self.app.consumer_secret)
        self.assertIsNone(self.app.consumer_key)
        self.assertIsNone(self.app.business_code)

    def testValidityOfToken(self):
        self.assertFalse(self.app.isvalid_client())


if __name__ == '__main__':
    unittest.main()

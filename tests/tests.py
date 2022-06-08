import unittest
from MpesaRest import Mpesa


class TestRestServices(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            'business_code': 3000,
            'consumer_key': 'r231842222222254265hagho',
            'consumer_secret': 'tq32r73uifgwqie'
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


if __name__ == '__main__':
    unittest.main()

import unittest
from MpesaRest import Mpesa
import os
from MpesaRest.models import Base
from sqlalchemy import create_engine

base = os.path.abspath(os.path.dirname(__file__))


class TestRestServices(unittest.TestCase):
    def setUp(self) -> None:
        config = {
            'business_code': os.environ.get('BUSINESS_CODE') or '174379',
            'consumer_key': os.environ.get('CONSUMER_KEY') or 'GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
            'consumer_secret': os.environ.get('CONSUMER_SECRET') or "66olbx4MCiDMfoIz",
            'phone_number': '254 794784462'
        }
        self.engine = create_engine(
            'sqlite:///test.sqlite'
        )
        Base.metadata.create_all(self.engine)
        self.app = Mpesa(**config)

    def tearDown(self) -> None:
        Base.metadata.drop_all(self.engine)
        os.unlink('test.sqlite')

    def testApplicationCreation(self):
        self.assertIsNotNone(self.app.consumer_secret)
        self.assertIsNotNone(self.app.consumer_key)
        self.assertIsNotNone(self.app.business_code)

    def testValidityOfToken(self):
        self.assertTrue(self.app.isvalid_client())

    def testValidationOfPayload(self):
        pass

    def testTransaction(self):
        pass

    def testdatabasecreation(self):
        pass


if __name__ == '__main__':
    unittest.main()

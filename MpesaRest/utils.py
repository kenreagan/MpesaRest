from abc import ABC, abstractmethod
import requests
from requests.auth import HTTPBasicAuth
import datetime
from typing import Dict, Any
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import MutableMapping
from sqlalchemy import select, insert, delete
from MpesaRest.models import TransactionModels


class DatabaseContextManager:
    def __init__(self):
        self.engine = create_engine(
            'sqlite:///main.sqlite'
        )

        self.Session = sessionmaker(
            bind=self.engine
        )

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.session.rollback()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()



class DatabaseMapper(MutableMapping):
    def __init__(self):
        self.table = TransactionModels

    def __getitem__(self, item):
        with DatabaseContextManager() as context:
            statement = select(
                self.table
            )
            return context.session.execute(statement).fetchall()

    def __setitem__(self, key: int, value: Dict):
        with DatabaseContextManager() as context:
            statement = insert(
                self.table
            ).where(
                id=key
            ).values(
                **value
            )
            context.session.execute(statement)
            context.session.commit()

    def __delitem__(self, key):
        with DatabaseContextManager() as context:
            instance = delete(
                self.table
            ).where(
                id=key
            ).first()
            context.session.execute(instance)
            context.commit()

    def __len__(self):
        return len([elem for elem in self.__iter__()])

    def __iter__(self):
        with DatabaseContextManager() as context:
            for elements in context.session.query(self.table).all():
                yield  elements


class AbstractPaymentService(ABC):
    def __init__(self, consumer_key: str, consumer_secret: str, business_code: str):
        self.url = None
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_code = business_code

    def __repr__(self):
        return f"{self.__class__.__qualname__}(key={self.consumer_key}, secret={self.consumer_secret}," \
               f" code={self.business_code}) "

    def validate_details(self) -> requests.Response:
        """
        HttpBasicAuth to obtain the access token.
        :return: response.Response
        """

        self.url: str = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            self.url,
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )
        return response

    def start_validation(self) -> Dict[str, str]:
        """
        Prepare client details once the credentials are valid, else returns invalid credentials
        :return: Dict[str, str]
        """
        if self.isvalid_client():
            payment_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            passkey: str = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            data_to_encode = self.business_code + passkey + payment_time
            online_password = base64.b64encode(data_to_encode.encode())
            decode_password = online_password.decode('utf-8')
            my_dict = {
                "password": decode_password,
                "payment_time": payment_time
            }
            return my_dict
        return {
            'Message': "Invalid credentials"
        }

    # lipa na mpesa request processing
    def initialize_mpesa_stk_push_request(self, clientname: str, clientphonenumber: str, amount: int) -> int:
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        access_token = self.validate_details().json()
        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }

        request = {
            "BusinessShortCode": self.business_code,
            "Password": self.start_validation()['password'],
            "Timestamp": self.start_validation()['payment_time'],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": clientname,
            "PartyB": self.business_code,
            "PhoneNumber": clientphonenumber,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": self.business_code,
            "TransactionDesc": f"Confirm the payment of {amount!r} to {self.business_code!r} by entering your Mpesa pin"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return response.status_code

    def get_account_balance(self):
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query'
        body = {
            "Initiator": "",
            "SecurityCredential": "",
            "CommandID": "AccountBalance",
            "PartyA": self.business_code,
            "IdentifierType": "4",
            "Remarks": "",
            "QueueTimeOutURL": "",
            "ResultURL": ""
        }
        access_token = self.validate_details().json()
        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }
        requests.post(self.url, headers=headers, data=body)

    # request payment to client
    def request_payment(self, PartyA, PartyB, Amount, remarks):
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
        body = {
            "InitiatorName": "",
            "SecurityCredential": "",
            "CommandID": "",
            "Amount": Amount,
            "PartyA": PartyA,
            "PartyB": PartyB,
            "Remarks": remarks,
            "QueueTimeOutURL": "",
            "ResultURL": "",
            "Occasion": ""
        }
        access_token = self.validate_details().json()
        headers = {
            "Authorization: %s" % access_token['access_token']
        }
        requests.post(self.url, data=body, headers=headers)

    def initialize_b2c_requests(self, amount: str):
        # authentication: Bearer Access Token
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
        post_request_body = {
            "Command ID": "CustomerPayBillOnline",
            "Amount": amount,
            "Msisdn": "254724628580",
            "BillRefNumber": "00000",
            "ShortCode": self.business_code
        }

        access_token = self.validate_details().json()
        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }
        requests.post(self.url, data=post_request_body, headers=headers)

    # reverse Mpesa Transaction
    def reverse_transaction(self, amount, ReceiverParty, remarks):
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request'
        body = {
            "Initiator": "",
            "SecurityCredential": "",
            "CommandID": "TransactionReversal",
            "TransactionID": "",
            "Amount": amount,
            "ReceiverParty": ReceiverParty,
            "RecieverIdentifierType": "4",
            "ResultURL": "",
            "QueueTimeOutURL": "",
            "Remarks": remarks,
            "Occasion": ""
        }
        access_token = self.validate_details().json()

        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }

        requests.post(self.url, data=body, headers=headers)

    def query_transaction_status(self, partyA, remarks, transactionId):
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query'
        body = {
            "Initiator": "",
            "SecurityCredential": "",
            "CommandID": "TransactionStatusQuery",
            "TransactionID": transactionId,
            "PartyA": partyA,
            "IdentifierType": "",
            "ResultURL": "",
            "QueueTimeOutURL": "",
            "Remarks": remarks,
            "Occasion": ""
        }
        access_token = self.validate_details().json()
        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }
        requests.post(self.url, headers=headers, data=body)

    def query_stkpush_status(self, payment_code: Any) -> None:
        """
        Query Status of the client Payment [Completed, Pending, Cancelled]
        :param payment_code:
        Transaction id
        :return:
        None
        """
        self.url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
        body = {
            "BusinessShortCode": self.business_code,
            "Password": self.start_validation()['Password'],
            "Timestamp": self.start_validation()['Timestamp'],
            "CheckoutRequestID": payment_code
        }
        access_token = self.validate_details().json()
        headers = {
            "Authorization": access_token['access_token']
        }
        requests.post(self.url, data=body, headers=headers)

    @abstractmethod
    def isvalid_client(self):
        pass


class Validator(ABC):
    """
    Validate Input for accuracy
    """
    def __set_value(self, value):
        self.name = f"_{value}"

    def __set__(self, instance, value):
        self.validate(value)
        setattr(
            instance,
            self.name,
            value
        )

    def __get__(self, instance, owner=None):
        return getattr(instance, self.name)

    @abstractmethod
    def validate(self, value):
        pass

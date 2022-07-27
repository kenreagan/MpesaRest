from __future__ import annotations

import re
from typing import Dict, Union, Iterable
import requests
from requests.auth import HTTPBasicAuth
import datetime
from abc import ABC, abstractmethod
import base64
from dataclasses import dataclass


class Validator(ABC):

    def __init__(self):
        self.det = None

    def set_det(self, owner, detail):
        self.det = f'_{detail}'

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.det, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.det)

    @abstractmethod
    def validate(self, value):
        pass


class DictValidator(Validator):
    def __init__(self):
        super(DictValidator, self).__init__()
        self.errors = []

    def validate(self, value):
        phone_pattern = re.compile(r'[254]{3}\d{9}')
        if isinstance(value, dict):
            if not isinstance(value['amount'], (float, int)):
                error = ValueError(f'expected {value["amount"]!r} to be a float or integer')
                self.errors.append(error)
                raise error
            if not phone_pattern.match(value['phone']):
                error = ValueError("Enter The Correct Number Format start with 2547 ...")
                raise error
        else:
            raise ValueError(f'Expected {value!r} to be of type dict')


class IntValidator(Validator):
    def __init__(self):
        super(IntValidator, self).__init__()
        self.min_value = 1
        self.max_value = 300000

    def validate(self, value):
        if int(value) < self.min_value:
            raise ValueError('Value Outside range minimum range is %d' % self.min_value)

        if int(value) > self.max_value:
            raise ValueError('Value Outside range maximum range is %d' % self.max_value)


class StringValidator(Validator):
    def __init__(self):
        super(StringValidator, self).__init__()
        self.max_value = 100
        self.min_value = 1

    def validate(self, value):
        if len(value) < self.min_value:
            raise ValueError('Value Outside range minimum range is %d' % self.min_value)

        if len(value) > self.max_value:
            raise ValueError('Value Outside range maximum range is %d' % self.max_value)


@dataclass(repr=True)
class AbstractPaymentService(ABC):
    consumer_key: str
    consumer_secret: str
    business_code: int
    phone_number: str
    passcode: str
    call_back: str
    BusinessShortCode: str
    Accountreference:str
    environment: str


    def validate_details(self) -> requests.Response:
        """
        HttpBasicAuth to obtain the access token.
        :return: response.Response
        """

        url: str = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )
        return response

    def start_validation(self) -> Dict[str, str]:
        """
        Prepare client details once the credentials are valid, else returns invalid credentials
        :return: Dict[str, str]
        """
        payment_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        passkey: str = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        data_to_encode = str(self.business_code) + passkey + payment_time
        online_password = base64.b64encode(data_to_encode.encode())
        decode_password = online_password.decode('utf-8')
        my_dict = {
            "password": decode_password,
            "payment_time": payment_time
        }
        return my_dict
        

    # lipa na mpesa request processing
    def initialize_mpesa_stk_push_request(self, clientphonenumber: str, amount: int, description: str) -> Dict[str, str]:
        request = {
            "BusinessShortCode": self.BusinessShortCode,
            "Password": self.start_validation()['password'],
            "Timestamp": self.start_validation()['payment_time'],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": clientphonenumber,
            "PartyB": self.business_code,
            "PhoneNumber": clientphonenumber,
            "CallBackURL": self.call_back,
            "AccountReference": self.Accountreference,
            "TransactionDesc": description
        }

        return request

    def get_account_balance(self):
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
        return body

    # request payment to client
    def request_payment(self, clientphonenumber, Amount, remarks):
        body = {
            "InitiatorName": "",
            "SecurityCredential": "",
            "CommandID": "",
            "Amount": Amount,
            "PartyA": self.business_code,
            "PartyB": clientphonenumber,
            "Remarks": remarks,
            "QueueTimeOutURL": "",
            "ResultURL": "",
            "Occasion": ""
        }

        return body

    def initialize_c2b_requests(self, amount: str, client: str):
        # authentication: Bearer Access Token
        post_request_body = {
            "Command ID": "CustomerPayBillOnline",
            "Amount": amount,
            "Msisdn": client,
            "BillRefNumber": "00000",
            "ShortCode": self.business_code
        }
        return post_request_body

    # reverse Mpesa Transaction
    def reverse_transaction(self, amount, remarks, security_credential):
        body = {
            "Initiator": "",
            "SecurityCredential": "",
            "CommandID": "TransactionReversal",
            "TransactionID": "",
            "Amount": amount,
            "ReceiverParty": self.business_code,
            "RecieverIdentifierType": "4",
            "ResultURL": "",
            "QueueTimeOutURL": "",
            "Remarks": remarks,
            "Occasion": ""
        }
        return body

    def query_transaction_status(self, partyA, remarks, transactionId):
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

        return body

    def query_stkpush_status(self, payment_code: str):
        body = {
            "BusinessShortCode": self.business_code,
            "Password": self.start_validation()['Password'],
            "Timestamp": self.start_validation()['Timestamp'],
            "CheckoutRequestID": payment_code
        }
        return body


class StartService(AbstractPaymentService):
    def __init__(self, *args, **kwargs) -> None:
        super(StartService, self).__init__(*args, **kwargs)
        self.detail_validator = self.validate_details()
        self.access_token = None
        if self.detail_validator.status_code == 200:
            self.access_token: str = self.detail_validator.json()['access_token']
            self.headers = {
                "Authorization": "Bearer %s" % self.access_token
            }
            self._env = 'api' if self.environment == 'production' else 'sandbox'


    def __repr__(self):
        return f"{self.__class__.__qualname__}(" \
               f"business code = {self.business_code}, phone_number={self.phone_number})"

    def prompt_payment_for_service(self, values: Union[Iterable, Dict[str, str]]):
        if self.access_token is not None:
            validator = DictValidator()
            string_validator = StringValidator()
            api_url = f"https://{self._env}.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

            if isinstance(values, dict):
                validator.validate(value=values)
                string_validator.validate(values['description'])
                if not validator.errors:
                    body =  self.initialize_mpesa_stk_push_request(
                        values['phone'],
                        values['amount'],
                        values['description']
                    )
                    req = requests.post(api_url, body, headers=self.headers)
                    response = req.json()

                    if req.status_code != 200:
                        out_ = {
                            'errors': [
                                response['errorMessage']
                            ]
                        }
                        return out_
                    out_ = {
                        'Response': {
                            'Message': response['CustomerMessage'],
                            'Code': response['ResponseCode'],
                            'Description': response['ResponseDescription'],
                            'MerchantID': response['MerchantRequestID'],
                            'CustomerID': response['CheckoutRequestID']
                        }
                    }
                    return out_
                else:
                    for errors in validator.errors:
                        print(errors)
            else:
                for items in values:
                    self.prompt_payment_for_service(items)

    def check_lipa_na_mpesa_status(self, code):
        validator = StringValidator()
        if validator.validate(code):
            body = self.query_stkpush_status(code)
            url = f'https://{self._env}.safaricom.co.ke/mpesa/stkpushquery/v1/query'
            response = requests.post(
                url,
                data=body,
                headers=self.headers
            )
            return response.json()


    def check_transaction_status(self, PartyA, remarks, transactionId):
        url = f'https://{self._env}.safaricom.co.ke/mpesa/transactionstatus/v1/query'
        body = self.query_transaction_status(PartyA, remarks, transactionId)
        req = requests.post(
            url,
            data=body,
            headers=self.headers
        )
        return req.json()

    def initialize_business_to_client(self, PartyA:str, Amount: float, Remarks: str):
        url = f'https://{self._env}.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
        body = self.request_payment(clientphonenumber, Amount, Remarks)
        req = requests.post(
            url,
            data=body,
            headers=self.headers
        )
        return req.json()

    def reverse_customer_transaction(self, amount, remarks: str, cred):
        body = self.reverse_transaction(amount, remarks, cred)
        url = f'https://{self._env}.safaricom.co.ke/mpesa/reversal/v1/request'
        req = requests.post(
            url,
            data=body,
            headers=self.headers
        )
        return req.json()

    def check_account_balance(self):
        url = f'https://{self._env}.safaricom.co.ke/mpesa/accountbalance/v1/query'
        body = self.get_account_balance()
        req = requests.post(
            url,
            data=body,
            headers=self.headers
        )
        return req.json()

    def initialize_buy_goods(self, amount, client):
        url = f'https://{self._env}.safaricom.co.ke/mpesa/c2b/v1/simulate'
        body = self.initialize_c2b_requests(
            amount,
            client
        )

        req = requests.post(
            url,
            data=body
        )

        return req.json()

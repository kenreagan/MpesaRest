from abc import ABC, abstractmethod
import requests
from requests.auth import HTTPBasicAuth
import datetime
from typing import Dict
import base64


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
        self.url: str = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            self.url,
            auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )
        return response

    def start_validation(self) -> Dict[str, str]:
        if self.isvalid_client():
            payment_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            passkey: str = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            data_to_encode = self.business_code + passkey + payment_time
            online_password = base64.b64encode(data_to_encode.encode())
            decode_password = online_password.decode('utf-8')
            my_dict = {
                "password": decode_password,
                "payment_time": payment_time,
                'Business_short_code': self.business_code
            }
            return my_dict
        return {
            'Message': "Invalid credentials"
        }

    def initialize_mpesa_stk_push_request(self, clientname: str, clientphonenumber: str, amount: int) -> int:
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        access_token = self.validate_details().json()
        headers = {
            "Authorization": "Bearer %s" % access_token['access_token']
        }

        request = {
            "BusinessShortCode": self.start_validation()['Business_short_code'],
            "Password": self.start_validation()['password'],
            "Timestamp": self.start_validation()['payment_time'],
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": clientname,
            "PartyB": self.start_validation()['Business_short_code'],
            "PhoneNumber": clientphonenumber,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": self.business_code,
            "TransactionDesc": "Please enter your pin to ensure the correct amount is paid"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return response.status_code

    @abstractmethod
    def isvalid_client(self):
        pass


class Validator(ABC):
    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance

    @abstractmethod
    def validate(self, value):
        pass

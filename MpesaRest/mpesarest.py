from MpesaRest.utils import AbstractPaymentService, Validator, DatabaseMapper
from typing import Dict, Union, Iterable
import logging

logging.basicConfig(
    filename='mpesarest.log',
    format="[%(level)s] %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DictValidator(Validator):
    def __init__(self):
        self.errors = []

    def validate(self, value):
        if isinstance(value, dict):
            if not isinstance(value['amount'], (float, int)):
                error = ValueError(f'expected {value["amount"]!r} to be a float or integer')
                self.errors.append(error)
                raise error
            if not len(value['phone'].strip(' ')) == 13:
                error = ValueError("Enter The Correct Number Format start with +2547")
                raise error
        else:
            raise ValueError(f'Expected {value!r} to be of type dict')


class IntValidator(Validator):
    def __init__(self):
        min_value = None
        max_value = None

    def validate(self, value):
        pass

class stringValidator(Validator):
    def __init__(self):
        max_val = None
        min_val = None

    def validate(self, value):
        pass

class StartService(AbstractPaymentService):
    def isvalid_client(self) -> bool:
        return self.validate_details().status_code == 200 and self.validate_details().json() is not None

    def prompt_payment_for_service(self, values: Union[Iterable, Dict]):
        """
        >>> config = {
        ...     'consumer_key': '<YOURCONSUMERKEY>',
        ...     'consumer_secret': '<YOURCONSUMERSECRET>',
        ...     'BUSINESSCODE': '<YOURBUSINESSCODE'
        ... }
        >>> app = StartService(**config)
        >>> app.prompt_payment_for_service({
        ...     'name': 'lumuli',
        ...     'phone': '+254794784462',
        ...     'amount': 7000
        ...})
        "payment Success"
        >>>
        :param values:
        client_details: Dict[str, str]
        default = None
        :return:
        String
        """
        if self.isvalid_client():
            validator = DictValidator()
            if isinstance(values, dict):
                validator.validate(value=values)
                if not validator.errors:
                    self.initialize_mpesa_stk_push_request(
                        values['name'],
                        values['phone'],
                        values['amount']
                    )
                else:
                    for errors in validator.errors:
                        logger.critical(errors)
            else:
                for items in values:
                    self.prompt_payment_for_service(items)

    def check_lipa_na_mpesa_status(self, code):
        self.query_stkpush_status(code)

    def check_transaction_status(self, PartyA, remarks, transactionId):
        self.query_transaction_status(PartyA, remarks, transactionId)

    def request_from_customer(self, PartyA:str, PartyB:str, Amount: float, Remarks: str):
        self.request_payment(PartyA, PartyB, Amount, Remarks)

    def reverse_customer_transaction(self, amount, recipient: str, remarks: str):
        self.reverse_transaction(amount, recipient, remarks)

    def check_account_balance(self):
        return self.get_account_balance()

    @staticmethod
    def download_report(format, start_date, end_date):
        mapper = DatabaseMapper()
        return mapper

### Mpesa Rest Api
A special interaction with the Safaricom daraja Api using python
suitable for business payment integration. create your consumer key and consumer secret from the
[safaricom daraja developer's portal](https://developer.safaricom.com)

#### Installation

```commandline
pip install MpesaRest
```

#### Usage
##### Instantiate Business to client Lipa na Mpesa Stk Push
Prompt user to Accept Payment for your service using lipa na mpesa

```python
from MpesaRest.mpesarest import StartService as Mpesa
from typing import Any, Dict
import pprint

app = Mpesa(
    consumer_key='GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
    consumer_secret='66olbx4MCiDMfoIz',
    business_code=174379,
    passcode='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
    call_back='https://myapp.co.ke/',
    environment='development',
    phone_number=254794784462,
    BusinessShortCode=174379,
    Accountreference='MyCompany'
)


pay: Dict[str, Any] = app.prompt_payment_for_service({
    'phone': '254794784462',
    'amount': 3000,
    'description': 'pay for the service ...'
})

pprint.pprint(pay)

#### Check Transaction Status for transaction

status = app.check_lipa_na_mpesa_status(pay['CustomerID'])

pprint.pprint(status)

# One Can prompt for payment from multiple clients
mult = app.prompt_payment_for_service(
    [
        {
            'phone': '254794784462',
            'amount': 3000,
            'description': 'Pay for my service'
        },
        {
            'phone': '254794784462',
            'amount': 6000,
            'description': 'pay for cool project'
        }
    ]
)

pprint.pprint(mult)
```

##### Reverse Mpesa Transaction
```python
from MpesaRest import Mpesa

app = Mpesa(
    consumer_key='GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
    consumer_secret='66olbx4MCiDMfoIz',
    business_code=174379,
    passcode='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
    call_back='https://myapp.co.ke/',
    environment='development',
    phone_number=254794784462,
    BusinessShortCode=174379,
    Accountreference='MyCompany'
)

transaction = app.prompt_payment_for_service({
    'name': 'lumuli',
    'phone': '254794784462',
    'amount': 3000
})

credential = "gtuVU97sOygJeUCC+22dnZTYVfSseHMmbzQydjzbeQQrKU9hFfEljKINBw4iIhDqan417UPquzdoBND2F6e7r/4emGYzLPK9OBlTkUKB+rZx+ttNFyw0kq2+k93JMcaAAS9rbu3dZSw8mE47EHLE9PNQ0V8qdp0xhcLpi0GQptwBLQPD9gzKvSqz/E0hg1YisKFtOZizQ2PadX9KqxLKFYD1No/UJEXYEyduemKe6WmI/T7m5llYzIZRu3AdCcAF4JU8vFP/GMAn0uJB/xlGf5+23VV7Q/O+l/mkMXaN401EHO9OygTWiSf3+c8BN7wwpQQUCDh3T+mzWKc74AMZ6w=="
app.reverse_transaction(3000, transaction['CustomerID'], security_credential=credential)
```

##### Request payment from clients
```python
from MpesaRest.mpesarest import StartService as Mpesa

app = Mpesa(
    consumer_key='GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
    consumer_secret='66olbx4MCiDMfoIz',
    business_code=174379,
    passcode='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
    call_back='https://myapp.co.ke/',
    environment='development',
    phone_number=254794784462,
    BusinessShortCode=174379,
    Accountreference='MyCompany'
)

app.request_payment(254794784462, 3000, '')
```

#### Check Account Balance status
```python
from MpesaRest.mpesarest import StartService as Mpesa

app = Mpesa(
    consumer_key='GfcDOBUOM4oFzQpmq6QUYL2TR8rJXhvM',
    consumer_secret='66olbx4MCiDMfoIz',
    business_code=174379,
    passcode='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
    call_back='https://myapp.co.ke/',
    environment='development',
    phone_number=254794784462,
    BusinessShortCode=174379,
    Accountreference='MyCompany'
)

app.check_account_balance()
```

##### Contribution
Contribute by creating pull request
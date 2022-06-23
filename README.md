### Mpesa Rest Api
A special interaction with the Safaricom daraja Api using python
suitable for business payment integration. create your consumer key and consumer secret from the
[safaricom daraja developer's portal](https://developer.safaricom.com)

#### Installation

```commandline
pip3 install MpesaRest
```

#### Usage
##### Instantiate Business to client Lipa na Mpesa Stk Push
Prompt user to Accept Payment for your service using lipa na mpesa

```python
from MpesaRest import Mpesa

config = {
        'consumer_key': "YOUR_CONSUMER_KEY",
        'consumer_secret': "YOUR_CONSUMER_SECRET",
        'business_code': "YOUR_BUSINESS_CODE"
    }

app = Mpesa(**config)


app.prompt_payment_for_service({
    'name': 'lumuli',
    'phone': '254794784462',
    'amount': 3000
})

# One Can prompt for payment from multiple clients
app.prompt_payment_for_service(
    [
        {
            'name': 'lumuli',
            'phone': '254794784462',
            'amount': 3000
        },
        {
            'name': 'test',
            'phone': '254794784462',
            'amount': 6000
        }
    ]
)
```

##### Reverse Mpesa Transaction
```python
from MpesaRest import Mpesa

config = {
        'consumer_key': "YOUR_CONSUMER_KEY",
        'consumer_secret': "YOUR_CONSUMER_SECRET",
        'business_code': "YOUR_BUSINESS_CODE"
    }

app = Mpesa(**config)

app.prompt_payment_for_service({
    'name': 'lumuli',
    'phone': '+254794784462',
    'amount': 3000
})

app.reverse_transaction(3000, 'transaction_code', 'reversal for purchase of goods worth 300')
```

##### Request payment from clients
```python
from MpesaRest import Mpesa

config = {
        'consumer_key': "YOUR_CONSUMER_KEY",
        'consumer_secret': "YOUR_CONSUMER_SECRET",
        'business_code': "YOUR_BUSINESS_CODE"
    }

app = Mpesa(**config)

app.request_payment()
```

#### Check Account Balance status
```python
from MpesaRest import Mpesa

config = {
    'consumer_key': "YOUR_CONSUMER_KEY",
    'consumer_secret': "YOUR_CONSUMER_SECRET",
    'business_code': "YOUR_BUSINESS_CODE"
}

mpesa = Mpesa(**config)

mpesa.check_account_balance()
```

##### Contribution
Contribute by creating pull request
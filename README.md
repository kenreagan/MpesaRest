### Mpesa Rest Api
A special interaction with the Safaricom daraja Api using python
suitable for business payment integration. create your consumer key and consumer secret from the  
[https://developer.safaricom.com](safaricom daraja client portal)

##### Installation

```commandline
pip3 install MpesaRest
```
##### Usage
###### Instantiate B2C to client
Prompt user to Accept Payment for your service

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

# One Can prompt for payment from multiple clients
app.prompt_payment_for_service(
    [
        {
            'name': 'lumuli',
            'phone': '+254794784462',
            'amount': 3000
        },
        {
            'name': 'test',
            'phone': '+254794784462',
            'amount': 6000
        }
    ]
)
```

##### Download Report For the Transactions

```python
import datetime

app.download_report(format=['excel', 'CSV'], start_date=datetime.datetime.today(), end_date=datetime.datetime)
```

```
echo "{
    "message": "payment success"
}"
```
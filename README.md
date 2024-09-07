## Pallapay crypto payment gateway SDK

Easy to use SDK for pallapay crypto payment gateway, accept crypto in your website and get paid in cash.


#### Installation
```
pip install pallapay-python-sdk
```

#### Easy to use

First signup and [create your API Key in pallapay website](https://www.pallapay.com)

Then you can create a payment link:

```python
from pallapay.client import PallapayClient

api_key = "TEST_API_KEY"
secret_key = "TEST_API_KEY"

# Create payment link
pallapay_client = PallapayClient(apiKey=api_key, secret_key=secret_key)
created_payment = pallapay_client.create_payment(
    symbol="AED",
    amount="10",
    ipn_success_url="https://my_website.com/payment/success",
    ipn_failed_url="https://my_website.com/payment/failed",
    payer_email_address="johndoe@gmail.com",
    webhook_url="https://my_website.com/webhook",  # Optional
    payer_first_name="John",  # Optional
    payer_last_name="Doe",  # Optional
    note="YOUR CUSTOM NOTE",  # Optional
    order_id="YOUR_UNIQUE_ORDER_ID",  # Optional
)

print(created_payment.payment_link)
# Now you can redirect user to payment_link.
```

#### Handle Webhook

After user payment was done, we will call your WEBHOOK_URL. then you can validate the request and check if transaction was paid. 

```python
from pallapay.client import PallapayClient

def handle_webhook(request_body: dict):
    # Checking webhook request that pallapay will send to your WEBHOOK_URL

    api_key = "TEST_API_KEY"
    secret_key = "TEST_API_KEY"

    pallapay_client = PallapayClient(apiKey=api_key, secret_key=secret_key)
    webhook_data = pallapay_client.get_webhook_data(request_body=request_body)
    
    is_valid_webhook: bool = pallapay_client.is_valid_webhook_data(webhook_data=webhook_data)
    if is_valid_webhook:
        raise Exception("Invalid webhook data")
    
    is_paid = pallapay_client.is_paid_webhook_data(webhook_data=webhook_data)
    
    if is_paid:
        print('Successful Payment')
    else:
        print('Failed Payment')
```


#### Contribution

Contributions are highly appreciated either in the form of pull requests for new features, bug fixes or just bug reports.

----------------------------------------------

[Pallapay Website](https://www.pallapay.com)

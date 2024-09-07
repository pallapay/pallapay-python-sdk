from pallapay.client import PallapayClient


def create_payment():
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


if __name__ == '__main__':
    create_payment()

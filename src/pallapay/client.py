import hashlib
import hmac

from typing import List
from pydantic import validate_arguments
from pallapay.enums import PAID_STATUS
from pallapay.request import RequestsApi
from pallapay.schema import CreatePaymentRequestModel, PaymentResponseModel, WebhookDataModel, \
    WebhookDataResultModel, PaginatedPaymentResponseModel, PaginationModel, BalanceModel


class PallapayClient:
    __secret_key: str

    @validate_arguments
    def __init__(self, api_key: str, secret_key: str, base_url: str = 'https://app.pallapay.com') -> None:
        self.__secret_key = secret_key

        self.consumer = RequestsApi(
            base_url=base_url,
            api_key=api_key,
            secret_key=secret_key,
        )

    @validate_arguments()
    def get_all_balances(self) -> List[BalanceModel]:
        """
        :return: List[BalanceModel]
        """
        response = self.consumer.get('/api/v1/api/balances')
        response_json = response.json()

        data = []
        for payment in response_json['data']:
            data.append(BalanceModel(**payment))

        return data

    @validate_arguments()
    def get_balance_by_symbol(self, symbol: str) -> BalanceModel:
        """
        :param symbol: str = Currency symbol (required)
        :return: PaymentResponseModel
        """
        if symbol == "":
            Exception("Invalid symbol")

        response = self.consumer.get(f"/api/v1/api/balances/{symbol}")
        return BalanceModel(**response.json()['data'])

    @validate_arguments()
    def get_all_payments(self) -> PaginatedPaymentResponseModel:
        """
        :return: PaginatedPaymentResponseModel
        """
        response = self.consumer.get('/api/v1/api/payments')
        response_json = response.json()

        data = []
        for payment in response_json['data']:
            data.append(PaymentResponseModel(**payment))

        return PaginatedPaymentResponseModel(
            data=data,
            pagination=PaginationModel(**response_json['pagination'])
        )

    @validate_arguments()
    def get_payment_by_payment_request_id(self, payment_request_id: str) -> PaymentResponseModel:
        """
        :param payment_request_id: str = Payment request ID (required)
        :return: PaymentResponseModel
        """
        if payment_request_id == "":
            Exception("Invalid payment request ID")

        response = self.consumer.get(f"/api/v1/api/payments/{payment_request_id}")
        return PaymentResponseModel(**response.json()['data'])

    @validate_arguments()
    def create_payment(
            self,
            symbol: str,
            amount: str,
            ipn_success_url: str,
            ipn_failed_url: str,
            payer_email_address: str,
            webhook_url: str = None,
            payer_first_name: str = None,
            payer_last_name: str = None,
            note: str = None,
            order_id: str = None
    ) -> PaymentResponseModel:
        """
        :param symbol: str = Payment currency symbol, for example: AED (required)
        :param amount: str = Amount in selected currency (required)
        :param ipn_success_url: float = The URL that we redirect the user after successful payment (required)
        :param ipn_failed_url: str = The URL that we redirect the user after unsuccessful payment (required)
        :param payer_email_address: str = Payer email address (required)
        :param webhook_url: str = Custom webhook URL (optional)
        :param payer_first_name: str = Payer first name (optional)
        :param payer_last_name: str = Payer email address (optional)
        :param note = Custom data to get in callback (optional)
        :param order_id = Unique order ID to get in callback (optional)
        :return: dict
        """
        params = CreatePaymentRequestModel(
            symbol=symbol,
            amount=amount,
            ipn_success_url=ipn_success_url,
            ipn_failed_url=ipn_failed_url,
            payer_email_address=payer_email_address,
            webhook_url=webhook_url,
            payer_first_name=payer_first_name,
            payer_last_name=payer_last_name,
            note=note,
            order_id=order_id,
        ).dict(exclude_none=True)

        response = self.consumer.post('/api/v1/api/payments', json=params)
        return PaymentResponseModel(**response.json()['data'])

    @validate_arguments
    def get_webhook_data(self, request_body: dict) -> WebhookDataModel:
        """
        :param request_body: dict = Request body that you received in your webhook page (required)
        :return: WebhookDataModel
        """

        if "approval_hash" not in request_body or "data" not in request_body:
            raise Exception("approve_hash or data does not exist in webhook call.")

        return WebhookDataModel(
            data=WebhookDataResultModel(**request_body['data']),
            approval_hash=request_body['approval_hash']
        )

    @validate_arguments
    def is_valid_webhook_data(self, webhook_data: WebhookDataModel) -> bool:
        """
        :param webhook_data: WebhookDataModel = Webhook data model that you received (required)
        :return: bool
        """

        sorted_data = dict(sorted(webhook_data.data.dict().items()))
        approval_string = ""
        for item_name in sorted_data:
            item = sorted_data[item_name]
            if item:
                approval_string += str(item)

        signed_approval_hash = hmac.new(
            bytes(self.__secret_key, 'latin-1'),
            msg=bytes(approval_string, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().lower()

        return webhook_data.approval_hash == signed_approval_hash

    @validate_arguments
    def is_paid_webhook_data(self, webhook_data: WebhookDataModel) -> bool:
        """
        :param webhook_data: WebhookDataModel = Webhook data model that you received (required)
        :return: bool
        """

        return webhook_data.data.status == PAID_STATUS

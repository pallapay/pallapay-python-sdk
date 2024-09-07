from typing import List
from pydantic import BaseModel


class PaginationModel(BaseModel):
    total_count: int
    page_count: int
    page_size: int


class CreatePaymentRequestModel(BaseModel):
    symbol: str
    amount: str
    ipn_success_url: str
    ipn_failed_url: str
    payer_email_address: str
    webhook_url: str = None
    payer_first_name: str = None
    payer_last_name: str = None
    note: str = None
    order_id: str = None


class PaymentResponseModel(BaseModel):
    payment_request_id: str
    payment_link: str
    currency_symbol: str
    amount: str
    payer_email_address: str
    payment_status: str
    payer_first_name: str = None
    payer_last_name: str = None
    payment_currency: str = None
    payment_amount: str = None
    receiving_amount: str = None
    fee_paid_by: str = None
    payment_fee_amount: str = None
    ref_id: str = None
    note: str = None
    order_id: str = None


class PaginatedPaymentResponseModel(BaseModel):
    data: List[PaymentResponseModel]
    pagination: PaginationModel


class WebhookDataResultModel(BaseModel):
    payment_request_id: str
    payment_amount: str
    payment_currency: str
    payer_email_address: str
    status: str
    receiving_amount: str = None
    paid_cryptocurrency: str = None
    fee_amount: str = None
    fee_paid_by: str = None
    payer_first_name: str = None
    payer_last_name: str = None
    ref_id: str = None
    paid_at: str = None
    note: str = None
    order_id: str = None


class WebhookDataModel(BaseModel):
    data: WebhookDataResultModel
    approval_hash: str


class BalanceModel(BaseModel):
    asset: str
    value: str
    locked: str

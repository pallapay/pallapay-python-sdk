import pytest
from pallapay.client import PallapayClient


def init_payment_with_base_url():
    PallapayClient(api_key='TEST_API_KEY', secret_key='TEST_SECRET_KEY')
    print('Pallapay test payment client created successfully.')


def test_init_payment_with_wrong_base_url():
    with pytest.raises(Exception) as e:
        print(e)
        PallapayClient(base_url=12345)

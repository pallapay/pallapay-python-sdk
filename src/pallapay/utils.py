from typing import Any


def error_handler(func: Any) -> Any:
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        accepted_status_codes = [200, 201, 202, 204]
        if response.status_code not in accepted_status_codes:
            raise Exception('Api call error', response.json())
        return response
    return wrapper

import pynrfjprog.API

def _nrf_api_call(on_fail_message="Unknown error"):
    def inner_dec(f):
        def decorator(*args, **kwargs):
            try:
                f(*args, **kwargs)
                return True
            except pynrfjprog.API.APIError as e:
                print(on_fail_message)
                print(e)
                return False
        return decorator
    return inner_dec

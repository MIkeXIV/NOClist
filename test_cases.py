
from badsecAPIclient import APIclient as client


def test_cases(base_url, auth_end, users_end):
    timeout, attempts = 3, 3
    test = client(base_url, auth_end, users_end)
    test.get_auth_token(attempts, timeout)
    print(test.auth_token)
    test.generate_checksum()
    print(test.check_sum)
    response = test.get_users(attempts, timeout)
    print(response.status_code)
    dict_keyname = "userIDs"
    badsec_users = test.convert_response_to_dict(response, dict_keyname)
    print(badsec_users)

    

## Some sample test cases to test client side errors

## invalid_auth_endpoint = test_cases("http://127.0.0.1:8888", "/authen", "/users")
## invalid_user_endpoint = test_cases("http://127.0.0.1:8888", "/auth", "/userser")
## invalid_base_url = test_cases("http://0.0.0.0:8888", "/auth", "/users")


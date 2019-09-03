
from badsecAPIclient import APIclient as client
import sys


def main():
    timeout, attempts = 3, 3
    client1 = client("http://127.0.0.1:8888", '/auth', '/users')
    client1.get_auth_token(attempts, timeout)
    client1.generate_checksum()
    response = client1.get_users(attempts, timeout)
    dict_keyname = "userIDs"
    badsec_users = client1.convert_response_to_dict(response, dict_keyname)
    json_filename = "solution.json"
    client1.write_json_file(json_filename, badsec_users)


if __name__ == "__main__":
    main()
    print('Successfully queried user endpoint')
    sys.exit(0)
    

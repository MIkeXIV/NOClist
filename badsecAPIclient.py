
import requests
import hashlib
import json
import sys

class APIclient(object):


    def __init__(self, base_url, auth_endpoint, users_endpoint):
        self.base_url = base_url
        self.auth_endpoint = auth_endpoint
        self.users_endpoint = users_endpoint
        self.auth_token = None
        self.check_sum = None   
        
    
    def get_auth_token(self, num_of_attempts, timeout_dur):
        auth_response = self.make_get_request(self.auth_endpoint,
                                              num_of_attempts, timeout_dur)
        self.auth_token = auth_response.headers['Badsec-Authentication-Token']


    def generate_checksum(self):
        auth_str = self.auth_token + self.users_endpoint 
        auth_bytes = auth_str.encode()
        auth = hashlib.sha256(auth_bytes)
        self.check_sum = auth.hexdigest()


    def get_users(self, num_of_attempts, timeout_dur):
        user_response = self.make_get_request(self.users_endpoint, num_of_attempts,
                                              timeout_dur, req_headers={
                                                 'X-Request-Checksum' : self.check_sum,
                                                 })
        return user_response
        
        

    def make_get_request(self, endpoint, num_of_attempts, timeout_dur, req_headers={}):
        url = self.base_url + endpoint
        for attempt in range(num_of_attempts):
            try:
                response = requests.get(url, timeout=timeout_dur,
                                        headers=req_headers)
                valid_response = self.analyze_response(response)
                if valid_response:
                    return response
                
            except requests.exceptions.RequestException as e:
                print(e, end='\n\n')
        else:
            print(f'server could not process {endpoint} endpoint request',
                  'exit with err code 1')
            sys.exit(1)
    
    
    @staticmethod
    def analyze_response(response):
        if response.status_code != 200:
            print(f"bad response...{response.status_code}")
            return None
        return response
            
    
    @staticmethod
    def convert_response_to_dict(response, key_name):
        response_list = response.text.split('\n')
        response_dict = {key_name : response_list}
        return response_dict
      

    @staticmethod
    def write_json_file(file_out_name, data):
        with open(file_out_name, "w") as f:
            json.dump(data, f, indent=4)


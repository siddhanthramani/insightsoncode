import requests
import json

class HttpRequests():
    _BASE_URL = ""
    
    def send_fastcode_results(self, api_key, json_as_dict):
        session  = requests.Session()
        headers = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer {0}'.format(api_key)}
        api_url = self._BASE_URL + "/uploadlog"
        response = session.post(api_url, headers = headers, json = json_as_dict)

        if response.status != 200:
            print("ERROR IN CODE: Logging to insights on code failed as you do not have permission")
            response.raise_for_status()
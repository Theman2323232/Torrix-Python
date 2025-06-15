import requests

class ERLCAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.policeroleplay.community/v1/server/command"

    def send_hint(self, message):
        url = f"{self.base_url}/server/hint"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "message": message
        }
        response = requests.post(url, headers=headers, json=data)
        return response.status_code, response.text

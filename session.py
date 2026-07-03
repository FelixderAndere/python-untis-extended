from urllib import response

import requests
from dotenv import load_dotenv
import os
import datetime
from utils import rpcLogin, apiLogin

load_dotenv()

class session():
    def __init__(self, base_url: str, username: str, password: str) -> None:
        try:
            self.base_url = base_url + "/WebUntis" if not base_url.endswith("/WebUntis") else base_url
            self.username = username
            self.password = password

            self.session, self.jsessionid, self.token = apiLogin.login(self.base_url, username=username, password=password)
            
            if not self.jsessionid:
                raise RuntimeError("No JSESSIONID received.")
        
        except Exception as e: 
            raise RuntimeError("Failed Login")


    def login(self):
        self.send_request(self, "/login")


    def send_request(self, endpoint, params):
        """ Sends a GET request to the specified endpoint with the provided parameters."""
        base_url = self.base_url

        print("Base URL:", base_url)
        print("Endpoint:", endpoint)
        url = f"{base_url}{endpoint}"
        print("URL:", url)

        headers = {
            "User-Agent": "user",
            "Content-Type": "application/json",
        }
        headers["Cookie"] = f'JSESSIONID={self.jsessionid}'
        
        response = requests.get(url, params=params, headers=headers)

        print(response.status_code)

        return response.json()


if __name__ == "__main__":
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    s = session(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
    s.send_request(endpoint="/WebUntis/api/homeworks/lessons", params={"startDate": start.strftime("%Y%m%d"), "endDate": end.strftime("%Y%m%d")})

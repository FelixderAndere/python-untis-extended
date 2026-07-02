from urllib import response

import requests
from dotenv import load_dotenv
import os
import datetime
from utils import rpcLogin

load_dotenv()

class session():
    def __init__(self) -> None:
        self.base_url = os.getenv("BASE_URL")
        sessionResult = rpcLogin.login(self.base_url, username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
        self.jsessionid = sessionResult["sessionId"]
        print(f"{self.jsessionid = }")

    def login(self):
        self.send_request(self, "/login")


    def send_request(self, endpoint, params):
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
        print(response.text[:500])

        
        return response
    
if __name__ == "__main__":
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    s = session()
    s.send_request(endpoint="/WebUntis/api/homeworks/lessons", params={"startDate": start.strftime("%Y%m%d"), "endDate": end.strftime("%Y%m%d")})
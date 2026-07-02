import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

class session():
    def __init__(self) -> None:
        self.base_url = os.getenv("BASE_URL")
        self.jsessionid = os.getenv("JSESSIONID")
        # self.login()


    def login(self):
        self.send_request(self, "/login")


    def send_request(self, endpoint, params):
        base_url = self.base_url

        print("Base URL:", base_url)
        print("Endpoint:", endpoint)
        url = f"{base_url}{endpoint}"
        print("URL:", url)

        headers = {
            "User-Agent": "Agent",
            "Content-Type": "application/json",
        }

    
        headers["Cookie"] = f'JSESSIONID={self.jsessionid}'
        
        response = requests.get(url, params=params, headers=headers)


        response_data = response.json()
        print(response_data)
        
        return response_data
    
if __name__ == "__main__":
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    s = session()
    s.send_request(endpoint="/Webuntis/api/homeworks/lessons", params={"startDate": start.strftime("%Y%m%d"), "endDate": end.strftime("%Y%m%d")})
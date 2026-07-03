from urllib import response

import requests
from dotenv import load_dotenv
import os
import datetime
from utils import rpcLogin, apiLogin
from utils.jwt import decode_jwt_unverified

load_dotenv()

class session():
    def __init__(self, base_url: str, username: str, password: str) -> None:
        try:
            self.base_url = base_url + "/WebUntis" if not base_url.endswith("/WebUntis") else base_url
            self.username = username
            self.password = password

            self.session, self.jsessionid, self.schoolname, self.tenantid, self.token = apiLogin.login(self.base_url, username=username, password=password)

            self.jwt_claims = decode_jwt_unverified(self.token)
            self.jwt_token = self.token

            if not self.jsessionid:
                raise RuntimeError("No JSESSIONID received.")
        
        except Exception as e: 
            raise RuntimeError("Failed Login")


    def logout(self):
        apiLogin.logout(self.session, base_url=self.base_url)
        print("logout successful")


    def send_request(self, endpoint, params):
        """Sends a GET request to the specified endpoint with the provided parameters."""
        base_url = self.base_url

        print("Base URL:", base_url)
        print("Endpoint:", endpoint)
        url = f"{base_url}{endpoint}"
        print("URL:", url)

        headers = {
            "User-Agent": "user",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.token}",
            "Cookie": f"JSESSIONID={self.jsessionid}; schoolname={self.schoolname}",
        }
        response = requests.get(url, params=params, headers=headers)

        print("Status:", response.status_code)
        print("Response:", response.text)

        return response

if __name__ == "__main__":
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=7)
    s = session(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))
    s.send_request(endpoint="/WebUntis/api/homeworks/lessons", params={"startDate": start.strftime("%Y%m%d"), "endDate": end.strftime("%Y%m%d")})

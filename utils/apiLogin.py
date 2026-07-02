import requests
import os
from dotenv import load_dotenv


class WebUntisClient:
    def __init__(self, base_url: str):
        self.base_url = base_url + "/WebUntis"
        self.session = requests.Session()

        self.token: str | None = None
        self.jsessionid: str | None = None


    def login(self, username: str, password: str) -> None:
        self._fetch_cookies(username, password)
        self._fetch_token()


    def logout(self):
        response = self.session.get(
            f"{self.base_url}/saml/logout",
            timeout=15,
        )
        response.raise_for_status()
        print(response.text)
        

    def _fetch_cookies(self, username: str, password: str):
        response = self.session.post(
            f"{self.base_url}/j_spring_security_check",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "j_username": username,
                "j_password": password,
                "token": "",
            },
            timeout=15,
        )

        if response.status_code == 404:
            raise RuntimeError("School or server not found.")
        response.raise_for_status()

        if not self.session.cookies:
            raise RuntimeError("No cookies received.")
        
        self.jsessionid = self.session.cookies.get("JSESSIONID")
        return self.session.cookies.get_dict()


    def _fetch_token(self):
        response = self.session.get(
            f"{self.base_url}/api/token/new",
            timeout=15,
        )

        response.raise_for_status()
        token = response.text.strip()

        if "loginError" in token:
            raise RuntimeError("Invalid username or password.")

        if not token:
            raise RuntimeError("No bearer token received.")

        self.token = token
        return self.token



if __name__ == "__main__":
    load_dotenv()

    client = WebUntisClient(base_url=os.getenv("BASE_URL"))
    client.login(username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"),)

    print(f"{client.token = }")
    print(f"{client.jsessionid = }")
    print(f"{client.session.cookies.get_dict() = }")
    
    client.logout()

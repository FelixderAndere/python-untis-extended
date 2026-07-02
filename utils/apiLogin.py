import logging
import requests
import os
from dotenv import load_dotenv

log = logging.getLogger(__name__)


class WebUntisClient:
    def __init__(self, base_url: str):
        self.base_url = base_url + "/WebUntis"
        self.session = requests.Session()

        self.token: str | None = None
        self.user: dict | None = None


    def login(self, username: str, password: str) -> dict:
        log.info(
            "Logging in as %s in school %s on %s.webuntis.com",
            username,

        )

        self._fetch_cookies(username, password)
        self._fetch_token()

        self.user = self._fetch_user()

        log.info(
            "Logged in as %s (%s)",
            self.user["displayName"],
            self.user["username"],
        )

        return self.user


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

        log.info("Received %d cookies.", len(self.session.cookies))


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

        log.info("Received bearer token.")


    def _fetch_user(self) -> dict:
        response = self.session.get(
            f"{self.base_url}/api/rest/view/v1/app/data",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        if "user" not in data:
            raise RuntimeError("No user data returned.")

        user = data["user"]

        return {
            "id": user["person"]["id"],
            "username": user["name"],
            "displayName": user["person"]["displayName"],
            "imageUrl": user["person"].get("imageUrl"),
        }


if __name__ == "__main__":
    load_dotenv()

    client = WebUntisClient(base_url=os.getenv("BASE_URL"))
    user = client.login(username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"),)

    print(user)
    print(client.token)

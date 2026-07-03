import requests
from dotenv import load_dotenv
import os
import datetime
from utils import rpcLogin, apiLogin 
from utils.jwt import decode_jwt_unverified
import errors

load_dotenv()

class session():
    def __init__(self, base_url: str, username: str, password: str) -> None:
        if base_url.endswith("/WebUntis") or base_url.endswith("/WebUntis/"):
            self.base_url = base_url.rstrip("/")
        else:
            self.base_url = f"{base_url.rstrip('/')}/WebUntis"

        self.username = username
        self.password = password

        # Login attempts will now surface our clean Untis errors naturally
        self.session, self.jsessionid, self.schoolname, self.tenantid, self.token = apiLogin.login(
            self.base_url, username=username, password=password
        )

        if not self.jsessionid:
            raise errors.UntisAPIError("Login workflow finished but 'JSESSIONID' is missing from session cookies.")

        self.jwt_claims = decode_jwt_unverified(self.token)
        self.jwt_token = self.token


    def logout(self):
        success = apiLogin.logout(self.session, base_url=self.base_url)
        if success:
            print("Logout successful")
        else:
            print("Logout complete (Server didn't return expected redirect code)")


    def send_request(self, endpoint: str, params: dict) -> requests.Response:
        """Sends a GET request to the specified endpoint with the provided parameters."""
        # Ensure endpoint starts with a single slash and remove any duplicate /WebUntis strings
        clean_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        if clean_endpoint.startswith("/WebUntis"):
            clean_endpoint = clean_endpoint.replace("/WebUntis", "", 1)

        url = f"{self.base_url}{clean_endpoint}"

        headers = {
            "User-Agent": "user",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.token}",
            "Cookie": f"JSESSIONID={self.jsessionid}; schoolname={self.schoolname}",
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            
            if response.status_code in (401, 403):
                raise errors.UntisAuthError("Authentication token is invalid or expired.")
                
            response.raise_for_status()
            return response

        except requests.Timeout as e:
            raise errors.UntisTimeoutError(f"Request to {endpoint} timed out.") from e
        except requests.ConnectionError as e:
            raise errors.UntisConnectionError(f"Failed to connect to endpoint: {endpoint}.") from e
        except requests.HTTPError as e:
            raise errors.UntisAPIError(f"API endpoint returned HTTP status {e.response.status_code}: {e.response.text}") from e
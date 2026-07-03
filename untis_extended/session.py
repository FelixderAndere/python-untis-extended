import time
import threading
import requests
from dotenv import load_dotenv
import os
import datetime
from untis_extended.utils import apiLogin
from untis_extended.utils.jwt import decode_jwt_unverified
import errors as errors

load_dotenv()

class session():
    def __init__(self, base_url: str, username: str, password: str) -> None:
        if base_url.endswith("/WebUntis") or base_url.endswith("/WebUntis/"):
            self.base_url = base_url.rstrip("/")
        else:
            self.base_url = f"{base_url.rstrip('/')}/WebUntis"

        self.username = username
        self.password = password

        # central ratelimit to avoid Untis server problems
        self.max_requests = 1
        self.period = 60              
        self.tokens = float(self.max_requests)
        self.last_refill = time.time()
        self.rate_limit_lock = threading.Lock()

        # Login flow
        self.session, self.jsessionid, self.schoolname, self.tenantid, self.token = apiLogin.login(
            self.base_url, username=username, password=password
        )

        if not self.jsessionid:
            raise errors.UntisAPIError("Login workflow finished but 'JSESSIONID' is missing.")

        self.jwt_claims = decode_jwt_unverified(self.token)
        self.jwt_token = self.token


    def _apply_rate_limit(self):
            """Internal helper to manage token refills and delays dynamically and thread-safely."""
            while True:
                sleep_duration = 0
                
                with self.rate_limit_lock:
                    now = time.time()
                    elapsed = now - self.last_refill
                    
                    refill_amount = elapsed * (self.max_requests / self.period)
                    if refill_amount > 0:
                        self.tokens = min(self.max_requests, self.tokens + refill_amount)
                        self.last_refill = now

                    if self.tokens >= 1.0:
                        self.tokens -= 1.0
                        return

                    tokens_needed = 1.0 - self.tokens
                    sleep_duration = tokens_needed / (self.max_requests / self.period)
                    
                if sleep_duration > 0:
                    print(f"[Rate Limiter] Limit reached. Cooling down for {sleep_duration:.2f}s...")
                    time.sleep(sleep_duration)

    def logout(self):
        success = apiLogin.logout(self.session, base_url=self.base_url)
        if success:
            print("Logout successful")
        else:
            print("Logout complete (Server didn't return expected redirect code)")

    def send_request(self, endpoint: str, params: dict) -> requests.Response:
        """Sends a GET request to the specified endpoint with built-in rate limiting."""
        self._apply_rate_limit()

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
            
            # If the remote API explicitly flags an external 429 rate limit error
            if response.status_code == 429:
                raise errors.UntisAPIError("Exceeded remote Untis rate limit limits (HTTP 429).")
                
            if response.status_code in (401, 403):
                raise errors.UntisAuthError("Authentication token is invalid or expired.")
                
            response.raise_for_status()
            return response

        except requests.Timeout as e:
            raise errors.UntisTimeoutError(f"Request to {endpoint} timed out.") from e
        except requests.ConnectionError as e:
            raise errors.UntisConnectionError(f"Failed to connect to endpoint: {endpoint}.") from e
        except requests.HTTPError as e:
            raise errors.UntisAPIError(f"API endpoint returned status {e.response.status_code}") from e
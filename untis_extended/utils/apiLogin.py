import requests
import os
from dotenv import load_dotenv
import errors as errors

def _fetch_cookies(session: requests.Session, base_url: str, username: str, password: str) -> tuple:
    try:
        response = session.post(
            f"{base_url}/j_spring_security_check",
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
            raise errors.UntisAPIError("School or server not found (404). Check your base URL.")
        
        response.raise_for_status()

    except requests.Timeout as e:
        raise errors.UntisTimeoutError("Connection timed out while fetching cookies.") from e
    except requests.ConnectionError as e:
        raise errors.UntisConnectionError("Failed to connect to the Untis server while fetching cookies.") from e
    except requests.HTTPError as e:
        raise errors.UntisAPIError(f"HTTP Error during cookie fetch: {e.response.status_code}") from e

    if not session.cookies:
        raise errors.UntisDataError("Authentication seemingly succeeded, but no session cookies were received.")
    
    jsessionid = session.cookies.get("JSESSIONID")
    schoolname = session.cookies.get("schoolname")
    tenantid = session.cookies.get("Tenant-Id")

    return jsessionid, schoolname, tenantid


def _fetch_token(session: requests.Session, base_url: str):
    try:
        response = session.get(
            f"{base_url}/api/token/new",
            timeout=15,
        )
        response.raise_for_status()
        
    except requests.Timeout as e:
        raise errors.UntisTimeoutError("Connection timed out while retrieving API token.") from e
    except requests.ConnectionError as e:
        raise errors.UntisConnectionError("Failed to connect to the Untis server while retrieving API token.") from e
    except requests.HTTPError as e:
        raise errors.UntisAPIError(f"HTTP Error during token fetch: {e.response.status_code}") from e

    token = response.text.strip()

    if "loginError" in token:
        raise errors.UntisCredentialsError("Invalid username or password.")

    if not token:
        raise errors.UntisAuthError("Server response empty. No bearer token received.")

    return token


def login(base_url: str, username: str, password: str) -> tuple:
    session = requests.Session()
    jsessionid, schoolname, tenantid = _fetch_cookies(session=session, base_url=base_url, username=username, password=password)
    token = _fetch_token(session=session, base_url=base_url)
    return session, jsessionid, schoolname, tenantid, token


def logout(session: requests.Session, base_url: str) -> bool:
    try:
        response = session.get(
            f"{base_url}/saml/logout",
            allow_redirects=False,
            timeout=15,
        )
        response.raise_for_status()
        return response.status_code == 302  # Expecting a redirect after logout
    except (requests.Timeout, requests.ConnectionError):
        return False
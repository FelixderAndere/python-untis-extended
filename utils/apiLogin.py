import requests
import os
from dotenv import load_dotenv


def _fetch_cookies(session: requests.Session, base_url: str, username: str, password: str) -> tuple:
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
            raise RuntimeError("School or server not found.")
        response.raise_for_status()

        if not session.cookies:
            raise RuntimeError("No cookies received.")
        
        jsessionid = session.cookies.get("JSESSIONID")
        schoolname = session.cookies.get("schoolname")
        tenantid = session.cookies.get("Tenant-Id")

        return jsessionid, schoolname, tenantid


def _fetch_token(session: requests.Session, base_url: str):
        response = session.get(
            f"{base_url}/api/token/new",
            timeout=15,
        )

        response.raise_for_status()
        token = response.text.strip()

        if "loginError" in token:
            raise RuntimeError("Invalid username or password.")

        if not token:
            raise RuntimeError("No bearer token received.")

        token = token
        return token


def login(base_url: str, username: str, password: str) -> tuple:
    base_url = base_url
    session = requests.Session()
    jsessionid, schoolname, tenantid = _fetch_cookies(session=session, base_url=base_url, username=username, password=password)
    token = _fetch_token(session=session, base_url=base_url)
    return session, jsessionid, schoolname, tenantid, token


def logout(session: requests.Session, base_url: str) -> int:
    response = session.get(
        f"{base_url}/saml/logout",
        allow_redirects=False,
        timeout=15,
    )

    response.raise_for_status()
    return response.status_code == 302  # Expecting a redirect after logout
        


if __name__ == "__main__":
    load_dotenv()

    session, jsessionid, schoolname, tenantid, token = login(base_url=os.getenv("BASE_URL"), username=os.getenv("UNTIS_USERNAME"), password=os.getenv("UNTIS_PASSWORD"))

    print(f"{token = }")
    print(f"\n{jsessionid = }")
    print(f"\n{schoolname = }")
    print(f"\n{tenantid = }")
    print(f"\n{token = }")

    logout(session = session, base_url=os.getenv("BASE_URL"))

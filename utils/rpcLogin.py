import requests
from urllib import response

import requests
from dotenv import load_dotenv
import os

load_dotenv()


def login(self, base_url: str, username: str, password: str):
    payload = {
        "id": "1",
        "method": "authenticate",
        "jsonrpc": "2.0",
        "params": {
            "user": username,
            "password": password,
            "client": "pythonapp"
        }
    }

    response = requests.post(
        f"{base_url}/WebUntis/jsonrpc.do",
        json=payload,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    print("Login successful")
    print("Cookies:", response.cookies.get_dict())

    return data["result"]
import base64
import json

def decode_jwt_unverified(token: str) -> dict:
    payload = token.split(".")[1]

    payload += "=" * (-len(payload) % 4)

    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)
import time
from typing import Dict
import jwt

from app.utils import JWT_SECRET, JWT_ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str, is_admin: bool = False) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    if is_admin:
        payload["role"] = "admin"
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def verify_password(username: str, password: str):
    # Replace this function with a function that checks the username and password in your database
    return username == "user1" and password == "password1"

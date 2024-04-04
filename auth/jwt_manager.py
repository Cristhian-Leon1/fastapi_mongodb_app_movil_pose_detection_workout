import jwt
from fastapi import HTTPException
from jwt import encode, decode, InvalidTokenError
import os

key = os.environ["MY_KEY"]
algorithm = "HS256"


class Token:

    @staticmethod
    def create_token(data: dict):
        token: str = encode(payload=data, key=key, algorithm=algorithm)
        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            data: dict = decode(token, key=key, algorithms=[algorithm])
            email = data.get("access")
            return email
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

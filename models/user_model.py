from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    username: str
    password: str
    email: str
    full_name: str
    disabled: bool = None
    timestamp: datetime = None

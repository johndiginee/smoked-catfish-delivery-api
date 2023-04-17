from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    """schema to validate user sign up"""

    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "johndiginee",
                "email": "john@johndiginee.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    """JWT token"""
    authjwt_secret_key:str='61aecb11a05063d2879527805972305252a3b1135b78194ee46d1745a14a38bb'


class LoginModel(BaseModel):
    username:str
    password:str
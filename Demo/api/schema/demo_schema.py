# demo_schema.py
import re
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class DemoViewModel(BaseModel):
    id: int
    name: str
    phone_number: str
    company: Optional[str] = None
    email: str


class DemoCreationCommand(BaseModel):
    name: str
    phone_number: str
    company: Optional[str] = None
    email: EmailStr

    @field_validator("phone_number")
    def check_phone_number(cls, phone_number):
        phone_regex = re.compile(r'^(?:\+98|0)?9\d{9}$')  # "09********* or +98 912*******"
        if not phone_regex.match(phone_number):
            raise ValueError('Invalid phone number format')
        return phone_number

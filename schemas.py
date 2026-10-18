from pydantic import BaseModel, EmailStr, Field, ConfigDict
from models import UserRole
from typing import Annotated
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
import enum

Phone = Annotated[
    str,
    PhoneNumberValidator(default_region="TN", number_format="E164"),
]
import re


class ProjectCreate(BaseModel):
    name: str = Field(max_length=50)
    category_id: int


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category_id: int

class SignInRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    phone: Phone
    project: ProjectCreate
    password: str = Field(
        min_length=8,
        pattern=r"^(?:(?:[A-Za-z0-9]*[A-Z][A-Za-z0-9]*[^A-Za-z0-9].*)|(?:[A-Za-z0-9]*[^A-Za-z0-9].*[A-Z].*))$"
    )
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    phone: Phone
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
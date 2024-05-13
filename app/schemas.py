from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Query(BaseModel):
    query : str

class UserCreate(BaseModel):
    email: EmailStr
    password : str

class UserOut(BaseModel):
    id: int
    email : EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes=True

class UserLogin(BaseModel):
    email : EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class TranslationIn(BaseModel):
    text : str = Field(max_length=256)

class TranslationOut(BaseModel):
    text :str = Field(max_length=256)
    translation : str = Field(max_length=512)
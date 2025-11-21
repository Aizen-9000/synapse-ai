from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    is_premium: bool


class Config:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    message: str
    voice: Optional[bool] = False
    target_language: Optional[str] = None  # for translation
    search: Optional[bool] = False         # for web search
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserModel(BaseModel):
    id: Optional[str]
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_premium: bool = False
    created_at: Optional[datetime] = None


class ChatModel(BaseModel):
    id: Optional[str]
    user_id: str
    message: str
    reply: str
    created_at: Optional[datetime] = None

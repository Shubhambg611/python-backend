from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    companyName: str
    phoneNumber: str

class UserResponse(BaseModel):
    message: str
    userId: Optional[str] = None

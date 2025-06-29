from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "user"


class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str

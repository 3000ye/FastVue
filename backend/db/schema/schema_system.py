from typing import Optional
from pydantic import BaseModel


class AddUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    status: Optional[int] = 1


class UpdateUser(BaseModel):
    id: Optional[int]
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class DeleteUser(BaseModel):
    id: Optional[int]


class QueryUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = 1

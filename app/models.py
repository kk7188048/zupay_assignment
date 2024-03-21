from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    tags: Optional[List[str]] = []

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class Login(BaseModel):
    username: str
    password: str

class TagUpdate(BaseModel):
    tags: List[str]

class Blog(BaseModel):
    title: str
    content: str
    author: str 
    tags: Optional[List[str]] = [] 

class UpdateProfileData(BaseModel):
    name: Optional[str]
    password: Optional[str]

class DeleteBlogRequest(BaseModel):
    title: str
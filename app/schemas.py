from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# returns the specified information to user
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    first_name:str
    last_name:str
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    first_name:str
    last_name:str
    created_at: datetime
    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Define a Pydantic BaseModel for creating new blog posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
# Define a Pydantic BaseModel for returning blog post data to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id:int

    # This configures Pydantic to use ORM mode, which allows the Post object to be returned directly from the database
    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


# returns the specified information to user


# Define a Pydantic BaseModel for creating new users
class UserCreate(BaseModel):
    email: EmailStr
    # first_name: str
    # last_name: str
    password: str


# Define a Pydantic BaseModel for returning user data to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    # first_name: str
    # last_name: str
    created_at: datetime

    # This configures Pydantic to use ORM mode, which allows the User object to be returned directly from the database
    class Config:
        orm_mode = True


# Define a Pydantic BaseModel for logging in users
class UserLogin(BaseModel):
    email: str
    password: str


# Define a Pydantic BaseModel for representing a JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a Pydantic BaseModel for representing the data contained within a JWT token
class TokenData(BaseModel):
    id: Optional[str] = None

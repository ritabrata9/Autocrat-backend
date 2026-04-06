from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    email:EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True



class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime  
    user_id: int
    user: UserOut
    like_count: int

    # tells Pydantic to read data from SQLAlchemy model attributes
    # without this, Pydantic wouldn't know how to parse an ORM object
    class Config:
        from_attributes = True


class VoteResponse(BaseModel):
    user_id: int
    post_id: int

    class Config:
        form_attributes = True


    

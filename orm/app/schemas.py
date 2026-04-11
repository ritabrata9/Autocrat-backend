from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    
    # Tells Pydantic to read data from SQLAlchemy model attributes
    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime  
    user_id: int
    user: UserOut
    like_count: int

    model_config = ConfigDict(from_attributes=True)


class VoteResponse(BaseModel):
    user_id: int
    post_id: int

class CommentBase(BaseModel):
    content: str

class CommentIn(CommentBase):
    pass

class CommentOut(CommentBase):
    user_id: int
    post_id: int
    created_at: datetime
    user: UserOut

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, EmailStr,conint
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import relationship





class Vote(BaseModel):
    post_id:int
    dir:conint(le=1) # type: ignore

   

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True


class PostCreate(PostBase):
    pass

class UserPres(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class config:
        orm_mode = True

class Post(BaseModel):
    id:int
    own_id:int
    content:str
    owner: UserPres
    class config:
        orm_mode = True


class PostOut(BaseModel):
    Post:Post
    Votes: int
    class config:
        orm_mode = True
        


      

class UserCreate(BaseModel):
    email:EmailStr
    password: str


class Userlogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int







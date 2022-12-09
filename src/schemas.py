from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
	username:str
	email:str
	password:str

class SongItem(BaseModel):
    name : str
    artist : str

class Books(BaseModel):
    Id : int
    Book_Title : str 
    Book_Author : str
    Year_Of_Publication : int
    Publisher : str

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
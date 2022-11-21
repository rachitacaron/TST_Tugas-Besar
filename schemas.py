from pydantic import BaseModel


class User(BaseModel):
	username:str
	password:str
	email:str

class UserView(BaseModel):
	username: str
	email:str

	class Config:
		orm_mode = True
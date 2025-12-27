from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    firstname:str
    email:str
    lastname:str
    dob:str
    email:str
    password:str
    repeat_password:str
    phone:str
from pydantic import BaseModel,EmailStr
class UserBase(BaseModel):
    username:str
    email:EmailStr
class UserCreate(UserBase):
    password:str

class UserVerify(BaseModel):
    email:EmailStr
    password:str

class People(BaseModel):
    name:str
    age:int
    Mobile:int
    email:EmailStr
    gender:str
    

class del_data(BaseModel):
    ID:int
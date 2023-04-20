from pydantic import BaseModel, EmailStr
from datetime import datetime

class User_Create(BaseModel):
    username:str 
    email :EmailStr
    password: str 

class User_response(BaseModel):
    id :int 
    username:str 
    email:str  
    create_at:datetime
    class Config:
        orm_mode=True
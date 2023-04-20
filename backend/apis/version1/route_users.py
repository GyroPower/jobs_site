from typing import Annotated
from fastapi import APIRouter,Depends,Request
from backend.security.oauth2 import login_user 
from backend.schemas.User import User_Create,User_response
from backend.security.hashing import Hasher
from sqlalchemy.orm import Session 
from backend.db.database import get_db
from backend.db.models import users 
from backend.db.repository import users

users_router = APIRouter()

@users_router.get("/me/", response_model=User_response)
async def read_users_me(
    current_user: Annotated[User_Create, Depends(login_user.get_current_user)],
    
):  
    print(current_user)
    return current_user


@users_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User_Create, Depends(login_user.get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.email}]

@users_router.post("/register/",response_model=User_response)
async def create_user(
    user_created: User_Create,db: Annotated[Session,Depends(get_db)], 
    
):  
    user= users.create_new_user(user_created,db) 
    return user


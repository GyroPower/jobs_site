
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,status,APIRouter,Response,Request
from sqlalchemy.orm import Session 
from backend.db.database import get_db
from backend.db.models import users 
from backend.security.hashing import Hasher
from typing import Annotated
from backend.core.config import settings
from backend.security.oauth2 import login_user
auth_router = APIRouter()

@auth_router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    db:Annotated[Session,Depends(get_db)],
    response:Response
):
    
    user = db.query(users.User).filter(users.User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not Hasher.verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.acces_token_expire_minutes)
    access_token = login_user.create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    
    response.set_cookie(key="Authorization",value=access_token)
    return {"msg":"success"}


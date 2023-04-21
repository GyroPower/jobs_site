from datetime import datetime, timedelta

from ..db.models import users
from ..core.config import settings
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request
from ..db.database import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from ..schemas import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class login_user:
    @staticmethod
    def get_token(request: Request) -> oauth2_scheme:
        return request.cookies.get("Authorization")

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(get_token)],
        db: Annotated[Session, Depends(get_db)],
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            id: str = payload.get("user_id")
            if id is None:
                raise credentials_exception

            token_data = Token.TokenData(id=id)
        except JWTError:

            raise credentials_exception
        user = db.query(users.User).filter(users.User.id == token_data.id).first()
        if user is None:
            raise credentials_exception

        return user

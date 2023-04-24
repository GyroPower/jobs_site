from datetime import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..db.database import get_db
from ..db.models import users
from ..schemas import Token
from backend.apis.utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


class login_user:
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
        token: Annotated[str, Depends(oauth2_scheme)],
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

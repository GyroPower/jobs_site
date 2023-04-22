from sqlalchemy.orm import Session

from backend.db.models.users import User
from backend.schemas.User import User_Create
from backend.security.hashing import Hasher


def create_new_user(new_user: User_Create, db: Session):
    new_user.password = Hasher.get_password_hash(new_user.password)
    user = User(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

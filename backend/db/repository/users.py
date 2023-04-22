from sqlalchemy.orm import Session

from ...db.models.users import User
from ...schemas.User import User_Create
from ...security.hashing import Hasher


def create_new_user(new_user: User_Create, db: Session):
    new_user.password = Hasher.get_password_hash(new_user.password)
    user = User(
        username=new_user.username, email=new_user.email, password=new_user.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(a_email: str, db: Session):

    user = db.query(User).filter(User.email == a_email).first()

    return user

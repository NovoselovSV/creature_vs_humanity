from sqlalchemy.orm import Session
from sqlalchemy_utils import Password

from data.user import User, UserWriteSchema


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserWriteSchema) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy_utils import EmailType, PasswordType

from SQL_db.database import Base, engine


class User(Base):
    """ORM user model."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    email = Column(EmailType)
    is_admin = Column(Boolean)


class UserBaseSchema(BaseModel):
    """Base openAPI schema of user."""

    username: str
    email: str


class UserWriteSchema(UserBaseSchema):
    """OpenAPI schema of user to write."""

    password: str


class UserReadSchema(UserBaseSchema):
    """OpenAPI schema of user to read."""

    id: int

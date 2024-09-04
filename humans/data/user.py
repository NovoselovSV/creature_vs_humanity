from typing import List
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import EmailType, PasswordType

from SQL_db.database import Base, engine
import data


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

    hqs: Mapped[List['data.headquarter.Headquarter']] = relationship()

    def __str__(self):
        return f'{self.username}'


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

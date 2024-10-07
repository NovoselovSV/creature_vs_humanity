from typing import List

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import EmailType, PasswordType

import data
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
    is_admin = Column(Boolean, default=False)

    hqs: Mapped[List['data.headquarter.Headquarter']] = relationship()
    groups: Mapped[List['data.group.Group']] = relationship()
    units: Mapped[List['data.unit.Unit']] = relationship(lazy='select')

    def __str__(self):
        return f'{self.username}'

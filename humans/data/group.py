from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

import data
import settings
from SQL_db.database import Base
from web.shortcuts import get_redis_group_key


class Group(Base):
    """ORM group model."""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    director_id = Column(ForeignKey('users.id'))
    headquarter_id = Column(ForeignKey('headquarters.id', ondelete='RESTRICT'))

    director = relationship('User', back_populates='groups', lazy='select')
    headquarter = relationship(
        'Headquarter',
        back_populates='groups',
        lazy='select')

    members: Mapped[List['data.unit.Unit']] = relationship(lazy='selectin')

    @property
    def on_hq(self):
        return not get_redis_group_key(self.id)

    __table_args__ = (
        UniqueConstraint(
            'director_id',
            'name',
            name='director_id_group_name_unique_constraint'),
    )

    def __str__(self):
        return f'Group {self.name}'

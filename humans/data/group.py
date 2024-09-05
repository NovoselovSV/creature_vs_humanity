from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from SQL_db.database import Base
import data
from data.headquarter import HeadquarterReadSchema
from data.unit import UnitReadShortSchema


class Group(Base):
    """ORM group model."""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    director_id = Column(ForeignKey('users.id'))
    headquarter_id = Column(ForeignKey('headquarters.id', ondelete='RESTRICT'))

    director = relationship('User', back_populates='groups')
    headquarter = relationship('Headquarter', back_populates='groups')

    members: Mapped[List['data.unit.Unit']] = relationship()

    __table_args__ = (
        UniqueConstraint(
            'director_id',
            'name',
            name='director_id_group_name_unique_constraint'),
    )

    def __str__(self):
        return f'Group {self.name}'


class GroupReadShortSchema(BaseModel):
    """OpenAPI short schema of group to read."""

    id: int
    name: str
    headquarter: HeadquarterReadSchema


class GroupReadSchema(GroupReadShortSchema):
    """OpenAPI schema of group to read."""

    members: List[UnitReadShortSchema]


class GroupWriteSchema(BaseModel):
    """OpenAPI schema of group to write."""

    name: str
    headquarter_id: int

import hashlib
from typing import List

from pydantic import BaseModel, validator, Field
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from SQL_db.database import Base
import data
import settings
from data.headquarter import HeadquarterReadSchema
from data.shortcuts import get_bytes_from_stringed
from data.unit import UnitAttackResponseSchema, UnitAttackSchema, UnitReadShortSchema
from web.shortcuts import get_redis_group_key


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


class GroupReadShortSchema(BaseModel):
    """OpenAPI short schema of group to read."""

    id: int
    name: str
    on_hq: bool
    headquarter: HeadquarterReadSchema


class GroupReadSchema(GroupReadShortSchema):
    """OpenAPI schema of group to read."""

    members: List[UnitReadShortSchema]


class GroupWriteSchema(BaseModel):
    """OpenAPI schema of group to write."""

    name: str
    headquarter_id: int


class GroupBuilderSchema(BaseModel):
    """OpenAPI schema of group to build HQ."""

    group_id: int


class GroupChangeHQSchema(BaseModel):
    """OpenAPI schema of group to change HQ."""

    headquarter_id: int


class GroupAttackSchema(BaseModel):
    """OpenAPI schema of group to attack enemy."""

    members: List[UnitAttackSchema]
    signature: str = ''

    @validator('signature', always=True)
    def get_signature(cls, value, values):  # noqa
        hashed_attack = hashlib.sha256()
        for member in values.get('members', []):
            hashed_attack.update(
                get_bytes_from_stringed(member.id))
            hashed_attack.update(
                get_bytes_from_stringed(member.health))
            hashed_attack.update(
                get_bytes_from_stringed(member.attack))
        hashed_attack.update(get_bytes_from_stringed(settings.HUMANS_SALT))
        return hashed_attack.hexdigest()

    class Config:
        from_attributes = True


class GroupAttackResponseSchema(BaseModel):
    """OpenAPI schema of group to response about attack enemy."""

    members: List[UnitAttackResponseSchema]
    signature: str = Field(exclude=True)

    @validator('signature')
    def validate_signature(cls, value, values):  # noqa
        hashed_response = hashlib.sha256()
        for member in values.get('members', []):
            hashed_response.update(
                get_bytes_from_stringed(member.id))
            hashed_response.update(
                get_bytes_from_stringed(member.health))
            hashed_response.update(
                get_bytes_from_stringed(member.experience))
        hashed_response.update(get_bytes_from_stringed(settings.HUMANS_SALT))
        if value != hashed_response.hexdigest():
            raise ValueError('Signature not valid')
        return value


class GroupTargetSchema(BaseModel):
    """OpenAPI schema of groups target."""

    target_id: int

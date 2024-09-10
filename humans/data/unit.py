from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from SQL_db.database import Base
import settings


class Unit(Base):
    """ORM unit model."""

    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    director_id = Column(ForeignKey('users.id'))
    experience = Column(Integer, default=0)
    health = Column(Integer, default=settings.START_UNIT_HEALTH)
    attack = Column(Integer, default=settings.START_UNIT_ATTACK)
    group_id = Column(ForeignKey('groups.id', ondelete='RESTRICT'))

    director = relationship('User', back_populates='units')
    group = relationship('Group', back_populates='members')

    def __str__(self):
        return f'Soldier {self.id}'


class UnitReadShortSchema(BaseModel):
    """OpenAPI short schema of unit to read."""

    id: int
    experience: int
    health: int
    attack: int


class UnitReadSchema(UnitReadShortSchema):
    """OpenAPI schema of unit to read."""

    group_id: int


class UnitWriteSchema(BaseModel):
    """OpenAPI schema of unit to write."""

    group_id: int


class UnitChangeGroupSchema(BaseModel):
    """OpenAPI schema of unit to change group."""

    group_id: int


class UnitLevelUpSchema(BaseModel):
    """OpenAPI schema of unit to level up."""

    parametr_name: str = Field(pattern=r'^((attack)|(health))$')


class UnitAttackSchema(BaseModel):
    """OpenAPI schema of unit to attack enemy."""

    id: int
    attack: int
    health: int

    class Config:
        from_attributes = True


class UnitAttackResponseSchema(BaseModel):
    """OpenAPI schema of unit to response about attack enemy."""

    id: int
    health: int
    experience: int

from pydantic import BaseModel
from sqlalchemy import (Column, ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship

from SQL_db.database import Base
from data.region import RegionSchema


class Headquarter(Base):
    """ORM headquarter model."""

    __tablename__ = 'headquarters'

    id = Column(Integer, primary_key=True)
    director_id = Column(ForeignKey('users.id'))
    name = Column(String)
    recruitment_process = Column(Integer, default=0)
    region_id = Column(ForeignKey('regions.id'))

    director = relationship('User', back_populates='hqs')
    region = relationship('Region', back_populates='hqs')

    __table_args__ = (
        UniqueConstraint(
            'director_id',
            'name',
            name='director_id_name_unique_constraint'),
    )

    def __str__(self):
        return f'{self.name}'


class HeadquarterReadSchema(BaseModel):
    """OpenAPI schema of headquarter to read."""

    id: int
    name: str
    recruitment_process: int
    region: RegionSchema


class HeadquarterWriteSchema(BaseModel):
    """OpenAPI schema of headquarter to write."""

    name: str
    region_id: int

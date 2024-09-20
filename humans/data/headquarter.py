from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from SQL_db.database import Base
import data


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

    groups: Mapped[List['data.group.Group']] = relationship()

    __table_args__ = (
        UniqueConstraint(
            'director_id',
            'name',
            name='director_id_hq_name_unique_constraint'),
    )

    def __str__(self):
        return f'{self.name}'

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

import settings
from SQL_db.database import Base


class Unit(Base):
    """ORM unit model."""

    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    director_id = Column(ForeignKey('users.id'))
    experience = Column(Integer, default=0)
    health = Column(Integer, default=settings.START_UNIT_HEALTH)
    attack = Column(Integer, default=settings.START_UNIT_ATTACK)
    group_id = Column(ForeignKey('groups.id', ondelete='RESTRICT'))

    director = relationship('User', back_populates='units', lazy='select')
    group = relationship('Group', back_populates='members', lazy='select')

    def __str__(self):
        return f'Soldier {self.id}'

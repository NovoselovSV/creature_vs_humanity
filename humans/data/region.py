from typing import List

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

import data
from SQL_db.database import Base, engine


class Region(Base):
    """ORM region model."""

    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    attacker_attack_impact = Column(Integer, default=0)
    attacker_defense_impact = Column(Integer, default=0)
    defender_attack_impact = Column(Integer, default=0)
    defender_defense_impact = Column(Integer, default=0)

    hqs: Mapped[List['data.headquarter.Headquarter']] = relationship()

    def __str__(self):
        return f'{self.name}'

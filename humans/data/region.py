from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from SQL_db.database import Base, engine
import data


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


class RegionSchema(BaseModel):
    """OpenAPI schema of region to read."""

    id: int
    name: str
    description: str
    attacker_attack_impact: int
    attacker_defense_impact: int
    defender_attack_impact: int
    defender_defense_impact: int

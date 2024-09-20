from pydantic import BaseModel


class RegionSchema(BaseModel):
    """OpenAPI schema of region to read."""

    id: int
    name: str
    description: str
    attacker_attack_impact: int
    attacker_defense_impact: int
    defender_attack_impact: int
    defender_defense_impact: int

from pydantic import BaseModel


class EnemySchema(BaseModel):
    """OpenAPI schema of enemy."""

    name: str
    attack: int
    health: int
    defense: int
    signature: str


class EnemyResponseSchema(BaseModel):
    """OpenAPI schema to response about enemy."""

    health: int
    expirience: int
    signature: str

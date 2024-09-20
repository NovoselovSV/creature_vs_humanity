from pydantic import BaseModel, Field


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

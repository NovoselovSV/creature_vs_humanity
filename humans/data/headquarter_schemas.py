from pydantic import BaseModel

from .region_schemas import RegionSchema


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

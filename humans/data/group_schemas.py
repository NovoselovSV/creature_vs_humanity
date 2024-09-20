import hashlib

from pydantic import BaseModel, Field, validator

from . import unit_schemas
from .headquarter_schemas import HeadquarterReadSchema
from .shortcuts import get_bytes_from_stringed
import settings


class GroupReadShortSchema(BaseModel):
    """OpenAPI short schema of group to read."""

    id: int
    name: str
    on_hq: bool


class GroupReadSchema(GroupReadShortSchema):
    """OpenAPI schema of group to read."""

    headquarter: HeadquarterReadSchema
    members: list[unit_schemas.UnitReadShortSchema]


class GroupWriteSchema(BaseModel):
    """OpenAPI schema of group to write."""

    name: str
    headquarter_id: int


class GroupBuilderSchema(BaseModel):
    """OpenAPI schema of group to build HQ."""

    group_id: int


class GroupChangeHQSchema(BaseModel):
    """OpenAPI schema of group to change HQ."""

    headquarter_id: int


class GroupAttackSchema(BaseModel):
    """OpenAPI schema of group to attack enemy."""

    members: list[unit_schemas.UnitAttackSchema]
    signature: str = ''

    @validator('signature', always=True)
    def get_signature(cls, value, values):  # noqa
        hashed_attack = hashlib.sha256()
        for member in values.get('members', []):
            hashed_attack.update(
                get_bytes_from_stringed(member.id))
            hashed_attack.update(
                get_bytes_from_stringed(member.health))
            hashed_attack.update(
                get_bytes_from_stringed(member.attack))
        hashed_attack.update(get_bytes_from_stringed(settings.HUMANS_SALT))
        return hashed_attack.hexdigest()

    class Config:
        from_attributes = True


class GroupAttackResponseSchema(BaseModel):
    """OpenAPI schema of group to response about attack enemy."""

    members: list[unit_schemas.UnitAttackResponseSchema]
    signature: str = Field(exclude=True)

    @validator('signature')
    def validate_signature(cls, value, values):  # noqa
        hashed_response = hashlib.sha256()
        for member in values.get('members', []):
            hashed_response.update(
                get_bytes_from_stringed(member.id))
            hashed_response.update(
                get_bytes_from_stringed(member.health))
            hashed_response.update(
                get_bytes_from_stringed(member.experience))
        hashed_response.update(get_bytes_from_stringed(settings.HUMANS_SALT))
        if value != hashed_response.hexdigest():
            raise ValueError('Signature not valid')
        return value


class GroupTargetSchema(BaseModel):
    """OpenAPI schema of groups target."""

    target_id: int

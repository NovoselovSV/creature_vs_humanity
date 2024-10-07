import hashlib

from pydantic import BaseModel, validator

import settings
from data.shortcuts import get_bytes_from_stringed


class EnemySchema(BaseModel):
    """OpenAPI schema of enemy."""

    name: str
    attack: int
    health: int
    defense: int
    signature: str

    @validator('signature')
    def validate_signature(cls, value, values):  # noqa w805
        hashed_beast_parameters = hashlib.sha256()
        hashed_beast_parameters.update(
            get_bytes_from_stringed(
                values.get('name')))
        hashed_beast_parameters.update(
            get_bytes_from_stringed(
                values.get('health')))
        hashed_beast_parameters.update(
            get_bytes_from_stringed(
                values.get('attack')))
        hashed_beast_parameters.update(
            get_bytes_from_stringed(
                values.get('defense')))
        hashed_beast_parameters.update(
            get_bytes_from_stringed(
                settings.ENEMY_SALT))
        if value != hashed_beast_parameters.hexdigest():
            raise ValueError('Signature not valid')
        return value


class EnemyResponseSchema(BaseModel):
    """OpenAPI schema to response about enemy."""

    health: int
    experience: int
    signature: str = ''

    @validator('signature', always=True)
    def get_signature(cls, value, values):  # noqa w805
        hashed_response = hashlib.sha256()
        hashed_response.update(
            get_bytes_from_stringed(
                values.get('health', 0)))
        hashed_response.update(
            get_bytes_from_stringed(
                values.get('experience', 0)))
        hashed_response.update(get_bytes_from_stringed(settings.ENEMY_SALT))
        return hashed_response.hexdigest()

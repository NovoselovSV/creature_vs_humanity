import hashlib
from pydantic import BaseModel, validator

import settings


class EnemySchema(BaseModel):
    """OpenAPI schema of enemy."""

    name: str
    attack: int
    health: int
    defense: int
    signature: str

    @validator('signature')
    def get_signature(cls, value, values):  # noqa
        hashed_beast_parametrs = hashlib.sha256()
        hashed_beast_parametrs.update(
            bytes(str(values.get('name')), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(values.get('health')), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(values.get('attack')), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(values.get('defense')), encoding='utf-8'))
        hashed_beast_parametrs.update(
            bytes(str(settings.ENEMY_SALT), encoding='utf-8'))
        if value != hashed_beast_parametrs.hexdigest():
            raise ValueError('Signature not valid')
        return value


class EnemyResponseSchema(BaseModel):
    """OpenAPI schema to response about enemy."""

    health: int
    experience: int
    signature: str = ''

    @validator('signature', always=True)
    def get_signature(cls, value, values):  # noqa
        hashed_response = hashlib.sha256()
        hashed_response.update(
            bytes(str(values.get('health', 0)), encoding='utf-8'))
        hashed_response.update(
            bytes(str(values.get('experience', 0)), encoding='utf-8'))
        hashed_response.update(
            bytes(str(settings.ENEMY_SALT), encoding='utf-8'))
        return hashed_response.hexdigest()

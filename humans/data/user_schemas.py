from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    """Base openAPI schema of user."""

    username: str
    email: str


class UserWriteSchema(UserBaseSchema):
    """OpenAPI schema of user to write."""

    password: str


class UserReadSchema(UserBaseSchema):
    """OpenAPI schema of user to read."""

    id: int

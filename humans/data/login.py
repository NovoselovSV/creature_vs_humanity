from pydantic import BaseModel


class Token(BaseModel):
    """OpenAPI schema to output for login."""

    access_token: str
    token_type: str

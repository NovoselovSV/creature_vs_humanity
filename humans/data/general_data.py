from pydantic import BaseModel


class ErrorMessageSchema(BaseModel):
    """OpenAPI schema of error message."""

    detail: str

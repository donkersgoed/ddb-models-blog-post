from typing_extensions import Annotated, Optional
from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email, EmailNotValidError


class CreateEntityRequest(BaseModel):
    """Request model for creating an entity."""

    username: str = Field(min_length=5)
    password: str = Field(min_length=12)
    age: Optional[Annotated[int, Field(gt=0, lt=150, default=None)]] = None

    @field_validator("username")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value

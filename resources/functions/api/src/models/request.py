from typing_extensions import Annotated, Optional
from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email, EmailNotValidError

from . import UserRole


class CreateUserRequest(BaseModel):
    """Request model for creating a user."""

    username: str
    password: str = Field(min_length=12)
    age: Optional[Annotated[int, Field(gt=0, lt=150)]] = None
    role: UserRole

    @field_validator("username")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError as exc:
            raise ValueError("Invalid email format") from exc
        return value

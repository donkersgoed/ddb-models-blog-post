from typing_extensions import Annotated, Optional
from pydantic import BaseModel, Field

from .db_view import DatabaseViewUser
from . import UserRole


class CreateUserResponse(BaseModel):
    """Reponse model when creating a user."""

    id: str
    username: str
    age: Optional[Annotated[int, Field(gt=0, lt=150)]] = None
    role: UserRole

    @staticmethod
    def from_db_view_model(db_view_model: DatabaseViewUser) -> "CreateUserResponse":
        return CreateUserResponse(
            id=db_view_model.sk,
            username=db_view_model.username,
            age=db_view_model.age,
            role=db_view_model.role,
        )


class GetUserResponse(BaseModel):
    """Reponse model when getting a user."""

    id: str
    username: str
    age: Optional[Annotated[int, Field(gt=0, lt=150)]] = None
    role: UserRole

    @staticmethod
    def from_db_view_model(db_view_model: DatabaseViewUser) -> "GetUserResponse":
        return GetUserResponse(
            id=db_view_model.sk,
            username=db_view_model.username,
            age=db_view_model.age,
            role=db_view_model.role,
        )

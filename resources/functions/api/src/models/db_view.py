from copy import deepcopy
from typing_extensions import Optional
from pydantic import BaseModel, model_validator
from boto3.dynamodb.types import Binary, Decimal

from . import UserRole


class DatabaseViewUser(BaseModel):
    """Model representing the user being retrieved from the database."""

    pk: str
    sk: str

    username: str
    hashed_password: bytes

    age: Optional[int] = None

    role: UserRole

    # Timestamp in milliseconds
    created_at_ts_ms: int
    updated_at_ts_ms: int

    @model_validator(mode="before")
    @classmethod
    def convert_data_type_value(cls, values: dict):
        """Convert DynamoDB types to the correct Python types."""
        for key, value in values.items():
            if isinstance(value, Binary):
                values[key] = bytes(value)
            if isinstance(value, Decimal):
                values[key] = int(value)
        return values

    @staticmethod
    def from_dynamodb_item(item: dict) -> "DatabaseViewUser":
        """
        Convert a DynamoDB User item to a DatabaseViewUser object.

        Provide backward compatibility with older models, which might
        not have a "role" field stored in the database.
        """
        role = item.get("role", UserRole.READONLY)
        item_copy = deepcopy(item)
        item_copy["role"] = role
        return DatabaseViewUser(**item_copy)

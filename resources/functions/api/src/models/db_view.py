from typing_extensions import Optional
from pydantic import BaseModel, model_validator
from boto3.dynamodb.types import Binary, Decimal


class DatabaseViewUser(BaseModel):
    """Model representing the user being retrieved from the database."""

    pk: str
    sk: str

    username: str
    hashed_password: bytes

    age: Optional[int] = None

    # Timestamp in milliseconds
    created_at_ts_ms: int
    updated_at_ts_ms: int

    @model_validator(mode="before")
    @classmethod
    def convert_data_type_value(cls, values: dict):
        """Convert DynamoDB types to the correct Python types."""
        for key, value in values.items():
            if type(value) is Binary:
                values[key] = bytes(value)
            if type(value) is Decimal:
                values[key] = int(value)
        return values

    @staticmethod
    def from_dynamodb_item(item: dict) -> "DatabaseViewUser":
        """Convert a DynamoDB User item to a DatabaseViewUser object."""
        return DatabaseViewUser(**item)

from typing_extensions import Optional
from pydantic import BaseModel


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

from typing_extensions import Optional
from pydantic import BaseModel

from . import UserRole


class DatabaseCreateUser(BaseModel):
    """Model representing the user being stored in the database."""

    pk: str
    sk: str

    username: str
    hashed_password: bytes

    age: Optional[int] = None

    role: UserRole

    # Timestamp in milliseconds
    created_at_ts_ms: int
    updated_at_ts_ms: int

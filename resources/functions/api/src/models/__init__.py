from enum import Enum


class UserRole(str, Enum):
    """An enumeration of user roles."""

    READONLY = "READONLY"
    WRITER = "WRITER"
    ADMIN = "ADMIN"

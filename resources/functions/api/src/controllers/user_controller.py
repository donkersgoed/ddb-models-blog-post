# Standard library imports
import time
import uuid

# Related third party imports
import bcrypt
import boto3

# Local application / library specific imports
from ..models.request import CreateUserRequest
from ..models.db_create import DatabaseCreateUser
from ..models.db_view import DatabaseViewUser


class UserController:
    def __init__(self, ddb_table_name: str) -> None:
        self._ddb_table_name = ddb_table_name
        self._ddb_resource = boto3.resource("dynamodb")

        self._table = self._ddb_resource.Table(self._ddb_table_name)

    def create(self, create_request: CreateUserRequest) -> DatabaseViewUser:
        db_create_model = self._generate_create_model_from_request(create_request)
        self._table.put_item(Item=db_create_model.model_dump())
        return self._generate_view_model_from_create_model(db_create_model)

    def _generate_create_model_from_request(
        self, create_request: CreateUserRequest
    ) -> DatabaseCreateUser:
        """Generate a DatabaseCreateUser from a CreateUserRequest."""
        hashed_password = self._hash_password(create_request.password)

        # Generate a UTC timestamp in milliseconds
        ms_since_epoch = int(time.time() * 1000)

        return DatabaseCreateUser(
            pk="User",
            sk=str(self._generate_uuid()),
            username=create_request.username,
            hashed_password=hashed_password,
            age=create_request.age,
            created_at_ts_ms=ms_since_epoch,
            updated_at_ts_ms=ms_since_epoch,
        )

    def _generate_view_model_from_create_model(
        self, create_model: DatabaseCreateUser
    ) -> DatabaseViewUser:
        """Generate a DatabaseViewUser from a CreateUserRequest."""

        return DatabaseViewUser(**create_model.model_dump())

    @staticmethod
    def _generate_uuid() -> uuid.UUID:
        """Wrap the uuid generator in a function for easy mocking."""
        return uuid.uuid4()

    @staticmethod
    def _hash_password(password: str) -> bytes:
        # Convert the password to bytes
        password_bytes = password.encode("utf-8")

        # Generate a salt
        salt = bcrypt.gensalt()

        # Hash the password and return it
        return bcrypt.hashpw(password_bytes, salt)

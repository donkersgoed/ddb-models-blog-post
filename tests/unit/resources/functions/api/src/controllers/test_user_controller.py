# Standard library imports
import uuid
from unittest.mock import MagicMock

# Related third party imports
import freezegun

# Local application / library specific imports
from resources.functions.api.src.models.request import CreateUserRequest


class TestUserController:
    """Test class for UserController."""

    @staticmethod
    def test_generate_create_model_from_request_happy():
        # 1. ARRANGE
        from resources.functions.api.src.controllers.user_controller import (
            UserController,
        )

        create_user_request = CreateUserRequest(
            username="test@mydomain.com",
            password="p1234p1234p1234",
            age=30,
            role="WRITER",
        )
        controller = UserController(ddb_table_name="mock_table_name")

        mock_hashed_password = (
            b"$2b$12$ZqrqlJbq5GVfWTTpsz95zu0VcGfk63i7XjfuF9cS24HDDvABzi1TO"
        )
        controller._hash_password = MagicMock(return_value=mock_hashed_password)

        # 2. ACT
        model = controller._generate_create_model_from_request(create_user_request)

        # 3. ASSERT
        assert model.username == "test@mydomain.com"
        assert model.hashed_password == mock_hashed_password
        assert model.age == 30

    @staticmethod
    @freezegun.freeze_time("2022-01-01T00:00:00Z")
    def test_generate_create_happy():
        # 1. ARRANGE
        from resources.functions.api.src.controllers.user_controller import (
            UserController,
        )

        create_user_request = CreateUserRequest(
            username="test@mydomain.com",
            password="p1234p1234p1234",
            age=30,
            role="WRITER",
        )
        controller = UserController(ddb_table_name="mock_table_name")

        # Mock Bcrypt
        mock_hashed_password = (
            b"$2b$12$ZqrqlJbq5GVfWTTpsz95zu0VcGfk63i7XjfuF9cS24HDDvABzi1TO"
        )
        controller._hash_password = MagicMock(return_value=mock_hashed_password)

        # Mock DDB
        controller._table.put_item = MagicMock(return_value=None)

        # Mock UUIDgen
        controller._generate_uuid = MagicMock(
            return_value=uuid.UUID("673fd197-0de3-4bbb-b2df-6ee127e9208c")
        )

        # 2. ACT
        controller.create(create_user_request)

        # 3. ASSERT

        controller._table.put_item.assert_called_once_with(
            Item={
                "pk": "User",
                "sk": "673fd197-0de3-4bbb-b2df-6ee127e9208c",
                "username": "test@mydomain.com",
                "hashed_password": b"$2b$12$ZqrqlJbq5GVfWTTpsz95zu0VcGfk63i7XjfuF9cS24HDDvABzi1TO",
                "role": "WRITER",
                "age": 30,
                "created_at_ts_ms": 1640995200000,
                "updated_at_ts_ms": 1640995200000,
            }
        )

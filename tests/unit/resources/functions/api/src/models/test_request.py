import pytest
from pydantic_core import ValidationError


class TestCreateUserRequest:
    """Test class for CreateUserRequest."""

    @staticmethod
    def test_create_entity_request_happy():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import (
            CreateUserRequest,
        )

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
            "role": "WRITER",
        }

        # 2. ACT
        model = CreateUserRequest(**request_payload)

        # 3. ASSERT
        assert model.username == "test@mydomain.com"
        assert model.password == "p1234p1234p1234"
        assert model.age is None
        assert model.role == "WRITER"

    @staticmethod
    def test_create_entity_request_happy_with_age():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import (
            CreateUserRequest,
        )

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
            "age": 30,
            "role": "WRITER",
        }

        # 2. ACT
        model = CreateUserRequest(**request_payload)

        # 3. ASSERT
        assert model.username == "test@mydomain.com"
        assert model.password == "p1234p1234p1234"
        assert model.age == 30
        assert model.role == "WRITER"

    @staticmethod
    def test_create_entity_request_happy_with_extraneous_fields():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import (
            CreateUserRequest,
        )

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
            "age": 30,
            "role": "WRITER",
            "some_int": 12,
            "some_bool": False,
            "some_str": "lorem ipsum",
        }

        # 2. ACT
        model = CreateUserRequest(**request_payload)

        # 3. ASSERT
        assert model.username == "test@mydomain.com"
        assert model.password == "p1234p1234p1234"
        assert model.age == 30
        assert model.role == "WRITER"

    @staticmethod
    def test_create_entity_request_unhappy_invalid_email():
        """
        Validate that a CreateUserRequest with an invalid username raises an error.

        This test contains an example payload as provided through a REST API call.
        The payload contains all required fields, but the username contains a value
        which is not a valid email address. We expect creating an CreateUserRequest
        object with this payload raises a ValidationError.
        """
        # 1. ARRANGE
        from resources.functions.api.src.models.request import (
            CreateUserRequest,
        )

        request_payload = {
            "username": "test_user",
            "password": "p1234p1234p1234",
            "age": 30,
            "role": "ADMIN",
        }

        # 2. ACT
        with pytest.raises(ValidationError) as exc:
            CreateUserRequest(**request_payload)

        # 3. ASSERT
        errors = exc.value.errors()
        assert len(errors) == 1

        error = errors[0]
        assert error["type"] == "value_error"
        assert error["loc"] == ("username",)
        assert error["msg"] == "Value error, Invalid email format"

    @staticmethod
    def test_create_entity_request_unhappy_invalid_role():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import (
            CreateUserRequest,
        )

        request_payload = {
            "username": "test_user@mydomain.com",
            "password": "p1234p1234p1234",
            "age": 30,
            "role": "DOESNOTEXIST",
        }

        # 2. ACT
        with pytest.raises(ValidationError) as exc:
            CreateUserRequest(**request_payload)

        # 3. ASSERT
        errors = exc.value.errors()
        assert len(errors) == 1

        error = errors[0]
        assert error["type"] == "enum"
        assert error["loc"] == ("role",)
        assert error["msg"] == "Input should be 'READONLY', 'WRITER' or 'ADMIN'"

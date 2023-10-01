import pytest
from pydantic_core import ValidationError
from boto3.dynamodb.types import Binary, Decimal


class TestDatabaseViewUser:
    """Test class for DatabaseViewUser."""

    @staticmethod
    def test_create_entity_request_happy_v1():
        # 1. ARRANGE
        from resources.functions.api.src.models.db_view import (
            DatabaseViewUser,
        )

        dynamodb_response = {
            "Items": [
                {
                    "hashed_password": Binary(
                        b"$2b$12$yowVgWrjapGmpjVGRsMO/OyZPlrbXnyGJ23.CT3Y3.O.jlIy616NS"
                    ),
                    "created_at_ts_ms": Decimal("1696109591643"),
                    "sk": "070e7fd4-128c-486d-8ab2-09277253f2ee",
                    "username": "lucvandonkersgoed@mydomain.com",
                    "updated_at_ts_ms": Decimal("1696109591643"),
                    "pk": "User",
                    "age": None,
                },
            ],
            "Count": 1,
            "ScannedCount": 1,
            "ResponseMetadata": {
                # Redacted
            },
        }

        item = dynamodb_response["Items"][0]

        # 2. ACT
        model = DatabaseViewUser.from_dynamodb_item(item)

        # 3. ASSERT
        assert model.pk == "User"
        assert model.sk == "070e7fd4-128c-486d-8ab2-09277253f2ee"
        assert model.username == "lucvandonkersgoed@mydomain.com"
        assert (
            model.hashed_password
            == b"$2b$12$yowVgWrjapGmpjVGRsMO/OyZPlrbXnyGJ23.CT3Y3.O.jlIy616NS"
        )
        assert model.age is None
        assert model.created_at_ts_ms == 1696109591643
        assert model.updated_at_ts_ms == 1696109591643

    @staticmethod
    def test_create_entity_request_happy_v1_with_age():
        # 1. ARRANGE
        from resources.functions.api.src.models.db_view import (
            DatabaseViewUser,
        )

        dynamodb_response = {
            "Items": [
                {
                    "hashed_password": Binary(
                        b"$2b$12$U4S.pfOnMACczq2JH2MXnOrXUYL6k7autjeqLiJQQfs0OtT7Y9n5u"
                    ),
                    "created_at_ts_ms": Decimal("1696110403861"),
                    "sk": "b706a5de-3291-4bbe-8eba-b2c6bd64a729",
                    "username": "lucvandonkersgoed@mydomain.com",
                    "updated_at_ts_ms": Decimal("1696110403861"),
                    "pk": "User",
                    "age": 38,
                },
            ],
            "Count": 1,
            "ScannedCount": 1,
            "ResponseMetadata": {
                # Redacted
            },
        }

        item = dynamodb_response["Items"][0]

        # 2. ACT
        model = DatabaseViewUser.from_dynamodb_item(item)

        # 3. ASSERT
        assert model.pk == "User"
        assert model.sk == "b706a5de-3291-4bbe-8eba-b2c6bd64a729"
        assert model.username == "lucvandonkersgoed@mydomain.com"
        assert (
            model.hashed_password
            == b"$2b$12$U4S.pfOnMACczq2JH2MXnOrXUYL6k7autjeqLiJQQfs0OtT7Y9n5u"
        )
        assert model.age == 38
        assert model.created_at_ts_ms == 1696110403861
        assert model.updated_at_ts_ms == 1696110403861

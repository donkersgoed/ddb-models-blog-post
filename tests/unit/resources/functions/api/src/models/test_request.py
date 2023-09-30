class TestCreateEntityRequest:
    """Test class for CreateEntityRequest."""

    @staticmethod
    def test_create_entity_request_happy():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import CreateEntityRequest

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
        }

        # 2. ACT
        model = CreateEntityRequest(**request_payload)

        # 3. ASSERT
        assert model.username == request_payload["username"]
        assert model.password == request_payload["password"]
        assert model.age is None

    @staticmethod
    def test_create_entity_request_happy_with_age():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import CreateEntityRequest

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
            "age": 30,
        }

        # 2. ACT
        model = CreateEntityRequest(**request_payload)

        # 3. ASSERT
        assert model.username == request_payload["username"]
        assert model.password == request_payload["password"]
        assert model.age == request_payload["age"]

    @staticmethod
    def test_create_entity_request_happy_with_extraneous_fields():
        # 1. ARRANGE
        from resources.functions.api.src.models.request import CreateEntityRequest

        request_payload = {
            "username": "test@mydomain.com",
            "password": "p1234p1234p1234",
            "age": 30,
            "some_int": 12,
            "some_bool": False,
            "some_str": "lorem ipsum",
        }

        # 2. ACT
        model = CreateEntityRequest(**request_payload)

        # 3. ASSERT
        assert model.username == request_payload["username"]
        assert model.password == request_payload["password"]
        assert model.age == request_payload["age"]

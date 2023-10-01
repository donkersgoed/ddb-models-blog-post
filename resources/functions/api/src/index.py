# Standard library imports
import json
import os

# Related third party imports
from pydantic import ValidationError

# Local application / library specific imports
from .controllers.user_controller import UserController
from .models.request import CreateUserRequest
from .models.response import CreateUserResponse, GetUserResponse

DDB_TABLE_NAME = os.environ["DDB_TABLE_NAME"]

user_controller = UserController(ddb_table_name=DDB_TABLE_NAME)


def create_function_handler(event, _context):
    try:
        create_user_request = CreateUserRequest(**json.loads(event["body"]))
    except ValidationError as exc:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "Invalid request body", "errors": json.loads(exc.json())}
            ),
        }

    db_view_model = user_controller.create(create_user_request)
    response_model = CreateUserResponse.from_db_view_model(db_view_model)

    return {"statusCode": 200, "body": response_model.model_dump_json()}


def get_function_handler(_event, _context):
    # Get all users as a list of DatabaseViewUser objects
    db_view_models = user_controller.get_all()
    # Convert each DatabaseViewUser to a GetUserResponse object.
    users_response = [
        GetUserResponse.from_db_view_model(db_view_model).model_dump()
        for db_view_model in db_view_models
    ]

    return {
        "statusCode": 200,
        "body": json.dumps(
            users_response  # Convert the list of GetUserResponse objects to a JSON string
        ),
    }

import json


def create_function_handler(event, _context):
    print(json.dumps(event))
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


def get_function_handler(event, _context):
    print(json.dumps(event))
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}

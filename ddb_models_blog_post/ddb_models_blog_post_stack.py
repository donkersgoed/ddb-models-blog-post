from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
)
from constructs import Construct


class DdbModelsBlogPostStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            scope=self,
            id="Table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
        )

        layer = lambda_.LayerVersion(
            scope=self,
            id="ApiLayer",
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_3_11,
            ],
            code=lambda_.Code.from_asset("resources/layers/api/python.zip"),
        )

        create_function = lambda_.Function(
            scope=self,
            id="CreateFunction",
            architecture=lambda_.Architecture.X86_64,
            runtime=lambda_.Runtime.PYTHON_3_11,
            code=lambda_.Code.from_asset("resources/functions/api"),
            timeout=Duration.seconds(5),
            memory_size=2048,
            layers=[layer],
            handler="src.index.create_function_handler",
            environment={"DDB_TABLE_NAME": table.table_name},
        )
        table.grant_write_data(create_function)

        get_function = lambda_.Function(
            scope=self,
            id="GetFunction",
            architecture=lambda_.Architecture.X86_64,
            runtime=lambda_.Runtime.PYTHON_3_11,
            code=lambda_.Code.from_asset("resources/functions/api"),
            timeout=Duration.seconds(5),
            memory_size=2048,
            layers=[layer],
            handler="src.index.get_function_handler",
            environment={"DDB_TABLE_NAME": table.table_name},
        )
        table.grant_read_data(get_function)

        rest_api = apigateway.RestApi(
            scope=self,
            id="RestApi",
        )
        users_resource = rest_api.root.add_resource("users")
        users_resource.add_method(
            "POST", integration=apigateway.LambdaIntegration(create_function)
        )
        users_resource.add_method(
            "GET", integration=apigateway.LambdaIntegration(get_function)
        )

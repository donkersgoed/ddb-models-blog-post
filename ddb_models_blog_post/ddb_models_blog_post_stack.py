from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
)
from constructs import Construct


class DdbModelsBlogPostStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        create_function = lambda_.Function(
            scope=self,
            id="CreateFunction",
            architecture=lambda_.Architecture.X86_64,
            code=lambda_.Code.from_asset("resources/functions/api"),
            handler="src.index.create_function_handler",
        )

        get_function = lambda_.Function(
            scope=self,
            id="GetFunction",
            architecture=lambda_.Architecture.X86_64,
            code=lambda_.Code.from_asset("resources/functions/api"),
            handler="src.index.get_function_handler",
        )

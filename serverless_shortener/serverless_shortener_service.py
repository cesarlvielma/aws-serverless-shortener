from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_dynamodb as dynamodb
)


class WidgetService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        table = dynamodb.Table(
            self, "Table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
          )

        lambda_env = dict(
            DYNAMODB_TABLE_NAME=table.table_name,
            ID_LENGTH='7'
        )

        short_url_lambda = lambda_.Function(
            self, "ShortUrlLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("resources"),
            handler="lambda.short_url",
            environment=lambda_env)

        read_url_lambda = lambda_.Function(
            self, "ReadUrlLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("resources"),
            handler="lambda.read_url",
            environment=lambda_env)

        table.grant_read_write_data(short_url_lambda)
        table.grant_read_write_data(read_url_lambda)

        api = apigateway.RestApi(self, "widgets-api",
                                 rest_api_name="Serverless Shortener Service",
                                 description="This Service Shorts URL using Lambda + DynamoDb Serverless config.")

        request_templates = {"application/json": '{ "statusCode": "200" }'}

        api.root.add_method("POST", apigateway.LambdaIntegration(short_url_lambda, request_templates=request_templates))

        read_resource = api.root.add_resource('{randId}')
        read_resource.add_method("GET", apigateway.LambdaIntegration(read_url_lambda, request_templates=request_templates))


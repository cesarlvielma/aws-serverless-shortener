from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from . import serverless_shortener_service


class ServerlessShortenerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        serverless_shortener_service.WidgetService(self, "Widgets")

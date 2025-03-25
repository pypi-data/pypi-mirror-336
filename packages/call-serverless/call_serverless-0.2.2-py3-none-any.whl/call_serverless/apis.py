import json
from typing import Union

import boto3
import botocore
import botocore.exceptions

from .exceptions import LambdaAccessError
from .formatter import format_request
from .response import CLResponse

_clients = {}


def _get_lambda_client(region: str):
    global _client

    if region not in _clients:
        _clients[region] = boto3.client("lambda", region_name=region)
    return _clients[region]


def call_lambda(
    lambda_arn: str,
    path: str,
    method: str = "GET",
    stage: str = "prod",
    region: str = "us-east-1",
    headers: Union[dict, None] = None,
    path_params: Union[dict, None] = None,
    query_params: Union[dict, None] = None,
    body: Union[dict, None] = None,
) -> CLResponse:
    """
    Invokes an AWS Lambda function by sending an HTTP-like request with the specified method, path,
    and headers.

    Args:
        lambda_arn (str): The Amazon Resource Name (ARN) of the Lambda function to invoke.
        path (str): The API Gateway path to invoke on the Lambda function (e.g., `/users/{id}`,
            `/items`). It must be exactly how it is defined in the app.
        method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            Defaults to 'GET'.
        stage (str): The deployment stage of the API (e.g., 'dev', 'prod'). Defaults to 'prod'.
        region (str): The AWS region where the Lambda function is hosted. Defaults to 'us-east-1'.
        headers (Union[dict, None], optional): Additional headers to send in the request.
            Defaults to None.
        path_params (Union[dict, None], optional): Path parameters to send in the request.
            Defaults to None.
        query_params (Union[dict, None], optional): Query parameters to send in the request.
            Defaults to None.
        body (Union[dict, None], optional): The request body to send in the Lambda invocation.
            Defaults to None.

    Returns:
        CLResponse: A response object containing status code and body from the Lambda function.

    Raises:
        botocore.exceptions.ClientError: If there is an error in the Lambda client during invocation.
        LambdaAccessError: If there are issues accessing or executing the Lambda function.

    Example:
        >>> response = call_lambda(
                lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:MyFunction",
                path="/users",
                method="POST",
                stage="prod",
                region="us-west-2",
                body={"username": "new_user"},
                headers={"Authorization": "Bearer token123"}
            )
        >>> print(response)
        <CLResponse 200>

    This function formats a request payload and uses the AWS SDK to invoke a Lambda function via
    its ARN. It simulates an API Gateway request to the Lambda, including HTTP methods and headers,
    and returns a CLResponse object with the parsed response.
    """

    payload = format_request(
        path=path,
        method=method,
        stage=stage,
        headers=headers,
        path_params=path_params,
        query_params=query_params,
        body=body,
    )
    client = _get_lambda_client(region)
    try:
        response = client.invoke(
            FunctionName=lambda_arn,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
    except botocore.exceptions.ClientError as exc:
        raise LambdaAccessError(f"Issue with the lambda execution: {str(exc)}") from exc

    response_str = response["Payload"].read().decode("utf-8")
    return CLResponse.from_response(response_str)

import json
import os
from typing import Union


def base_template():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            ("template.json"),
        ),
        "r",
    ) as file:
        request = json.load(file)
    return request


def get_full_path(
    path: str,
    path_params: Union[dict, None] = None,
) -> str:

    if path_params:
        path = path.format(**path_params)
    return path


def format_request(
    path: str,
    method: str,
    stage: str,
    headers: Union[dict, None] = None,
    path_params: Union[dict, None] = None,
    query_params: Union[dict, None] = None,
    body: Union[dict, None] = None,
):
    """
    @param headers: dict
    @param path: str - the path of the resource and it starts with a forward slash
    """
    if not path.startswith("/"):
        path = f"/{path}"

    request_format = base_template()
    request_format["resource"] = path
    request_format["path"] = get_full_path(path, path_params)
    request_format["headers"] = headers
    request_format["body"] = body
    request_format["httpMethod"] = method
    request_format["queryStringParameters"] = query_params
    if query_params:
        request_format["multiValueQueryStringParameters"] = {
            k: [v] for k, v in query_params.items()
        }
    request_format["pathParameters"] = path_params

    request_format["requestContext"]["path"] = f"/{stage}{path}"
    request_format["requestContext"]["resourcePath"] = path
    request_format["requestContext"]["stage"] = stage
    request_format["stageVariables"] = None

    return request_format

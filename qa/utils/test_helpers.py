import json
import allure
from qa.models.api.common_models import ErrorResponse
from jsonschema import validate, ValidationError


def attach_api_data(request_payload, response):
    method = response.request.method
    url = response.request.url

    request_headers = "\n".join(
        f"{k}: {v}" for k, v in response.request.headers.items()
    )

    try:
        request_body = json.dumps(request_payload, indent=2)
    except Exception:
        request_body = str(request_payload)

    request_text = f"{method} {url}\n\nHeaders:\n{request_headers}\n\nBody:\n{request_body}".strip()

    try:
        response_body = json.dumps(response.json(), indent=2)
    except Exception:
        response_body = response.text

    response_headers = "\n".join(f"{k}: {v}" for k, v in response.headers.items())

    response_text = f"Status: {response.status_code}\n\nHeaders:\n{response_headers}\n\nBody:\n{response_body}".strip()

    allure.attach(
        request_text, name="request", attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        response_text, name="response", attachment_type=allure.attachment_type.TEXT
    )


def assert_error_response(actual: ErrorResponse, expected: dict):
    for key, value in expected.items():
        actual_value = getattr(actual, key)
        assert actual_value == value, f"{key}: expected {value}, got {actual_value}"

def set_report_parameters(test_params: dict):
    if hasattr(test_params, "model_dump"):
        test_params = test_params.model_dump()

    if hasattr(test_params, "items"):
        for k, v in test_params.items():
            allure.dynamic.parameter(
                name=k,
                value=v.model_dump() if hasattr(v, "model_dump") else v,
                excluded=True
            )



def validate_response(response_json: dict, schema: dict) -> None:
    """
    Validates API response against a JSON schema.

    Raises:
        AssertionError: if validation fails
    """
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")

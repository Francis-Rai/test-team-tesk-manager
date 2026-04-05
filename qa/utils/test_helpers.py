import functools
import json
import allure
from jsonschema import validate, ValidationError
from qa.models.api.common_models import ErrorResponse
from qa.config.settings import (
    ERROR_TAG,
    SUCCESS_TAG,
    SUPER_USER_EMAIL,
    SUPER_USER_PASSWORD,
)
from qa.config.enums import UserRole
from qa.utils.common import generate_email, generate_password

def _mask_sensitive_fields(obj):
    """Recursively mask sensitive fields in a dict or list."""
    keys_to_mask_full = ["password"]
    keys_to_truncate = ["token", "authorization"]

    if isinstance(obj, dict):
        masked_dict = {}
        for k, v in obj.items():
            lk = k.lower()
            if lk in keys_to_mask_full:
                masked_dict[k] = "****"
            elif lk in keys_to_truncate and isinstance(v, str):
                # truncate: first 6 chars + ... + last 6 chars
                if len(v) > 12:
                    masked_dict[k] = f"{v[:12]}...{v[-6:]}"
                else:
                    masked_dict[k] = v  # short token, keep as-is
            else:
                masked_dict[k] = v
        return masked_dict

    elif isinstance(obj, list):
        return [_mask_sensitive_fields(item) for item in obj]

    else:
        return obj

def attach_api_data(request_payload, response):
    method = response.request.method
    url = response.request.url

    request_headers = "\n".join(
        f"{k}: {v}" for k, v in _mask_sensitive_fields(dict(response.request.headers)).items()
    )

    request_payload = _mask_sensitive_fields(request_payload)
    try:
        request_body = json.dumps(request_payload, indent=2)
    except Exception:
        request_body = str(request_payload)

    request_text = f"{method} {url}\n\nHeaders:\n{request_headers}\n\nBody:\n{request_body}".strip()

    try:
        response_body = json.dumps(_mask_sensitive_fields(response.json()), indent=2)
    except Exception:
        response_body = response.text

    response_headers = "\n".join(
        f"{k}: {v}" for k, v in _mask_sensitive_fields(dict(response.headers)).items()
    )

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

    test_params = _mask_sensitive_fields(test_params)
    if hasattr(test_params, "items"):
        for k, v in test_params.items():
            allure.dynamic.parameter(
                name=k,
                value=v.model_dump() if hasattr(v, "model_dump") else v,
                excluded=True
            )

def set_allure_metadata(func):
    """
    param_metadata: dict mapping test args tuple -> metadata dict
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the test_data parameter from args/kwargs
        test_param = kwargs.get("test_data")

        if test_param:
            # Set title
            if title := test_param.get("description"):
                allure.dynamic.title(title)

            # Set severity
            if severity := test_param.get("severity"):
                allure.dynamic.severity(severity)

            # set success/error tag
            tag = ERROR_TAG if "response" in test_param else SUCCESS_TAG
            allure.dynamic.tag(tag)

            # set report parameters
            set_report_parameters(test_param.get("request", {}))

        return func(*args, **kwargs)
    return wrapper


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


def create_user_via_api(api_client, role=UserRole.USER):
    test_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": generate_email(),
        "password": generate_password(),
    }
    response = api_client.register(test_user, attach=False)

    assert response.status_code == 200, (
        f"Registration failed. "
        f"Status: {response.status_code}, "
        f"Body: {response.text}"
    )
    register_json = response.json()

    if role != UserRole.USER:
        # Login as super admin
        super_admin_creds = {
            "email": SUPER_USER_EMAIL,
            "password": SUPER_USER_PASSWORD
        }
        response = api_client.login(super_admin_creds, attach=False)
        assert (
            response.status_code == 200
        ), f"Super admin login failed: {response.text}"
        headers = {"Authorization": f"Bearer {response.json()['token']}"}

        # Change registered user role
        response = api_client.change_user_role(
            env=None,
            headers=headers,
            user_id=register_json["user"]["userId"],
            request_body={"role": role.value},
            attach=False,
        )
        assert response.status_code == 204, f"Role change failed: {response.text}"

        # check role was updated with get api
        get_response = api_client.get_all_users(
            env=None,
            headers=headers,
            attach=False,
        )
        assert get_response.status_code == 200, "Unable to get users"
        user = next(
            u
            for u in get_response.json()
            if u["id"] == register_json["user"]["userId"]
        )
        # update id key id to userId
        user["userId"] = user.pop("id")
        register_json.update({"user": user})

    register_json["user"].update({"password": test_user["password"]})
    return register_json

import pytest
import allure
from qa.tests.api.test_data.get_all_users_params import success_cases, error_cases
from qa.tests.api.schema.user_schema import GET_ALL_USERS_SCHEMA as schema
from qa.config.settings import ERROR_TAG, SUCCESS_TAG
from qa.config.settings import BASE_API_URL
from qa.clients.api_client import APIClient
from qa.models.api.common_models import ErrorResponse
from qa.utils.test_helpers import validate_response, assert_error_response

@allure.suite("User")
@allure.sub_suite("GetUsers")
@allure.tag("api")
class TestGetAllUsers:
    client = APIClient(BASE_API_URL)

    @pytest.mark.parametrize(
        "login_user,test_data",
        [(item["role"], item) for item in success_cases],
        indirect=["login_user"]
    )
    @allure.tag(SUCCESS_TAG)
    def test_get_all_users_successful(
        self, login_user, test_data, env
    ):
        allure.dynamic.title(test_data["description"])
        with allure.step("Send get all users request"):
            response = self.client.get_all_users(env)

        with allure.step("Assert API response"):
            assert response.status_code == 200, "Failed to get all users"
            response_json = response.json()
            validate_response(response_json=response_json, schema=schema)

    @pytest.mark.parametrize(
        "login_user,test_data",
        [(item["role"], item) for item in error_cases],
        indirect=["login_user"]
    )
    @allure.tag(ERROR_TAG)
    def test_get_all_users_exceptions(
        self, login_user, test_data, env
    ):
        allure.dynamic.title(test_data["description"])
        headers, method = (
            test_data.get("headers"),
            test_data.get("method")
        )

        with allure.step("Send get all users request"):
            response = self.client.get_all_users(env, headers=headers, method=method)

        with allure.step("Assert API response"):
            assert (
                response.status_code == test_data["response"]["status"]
            ), f"Incorrect status code. Response: {response.text}"
            if test_data["response"].get("message"):
                assert_error_response(
                    actual=ErrorResponse(**response.json()), expected=test_data["response"]
                )
            else:
                assert response.content == b''

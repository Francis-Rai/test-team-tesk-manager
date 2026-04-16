import pytest
import allure
from qa.tests.api.test_data.login_params import success_cases, error_cases
from qa.models.api.auth_models import LoginRequest
from qa.models.api.common_models import ErrorResponse
from qa.utils.test_helpers import assert_error_response, set_allure_metadata
from qa.config.settings import BASE_API_URL
from qa.clients.api_client import APIClient


@allure.suite("Authentication")
@allure.sub_suite("Login")
@allure.tag("api")
class TestLogin:
    client = APIClient(BASE_API_URL)

    @pytest.mark.parametrize("test_data", success_cases)
    @set_allure_metadata
    def test_login_successful(self, user_factory, test_data):
        if "request" not in test_data:
            # Generate login data dynamically for the "Login as a user" case
            test_user = user_factory()
            test_data["request"] = LoginRequest(
                email=test_user["user"]["email"],
                password=test_user["user"]["password"],
            )

        with allure.step("Send login request"):
            response = self.client.login(test_data["request"])

        with allure.step("Assert API response"):
            assert response.status_code == 200
            assert "token" in response.json()

    @pytest.mark.parametrize("test_data", error_cases)
    @set_allure_metadata
    def test_login_exceptions(self, user_factory, test_data):
        if "request" not in test_data:
            # Generate login data dynamically for the "Login as a user" case
            test_user = user_factory()
            test_data["request"] = LoginRequest(
                email=test_user["user"]["email"],
                password=test_user["user"]["password"],
            )

        with allure.step("Send login request"):
            response = self.client.login(
                request=test_data["request"], method=test_data.get("method", None)
            )

        with allure.step("Assert API response"):
            assert response.status_code == test_data["response"]["status"]
            if test_data["response"].get("message"):
                assert_error_response(
                    actual=ErrorResponse(**response.json()), expected=test_data["response"]
                )
            else:
                assert response.content == b''

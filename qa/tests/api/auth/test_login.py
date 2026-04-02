import pytest
import allure
from qa.tests.api.test_data.login_params import login, login_exceptions
from qa.models.api.auth_models import LoginErrorResponse, LoginRequest
from qa.utils.test_helpers import assert_error_response, set_report_parameters
from qa.config.settings import ERROR_TAG, SUCCESS_TAG
from qa.config.settings import BASE_API_URL
from qa.clients.api.auth_client import AuthClient

@allure.suite("Authentication")
@allure.sub_suite("Login")
@allure.tag("api")
class TestLogin:
    client = AuthClient(BASE_API_URL)

    @pytest.mark.parametrize(
        "test_data",
        login
    )
    @allure.tag(SUCCESS_TAG)
    def test_login_successful(
        self, registered_user, test_data
    ):
        allure.dynamic.title(test_data["description"])
        if "request" not in test_data:
            # Generate login data dynamically for the "Login as a user" case
            test_data["request"] = LoginRequest(
                email=registered_user["email"], password=registered_user["password"]
            )

        set_report_parameters(test_data["request"])
        with allure.step("Send login request"):
            response = self.client.login(test_data["request"])

        assert response.status_code == 200
        assert "token" in response.json()

    @pytest.mark.parametrize(
        "test_data",
        login_exceptions
    )
    @allure.tag(ERROR_TAG)
    def test_login_exceptions(
        self, registered_user, test_data
    ):
        allure.dynamic.title(test_data["description"])
        if "request" not in test_data:
            # Generate login data dynamically for the "Login as a user" case
            test_data["request"] = LoginRequest(
                email=registered_user["email"], password=registered_user["password"]
            )

        set_report_parameters(test_data["request"])
        with allure.step("Send login request"):
            response = self.client.login(
                request=test_data["request"], method=test_data.get("method", None)
            )

        assert response.status_code == test_data["response"]["status"]
        assert_error_response(
            actual=LoginErrorResponse(**response.json()), expected=test_data["response"]
        )

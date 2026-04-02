import pytest
import allure
from qa.tests.api.test_data.register_params import success_cases, error_cases
from qa.models.api.auth_models import RegisterErrorResponse
from qa.utils.test_helpers import assert_error_response, set_report_parameters
from qa.config.settings import ERROR_TAG, SUCCESS_TAG
from qa.config.settings import BASE_API_URL
from qa.clients.api.auth_client import AuthClient


@allure.suite("Authentication")
@allure.sub_suite("Register")
@allure.tag("api")
class TestRegister:
    client = AuthClient(BASE_API_URL)

    @pytest.mark.parametrize("test_data", success_cases)
    @allure.tag(SUCCESS_TAG)
    def test_register_successful(self, test_data):
        allure.dynamic.title(test_data["description"])

        set_report_parameters(test_data["request"])
        with allure.step("Send register request"):
            response = self.client.register(test_data["request"])

        with allure.step("Assert API response"):
            assert response.status_code == 200
            assert "token" in response.json()

        with allure.step("Get user details"):
            # TODO to add after get user api is created
            pass

    @pytest.mark.parametrize("test_data", error_cases)
    @allure.tag(ERROR_TAG)
    def test_register_exceptions(self, test_data):
        allure.dynamic.title(test_data["description"])
        set_report_parameters(test_data["request"])

        if test_data.get("setup"):
            with allure.step("Setup: Register user"):
                response = self.client.register(
                    request=test_data["request"],
                    method=test_data.get("method", None),
                    attach=False,
                )
                assert (
                    response.status_code == 200
                ), f"Unable to setup register user: {response.content}"

        with allure.step("Send register request"):
            response = self.client.register(
                request=test_data["request"], method=test_data.get("method", None)
            )

        with allure.step("Assert API response"):
            assert response.status_code == test_data["response"]["status"]
            assert_error_response(
                actual=RegisterErrorResponse(**response.json()),
                expected=test_data["response"],
            )

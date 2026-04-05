import pytest
import allure
from qa.tests.api.test_data.change_user_role_params import success_cases, error_cases
from qa.config.settings import BASE_API_URL
from qa.clients.api_client import APIClient
from qa.models.api.common_models import ErrorResponse
from qa.utils.test_helpers import assert_error_response, set_allure_metadata


@allure.suite("User")
@allure.sub_suite("ChangeUserRole")
@allure.tag("api")
class TestChangeUserRole:
    client = APIClient(BASE_API_URL)

    @pytest.mark.parametrize(
        "login_user,test_data",
        [(item["role"], item) for item in success_cases],
        indirect=["login_user"],
    )
    @set_allure_metadata
    def test_change_user_role_successful(
        self, login_user, test_data, env, user_factory
    ):
        with allure.step("Setup: Create user to change role"):
            user = user_factory(role=test_data["setup"]["create_user"])["user"]
            assert (
                user["role"] == test_data["setup"]["create_user"].value
            ), "Failed to setup user. Incorrect user role."

        with allure.step("Send get all users request"):
            request_body = test_data["request"]
            response = self.client.change_user_role(
                env, user_id=user["userId"], request_body=request_body
            )

        with allure.step("Assert API response"):
            assert response.status_code == 204, "Failed to change user role"
            assert response.content == b'', "Expecting no response body"

        with allure.step("Validate user role is updated with GET endpoint"):
            get_response = self.client.get_all_users(env=env)
            assert get_response.status_code == 200, "Unable to retrieve get users"
            get_results = get_response.json()
            user_details = next(
                (u for u in get_results if u.get("id") == user["userId"]), None
            )
            assert user_details, "Unable to retrieve updated user"
            assert (
                user_details["role"] == request_body["role"].upper()
            ), "Mismatch user role"

    @pytest.mark.parametrize(
        "login_user,test_data",
        [(item["role"], item) for item in error_cases],
        indirect=["login_user"],
    )
    @set_allure_metadata
    def test_change_user_role_exceptions(self, login_user, test_data, env, user_factory):
        headers, method = (test_data.get("headers"), test_data.get("method"))

        user_id = login_user["userId"]
        if create_user := test_data.get("setup", {}).get("create_user"):
            with allure.step("Setup: Create user to change role"):
                user = user_factory(role=create_user)["user"]
                assert (
                    user["role"] == create_user.value
                ), "Failed to setup user. Incorrect user role."
                user_id = user["userId"]
        # if no user created, use uid of logged in user

        with allure.step("Send get all users request"):
            response = self.client.change_user_role(
                env=env,
                headers=headers,
                method=method,
                user_id=user_id,
                request_body=test_data["request"],
            )

        with allure.step("Assert API response"):
            assert (
                response.status_code == test_data["response"]["status"]
            ), f"Incorrect status code. Response: {response.text}"
            if test_data["response"].get("message"):
                assert_error_response(
                    actual=ErrorResponse(**response.json()),
                    expected=test_data["response"],
                )
            else:
                assert response.content == b""

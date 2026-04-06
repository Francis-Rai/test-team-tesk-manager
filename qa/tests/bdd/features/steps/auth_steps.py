from behave import given, when, then
from hamcrest import assert_that, equal_to, has_key, instance_of
from qa.utils.common import generate_email, generate_password
from qa.config.enums import UserRole
from qa.models.entity.user import User
from qa.config.settings import SUPER_USER_EMAIL, SUPER_USER_PASSWORD
from qa.models.api.auth_models import LoginRequest, RegisterRequest
import allure

user_register = RegisterRequest.create_new_user()
super_user_login = LoginRequest(email=SUPER_USER_EMAIL, password=SUPER_USER_PASSWORD)

@given('a user is registered with role "{role}"')
def step_register_user(context, role):
    # register user
    with allure.step(f"Register as a USER"):
        response = context.api_client.register(user_register)
        assert_that(response.status_code, equal_to(200), f"Login failed: {response.content}")
        user = User(**response.json()["user"])
        token = f"Bearer {response.json()["token"]}"

    if role != UserRole.USER:
        with allure.step(f"Update role to {role}"):
            # login as super user
            context.token = context.super_user_token

            # change user role
            response = context.api_client.change_user_role(
                env=context,
                user_id=user.userId,
                request_body={"role": role},
            )
            assert_that(
                response.status_code,
                equal_to(204),
                f"Failed to change role from {user.role} to {role}: {response.content}",
            )

    context.user = user
    context.token = token

@when('the user accesses a "{role}"-only endpoint')
def step_access_admin_only_resource(context, role):
    response = None
    if role == UserRole.ADMIN:
        raise NotImplementedError("No Admin only endpoint yet")
    elif role == UserRole.SUPER_ADMIN:
        assert_that(context.test_user, instance_of(User), "No test user created")
        response = context.api_client.change_user_role(
            env=context,
            user_id=context.test_user.userId,
            request_body={"role": UserRole.ADMIN.value},
        )
    context.response = response

@then("the API should return a successful response")
def step_assert_successful_api(context):
    assert_that(
        context.response.status_code,
        equal_to(204),
        f"Super-admin endpoint failed: {context.response.content}",
    )

@when('the user\'s role is updated to "{role}"')
def step_update_user_role(context, role):
    assert_that(context.test_user, instance_of(User), "No test user created")

    # login as super user
    user_token = context.token
    context.token = context.super_user_token

    # change user role
    response = context.api_client.change_user_role(
        env=context, user_id=context.user.userId, request_body={"role": role}
    )
    assert_that(
        response.status_code,
        equal_to(204),
        f"Failed to change role from {context.user.role} to {role}: {response.content}",
    )

    # login as the updated user
    context.token = user_token


@then("the API should be forbidden")
def step_assert_api_forbidden(context):
    assert_that(
        context.response.status_code,
        equal_to(403),
        f"Unexpected API response: {context.response.content}",
    )

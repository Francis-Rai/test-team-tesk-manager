from behave import given, when, then
from qa.utils.data_generator import generate_email, generate_password
from qa.models.auth_models import LoginRequest

@given("a registered user exists")
def step_create_user(context):
    test_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": generate_email(),
        "password": generate_password()
    }
    response = context.auth_client.register(test_user, attach=False)
    assert response.status_code == 200
    context.user = test_user


@when("the user logs in with valid credentials")
def step_login(context):
    response = context.auth_client.login(
        LoginRequest(email=context.user["email"], password=context.user["password"])
    )
    context.response = response


@then("the login should be successful")
def step_validate(context):
    assert context.response.status_code == 200

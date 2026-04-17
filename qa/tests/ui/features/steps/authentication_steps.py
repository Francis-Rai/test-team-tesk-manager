from behave import given, when, then
from qa.pages.login_page import LoginPage
from qa.utils.common import generate_register_data
from hamcrest import assert_that, equal_to, not_

@given("the user is on the login page")
def step_user_on_login_page(context):
    """Navigate to login page."""
    print("Navigating to login page")
    context.page.goto(f"{context.base_url}/login")
    context.login_page = LoginPage(context.page)

@when("the user enters valid registration details and submits the form")
def step_register_user(context):
    """Fill up register form and submit"""
    context.new_user_data = generate_register_data()
    
    context.login_page.register(**context.new_user_data)

@then("the login form should be displayed and pre-filled")
def step_check_login_form_prefilled(context):
    """Check if login form is pre-filled with registered email."""
    # Assuming the email field should be pre-filled after registration
    context.login_page.verify_login_form_displayed()
    email_value = context.login_page.form.get_field_value("email")
    assert_that(
        email_value,
        equal_to(context.new_user_data["email"]),
        "Login form email field should be pre-filled with registered email",
    )
    assert_that(
        context.login_page.form.get_field_value("password"),
        not_(equal_to("")),
        "Login form password field should be pre-filled"
    )

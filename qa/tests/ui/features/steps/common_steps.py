"""Common step definitions for UI tests - PCOM approach."""
from behave import given, when, then
from qa.pages.login_page import LoginPage
from qa.pages.projects_page import ProjectsPage
from qa.pages.components.header_component import HeaderComponent
from qa.pages.tasks_page import TasksPage
import time


@given('the user navigates to "{page}"')
def step_navigate_to_page(context, page):
    """Navigate to a page."""
    url = f"{context.base_url}/{page}"
    context.base_page.goto(url)


@given('the user is logged in')
def step_user_logged_in(context):
    """Log in user."""
    context.base_page.goto(f"{context.base_url}/login")
    login_page = LoginPage(context.page)
    login_page.login("user@example.com", "password")


@when('the user clicks on "{button}"')
def step_click_button(context, button):
    """Click button by label/text."""
    context.base_page.click_by_text(button)

@when('the user clicks on the user menu in the header and selects "{option}"')
def step_click_button_in_header(context, option):
    """Click button by label/text."""
    # Find button by text content
    header = HeaderComponent(context.page)
    header.click_user_menu()

    # Click the specified option in the opened menu
    header.select_user_menu_option(option)

@then('the user should be redirected to the "{page}" page')
def step_check_redirection(context, page):
    """Check if user is redirected to expected page."""
    expected_url = f"{context.base_url}/{page}"
    context.page.wait_for_url(expected_url)
    actual_url = context.page.url
    assert (
        actual_url == expected_url
    ), f"Expected to be on {expected_url}, but was on {actual_url}"

@when('the user clicks on "{option}" option in the header')
def step_click_option_in_header(context, option):
    """Click option in user menu in header."""
    # Click user profile to open menu
    header = HeaderComponent(context.page)

    # Click the specified option in the opened menu
    header.select_user_menu_option(option)

@when('the user fills "{field}" with "{value}"')
def step_fill_field(context, field, value):
    """Fill input field with value."""
    # Find input by label/placeholder
    selector = f'input[placeholder="{field}"], input[aria-label="{field}"]'
    context.base_page.fill(selector, value)


@when('the user waits for "{time_str}" seconds')
def step_wait(context, time_str):
    """Wait for specified seconds."""
    time.sleep(float(time_str))


@then('the page title should be "{title}"')
def step_check_page_title(context, title):
    """Check page title."""
    page_title = context.page.title
    assert page_title == title, f"Expected '{title}', got '{page_title}'"


@then('"{text}" should be visible')
def step_text_visible(context, text):
    """Check if text is visible on page."""
    selector = f'text={text}'
    is_visible = context.base_page.is_visible(selector)
    assert is_visible, f"Text '{text}' is not visible"


@then('"{text}" should not be visible')
def step_text_not_visible(context, text):
    """Check if text is not visible on page."""
    selector = f'text={text}'
    is_visible = context.base_page.is_visible(selector)
    assert not is_visible, f"Text '{text}' is visible but shouldn't be"


# Page Object Model helpers
@given('the user is on the projects page')
def step_user_on_projects_page(context):
    """Navigate to projects page."""
    context.base_page.goto(f"{context.base_url}/projects")
    context.projects_page = ProjectsPage(context.page)


@given('the user is on the tasks page')
def step_user_on_tasks_page(context):
    """Navigate to tasks page."""
    context.base_page.goto(f"{context.base_url}/tasks")
    context.tasks_page = TasksPage(context.page)

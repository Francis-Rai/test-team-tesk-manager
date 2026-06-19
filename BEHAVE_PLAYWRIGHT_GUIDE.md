# Behave + Playwright UI Testing Setup

## Project Structure

```
qa/
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Base class for all pages
│   ├── login_page.py          # Login page example
│   └── (other page objects)
├── tests/
│   ├── ui/
│   │   ├── steps/
│   │   │   ├── __init__.py
│   │   │   ├── common_steps.py    # Common step definitions
│   │   │   └── (other steps)
│   │   ├── conftest.py            # Pytest integration (optional)
│   │   ├── environment.py         # Behave hooks (browser setup)
│   │   ├── (feature files)
│   │   └── .todo
│   └── api/
└── requirements.txt
```

## How It Works

### 1. **Feature Files** (`*.feature`)
Define test scenarios in Gherkin format:
```gherkin
Feature: User Login

  Scenario: Valid login
    Given the user navigates to "login"
    When the user fills "email" with "user@example.com"
    And the user fills "password" with "password123"
    And the user clicks "Login"
    Then the page title should be "Dashboard"
```

### 2. **Environment Hooks** (`environment.py`)
- **before_all()**: Launches browser once, sets up database, creates event loop
- **before_scenario()**: Launches new browser context and page for each test
- **after_scenario()**: Closes browser, cleans up database
- **after_all()**: Closes database connection

### 3. **Page Objects** (`pages/`)
Encapsulate UI interactions:
```python
class LoginPage(BasePage):
    EMAIL_INPUT = '[data-testid="email"]'
    LOGIN_BUTTON = 'button:has-text("Login")'
    
    async def login(self, email, password):
        await self.fill(self.EMAIL_INPUT, email)
        await self.click(self.LOGIN_BUTTON)
```

### 4. **Step Definitions** (`steps/`)
Connect feature files to page objects:
```python
@when('the user clicks "{button}"')
def step_click_button(context, button):
    selector = f'button:has-text("{button}")'
    context.loop.run_until_complete(context.page.click(selector))
```

### 5. **Behave Configuration** (`behave.ini`)
Configure test execution:
```ini
[behave]
paths = qa/tests/ui
format = progress
logging_level = DEBUG
```

## Running Tests

### Run all tests
```bash
behave
```

### Run specific feature
```bash
behave qa/tests/ui/login.feature
```

### Run only scenarios with specific tag
```bash
behave --tags=@wip
```

### Run with specific browser
Modify `environment.py`:
```python
await context.playwright.firefox.launch()  # or webkit
```

### Debug mode
```bash
behave --no-capture --logging-level DEBUG
```

### Generate reports
```bash
behave --format json.pretty -o allure-results/behave.json
```

## Key Files Reference

- **`environment.py`**: Browser lifecycle management
- **`conftest.py`**: Pytest compatibility (optional)
- **`behave.ini`**: Behave configuration
- **`base_page.py`**: Common page methods
- **`common_steps.py`**: Reusable step definitions

## Writing New Tests

### 1. Create feature file (`qa/tests/ui/example.feature`)
```gherkin
Feature: Example Feature

  Scenario: Example scenario
    Given the user navigates to "example"
    When the user clicks "Button"
    Then "Success" should be visible
```

### 2. Create step definitions (`qa/tests/ui/steps/example_steps.py`)
```python
from behave import given, when, then

@given('the user navigates to "{page}"')
def step_navigate(context, page):
    context.loop.run_until_complete(context.page.goto(f"{context.base_url}/{page}"))
```

### 3. Create page object if needed (`qa/pages/example_page.py`)
```python
from qa.pages.base_page import BasePage

class ExamplePage(BasePage):
    BUTTON = 'button:has-text("Button")'
    
    async def click_button(self):
        await self.click(self.BUTTON)
```

## Best Practices

✅ **Do:**
- Use `data-testid` attributes for selectors
- Keep page objects focused on one page
- Use meaningful selector names
- Use async/await for all Playwright calls
- Clean up database after each scenario
- Use tags for test organization

❌ **Don't:**
- Use `time.sleep()` — use `wait_for_selector()` instead
- Put complex logic in step definitions
- Hardcode URLs — use `context.base_url`
- Mix Playwright calls with step logic
- Create brittle selectors based on text/position

## Async/Await Pattern

All Playwright calls must run through the event loop:

```python
# In step definitions
context.loop.run_until_complete(context.page.click(selector))

# In page objects (async methods)
async def click_button(self):
    await self.click(self.BUTTON)
```

## Debugging

### View test execution
Remove `headless=True` in `environment.py`:
```python
await context.playwright.chromium.launch(headless=False)
```

### Capture screenshots
```python
@then('take a screenshot')
def step_screenshot(context):
    context.loop.run_until_complete(
        context.page.screenshot(path='screenshot.png')
    )
```

### Check page state
```python
url = context.page.url
title = context.page.title
content = context.loop.run_until_complete(context.page.content())
```

## Troubleshooting

**Q: Tests hang or timeout**
- A: Increase timeout in selectors, check if page is loading
- Use `wait_for_load_state()` before assertions

**Q: Selector not found**
- A: Use `context.page.pause()` to debug, check selector in DevTools

**Q: Database not cleaning up**
- A: Check `after_scenario()` in environment.py, verify database connection

**Q: Browser not opening**
- A: Run `playwright install` to download browsers

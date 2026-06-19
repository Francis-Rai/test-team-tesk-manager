# Playwright Selectors & Tips for Behave

## Selecting Elements

### By Test ID (Recommended)
```python
'[data-testid="button"]'
```

### By Text (Useful)
```python
'button:has-text("Click Me")'
'text=Success'  # Anywhere on page
```

### By Placeholder
```python
'input[placeholder="Enter email"]'
```

### By Label
```python
'input[aria-label="Username"]'
```

### By Name Attribute
```python
'input[name="password"]'
```

### By Type
```python
'button[type="submit"]'
'input[type="checkbox"]'
```

### Combinations
```python
'div.container button:has-text("Save")'
'form input[type="email"]'
```

### XPath (Last resort)
```python
'//button[contains(text(), "Click")]'
```

## Common Playwright Methods in Behave

```python
# Navigation
await context.page.goto("http://example.com")

# Click
await context.page.click("button")

# Fill form
await context.page.fill("input", "value")

# Get text
text = await context.page.inner_text("div.message")

# Check visibility
is_visible = await context.page.is_visible("button")

# Wait for element
await context.page.wait_for_selector("button")

# Wait for navigation
await context.page.wait_for_load_state("networkidle")

# Take screenshot
await context.page.screenshot(path="screenshot.png")

# Execute JS
result = await context.page.evaluate("() => 1 + 1")

# Get page title
title = context.page.title

# Get URL
url = context.page.url

# Select option
await context.page.select_option("select", "value")

# Check checkbox
await context.page.check("input[type=checkbox]")

# Uncheck checkbox
await context.page.uncheck("input[type=checkbox]")

# Hover
await context.page.hover("button")

# Keyboard
await context.page.keyboard.press("Enter")
await context.page.keyboard.type("Hello")

# Get attribute
value = await context.page.get_attribute("button", "disabled")
```

## Waiting Strategies

### Wait for Element
```python
await context.page.wait_for_selector("button", timeout=5000)
```

### Wait for URL
```python
await context.page.wait_for_url("**/dashboard")
```

### Wait for Response
```python
async with context.page.expect_response("**/api/users") as response:
    # Trigger request
    await context.page.click("button")
result = response.value
```

### Wait for Load State
```python
await context.page.wait_for_load_state("networkidle")  # Default
await context.page.wait_for_load_state("load")         # DOM loaded
await context.page.wait_for_load_state("domcontentloaded")
```

### Wait for Condition
```python
while not await context.page.is_visible("button"):
    await context.page.wait_for_timeout(100)
```

## Step Definition Patterns

### Using Page Objects
```python
from behave import when
from qa.pages.login_page import LoginPage

@when('user logs in')
def step_login(context):
    page = LoginPage(context.page)
    context.loop.run_until_complete(page.login("user@test.com", "pass"))
```

### Direct Page Access
```python
from behave import then

@then('"{text}" should be visible')
def step_text_visible(context, text):
    is_visible = context.loop.run_until_complete(
        context.page.is_visible(f'text={text}')
    )
    assert is_visible, f"{text} not found"
```

### Data Tables
```python
@given('user enters the following data')
def step_enter_data(context):
    for row in context.table:
        selector = row['field']
        value = row['value']
        context.loop.run_until_complete(
            context.page.fill(selector, value)
        )
```

## Handling Waits

### ✅ Good - Auto-wait
```python
# Playwright auto-waits for element
await context.page.click("button")
```

### ❌ Bad - Hard sleep
```python
import time
time.sleep(2)  # Don't do this!
```

### ✅ Better - Explicit wait
```python
await context.page.wait_for_selector("button")
await context.page.click("button")
```

## Assertions

### Simple assertions
```python
assert "Welcome" in context.loop.run_until_complete(
    context.page.content()
)
```

### Using is_visible
```python
is_visible = context.loop.run_until_complete(
    context.page.is_visible("button")
)
assert is_visible
```

### Using Playwright expect (async)
```python
from playwright.async_api import expect

async def check_button_text():
    await expect(context.page.locator("button")).to_have_text("Click Me")

context.loop.run_until_complete(check_button_text())
```

## Debugging

### Pause execution
```python
@then('debug')
def step_debug(context):
    context.loop.run_until_complete(context.page.pause())
```

### Print page state
```python
print(f"URL: {context.page.url}")
print(f"Title: {context.page.title}")
```

### Get element count
```python
count = await context.page.query_selector_all("button")
print(f"Found {len(count)} buttons")
```

### Take screenshot
```python
@then('take screenshot')
def step_screenshot(context):
    context.loop.run_until_complete(
        context.page.screenshot(path="debug.png")
    )
```

## Handle Common Scenarios

### Login
```python
await context.page.fill('[data-testid="email"]', "user@test.com")
await context.page.fill('[data-testid="password"]', "pass")
await context.page.click('button:has-text("Login")')
await context.page.wait_for_url("**/dashboard")
```

### Select Dropdown
```python
await context.page.select_option('select[name="role"]', "admin")
```

### Handle Modal
```python
await context.page.click('button:has-text("Confirm")')
await context.page.wait_for_selector(".modal", state="hidden")
```

### File Upload
```python
await context.page.set_input_files('input[type="file"]', "path/to/file.pdf")
```

### Multiple Tabs/Windows
```python
with context.page.expect_popup() as popup:
    await context.page.click('a[target="_blank"]')
new_page = popup.value
```

### Keyboard Shortcuts
```python
await context.page.keyboard.press("Escape")  # Close modal
await context.page.keyboard.press("Enter")   # Submit form
await context.page.keyboard.press("Tab")     # Navigate
```

## Performance Tips

- Use `data-testid` for reliable, fast selectors
- Avoid XPath (slower)
- Use `:has-text()` only as fallback
- Combine with ancestor selectors: `'div.form button:has-text("Save")'`
- Use `wait_for_load_state("load")` instead of `networkidle` for speed

# PCOM Implementation Guide

## What is PCOM?

**PCOM = Page Component Object Model** - An evolution of POM that breaks pages into reusable, composable components.

## Structure

```
pages/
├── base_page.py                 # Base class with Playwright methods
├── components/
│   ├── __init__.py
│   ├── base_component.py        # Base component class
│   ├── form_component.py        # Reusable form handling
│   ├── list_component.py        # Reusable lists/tables
│   ├── modal_component.py       # Reusable modals/dialogs
│   ├── header_component.py      # Application header
│   └── navigation_component.py  # Navigation/sidebar
├── login_page.py                # Uses FormComponent
├── projects_page.py             # Uses FormComponent, ListComponent, ModalComponent
└── tasks_page.py                # Uses FormComponent, ListComponent, ModalComponent
```

## Components Explained

### 1. **BaseComponent**
Base class for all components with selector scoping.

```python
class BaseComponent:
    def __init__(self, page, component_selector):
        self.page = page
        self.component_selector = component_selector
    
    def click(self, selector):
        # Automatically scopes selector to component
        full = f'{self.component_selector} {selector}'
        self.page.click(full)
```

**Benefit:** Selector logic stays within component boundary.

---

### 2. **FormComponent**
Handles form interactions - fill, submit, validate.

```python
form = FormComponent(page, '.login-form')
form.fill_field('email', 'user@test.com')
form.fill_field('password', 'password')
form.submit()
error = form.get_field_error('email')
```

**Supports:**
- Multiple field selector strategies (name, data-testid, placeholder)
- Auto-detect submit button variants
- Field-specific error handling

---

### 3. **ListComponent**
Handles lists, tables, grids.

```python
projects = ListComponent(page, '.projects-list', '.project-item')
count = projects.get_item_count()
projects.click_item_by_text('My Project')
all_items = projects.get_all_item_texts()
projects.filter_items('[filter-btn]', 'Active')
```

**Supports:**
- Get item count
- Click by index or text
- Filter and sort
- Check if item exists

---

### 4. **ModalComponent**
Handles modals and dialogs.

```python
modal = ModalComponent(page, '.create-project-modal')
modal.wait_for_open()
modal.fill_form_field('name', 'Project')
modal.confirm()
modal.wait_for_close()
```

**Supports:**
- Open/close detection
- Button click (Confirm, Cancel, etc.)
- Form filling within modal
- Title and message extraction

---

### 5. **HeaderComponent**
Handles application header.

```python
header = HeaderComponent(page, 'header')
name = header.get_user_profile_name()
header.click_logout()
header.search('query')
header.get_notification_count()
```

**Supports:**
- Profile management
- Logout
- Search
- Notifications

---

### 6. **NavigationComponent**
Handles sidebars and menus.

```python
nav = NavigationComponent(page, 'nav')
nav.click_link('Projects')
is_active = nav.is_link_active('Projects')
nav.expand_menu_section('Admin')
```

**Supports:**
- Click navigation
- Active state detection
- Menu expansion

---

## Page Objects Using Components

### LoginPage (Simple)
```python
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.form = FormComponent(page, '.login-form')
    
    def login(self, email, password):
        self.form.fill_field('email', email)
        self.form.fill_field('password', password)
        self.form.submit()
```

### ProjectsPage (Complex)
```python
class ProjectsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.nav = NavigationComponent(page)
        self.project_list = ListComponent(page, '.list', '.item')
        self.create_modal = ModalComponent(page, '.modal')
    
    def create_project(self, name, desc):
        self.click('button:has-text("Create")')
        self.create_modal.wait_for_open()
        self.create_modal.fill_form_field('name', name)
        self.create_modal.fill_form_field('desc', desc)
        self.create_modal.confirm()
    
    def open_project(self, name):
        self.project_list.click_item_by_text(name)
```

---

## Benefits of PCOM

✅ **Reusable** - FormComponent used everywhere  
✅ **Maintainable** - Change form logic in one place  
✅ **Scalable** - Complex pages stay organized  
✅ **Testable** - Components can be tested independently  
✅ **Clear Intent** - Component name describes what it does  
✅ **DRY** - No code duplication across pages  

---

## Step Definitions Using PCOM

```python
@when('user creates a project "{name}"')
def step_create_project(context, name):
    context.projects_page.create_project(name)

@then('project "{name}" should be visible')
def step_project_visible(context, name):
    assert context.projects_page.is_project_visible(name)
```

---

## When to Use Components

| Situation | Use Component |
|-----------|---|
| **Form with multiple fields** | FormComponent |
| **List/table of items** | ListComponent |
| **Modal/dialog** | ModalComponent |
| **Header/app bar** | HeaderComponent |
| **Sidebar/menu** | NavigationComponent |
| **One-off element** | BasePage directly |

---

## Selector Strategy in Components

Components try multiple selector strategies in order:

### FormComponent
```python
# Tries these in order:
1. [data-testid="field"]      # Most specific
2. [name="field"]             # Standard HTML
3. input[placeholder="field"] # User-visible
```

### ModalComponent
```python
# Close button - tries:
1. [data-testid="close"]
2. button[aria-label="Close"]
3. .close
4. button:has-text("Close")
```

This makes components flexible and resilient to UI changes.

---

## Adding New Components

1. **Create** `qa/pages/components/your_component.py`
2. **Extend** `BaseComponent`
3. **Implement** component-specific methods
4. **Use** in page objects

Example:
```python
# components/search_component.py
from .base_component import BaseComponent

class SearchComponent(BaseComponent):
    def search(self, query):
        self.fill('input', query)
        self.press_key('Enter')
    
    def get_results_count(self):
        return self.page.query_selector_all(
            f'{self.component_selector} .result'
        ).count()
```

---

## Feature File Examples

```gherkin
Feature: Project Management
  
  Scenario: User can create and view project
    Given the user is logged in
    When user creates a project "Test Project"
    Then "Test Project" should be visible in projects list
    When user opens "Test Project"
    Then the project details page should load
```

Step definitions:
```python
@when('user creates a project "{name}"')
def step_create(context, name):
    context.projects_page = ProjectsPage(context.page)
    context.projects_page.create_project(name)

@then('"{name}" should be visible')
def step_visible(context, name):
    assert context.projects_page.is_project_visible(name)
```

---

## Best Practices

✅ **One component = one concern** (form, list, modal)  
✅ **Reuse components across pages**  
✅ **Keep selectors flexible** (try multiple strategies)  
✅ **Use data-testid in HTML** when possible  
✅ **Document selector patterns** in components  
✅ **Test components independently** if complex  

---

## Migration from POM to PCOM

### Before (POM)
```python
class ProjectsPage:
    FORM = '.form'
    EMAIL = '.form input[name="email"]'
    SUBMIT = '.form button[type="submit"]'
    LIST = '.list'
    ITEM = '.list .item'
    MODAL = '.modal'
    
    def create_project(self, name):
        # 20 lines of code
```

### After (PCOM)
```python
class ProjectsPage:
    def __init__(self, page):
        self.form = FormComponent(page, '.form')
        self.list = ListComponent(page, '.list')
        self.modal = ModalComponent(page, '.modal')
    
    def create_project(self, name):
        # 3 lines of code using components
```

---

## Next Steps

1. Review the components in `qa/pages/components/`
2. Study how they're used in `projects_page.py` and `tasks_page.py`
3. Create feature files and step definitions
4. Run tests: `behave`

Enjoy the cleaner, more maintainable PCOM approach!

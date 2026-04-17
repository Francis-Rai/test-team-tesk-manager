"""Form component for handling form interactions using locators."""
from playwright.sync_api import Page
from .base_component import BaseComponent


class FormComponent(BaseComponent):
    """Reusable form component for login, registration, etc."""
    
    def __init__(self, page: Page, form_selector: str):
        """Initialize form component.
        
        Args:
            page: Playwright Page instance
            form_selector: CSS selector for the form element
        """
        super().__init__(page, form_selector)
        self.form_selector = form_selector

    def get_field(self, field_name: str):
        """Get form field locator by name.
        
        Args:
            field_name: Field name attribute or data-testid
            
        Returns:
            Locator for the form field
        """
        # Try multiple selector strategies with locators
        selectors = [
            f'{self.form_selector} input[name="{field_name}"]',
        ]

        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator

        raise AssertionError(f"Could not find field: {field_name}")

    def fill_field(self, field_name: str, value: str):
        """Fill form field by name using locator.
        
        Args:
            field_name: Field name attribute or data-testid
            value: Value to fill
        """
        locator = self.get_field(field_name)
        if self.get_field(field_name):
            locator.fill(value)
            return
        
        raise AssertionError(f"Could not find field: {field_name}")
    
    def submit(self):
        """Submit form by clicking submit button using locator."""
        # Try different submit button selectors with locators
        selector = 'button[type="submit"]'
        
        locator = self._get_scoped_locator(selector)
        if locator.is_visible():
            locator.click()
            return

        raise AssertionError("Could not find submit button")
    
    def get_field_value(self, field_name: str) -> str:
        """Get value of form field using locator.
        
        Args:
            field_name: Field name attribute or data-testid
            
        Returns:
            Field value
        """
        selectors = [
            f'input[name="{field_name}"]',
            f'[data-testid="{field_name}"]',
        ]
        
        for selector in selectors:
            locator = self._get_scoped_locator(selector)
            if locator.is_visible():
                return locator.input_value()
        
        raise AssertionError(f"Could not find field: {field_name}")
    
    def clear_field(self, field_name: str):
        """Clear form field using locator.
        
        Args:
            field_name: Field name attribute or data-testid
        """
        selectors = [
            f'[data-testid="{field_name}"]',
            f'[name="{field_name}"]',
        ]
        
        for selector in selectors:
            locator = self._get_scoped_locator(selector)
            if locator.is_visible():
                locator.fill('')
                return
        
        raise AssertionError(f"Could not find field: {field_name}")
    
    def is_form_visible(self) -> bool:
        """Check if form is visible using locator.
        
        Returns:
            True if form is visible
        """
        return self.page.locator(self.form_selector).is_visible()
    
    def get_field_error(self, field_name: str) -> str:
        """Get error message for a field using locator.
        
        Args:
            field_name: Field name
            
        Returns:
            Error message text
        """
        # Common error message selectors
        selectors = [
            f'[data-testid="{field_name}-error"]',
            f'[data-error="{field_name}"]',
            f'.error-{field_name}',
        ]
        
        for selector in selectors:
            if self.is_visible(selector):
                return self.get_text(selector)
        
        return ""

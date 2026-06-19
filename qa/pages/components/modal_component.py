"""Modal component for handling modals and dialogs using locators."""
from playwright.sync_api import Page
from .base_component import BaseComponent


class ModalComponent(BaseComponent):
    """Reusable component for handling modals and dialogs."""
    
    def __init__(self, page: Page, modal_selector: str):
        """Initialize modal component.
        
        Args:
            page: Playwright Page instance
            modal_selector: CSS selector for the modal element
        """
        super().__init__(page, modal_selector)
        self.modal_selector = modal_selector
    
    def is_open(self) -> bool:
        """Check if modal is open using locator.
        
        Returns:
            True if modal is visible
        """
        return self.page.locator(self.modal_selector).is_visible()
    
    def wait_for_open(self, timeout: int = 5000):
        """Wait for modal to open using locator.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self.page.locator(self.modal_selector).wait_for(timeout=timeout)
    
    def wait_for_close(self, timeout: int = 5000):
        """Wait for modal to close using locator.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self.page.locator(self.modal_selector).wait_for(state='hidden', timeout=timeout)
    
    def close(self):
        """Close modal by clicking close button using locator."""
        close_selectors = [
            f'{self.modal_selector} [data-testid="close"]',
            f'{self.modal_selector} button[aria-label="Close"]',
            f'{self.modal_selector} .close',
            f'{self.modal_selector} button:has-text("Close")',
            f'{self.modal_selector} button:has-text("Cancel")',
        ]
        
        for selector in close_selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError("Could not find close button")
    
    def get_title(self) -> str:
        """Get modal title using locator.
        
        Returns:
            Modal title text
        """
        selectors = [
            f'{self.modal_selector} [data-testid="modal-title"]',
            f'{self.modal_selector} h1',
            f'{self.modal_selector} h2',
            f'{self.modal_selector} .modal-title',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator.text_content()
        
        return ""
    
    def get_message(self) -> str:
        """Get modal message/content using locator.
        
        Returns:
            Modal message text
        """
        selectors = [
            f'{self.modal_selector} [data-testid="modal-message"]',
            f'{self.modal_selector} .modal-body',
            f'{self.modal_selector} p',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator.text_content()
        
        return ""
    
    def click_button(self, button_text: str):
        """Click button in modal by text using locator.
        
        Args:
            button_text: Button text
        """
        selector = f'{self.modal_selector} button:has-text("{button_text}")'
        self.page.locator(selector).click()
    
    def confirm(self):
        """Click confirm/OK button."""
        self.click_button_variants(['Confirm', 'OK', 'Save', 'Yes', 'Submit'])
    
    def cancel(self):
        """Click cancel button."""
        self.click_button_variants(['Cancel', 'No', 'Close', 'Dismiss'])
    
    def click_button_variants(self, texts: list):
        """Click first available button from list of texts using locator.
        
        Args:
            texts: List of possible button texts
        """
        for text in texts:
            selector = f'{self.modal_selector} button:has-text("{text}")'
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError(f"Could not find button with text: {texts}")
    
    def fill_form_field(self, field_name: str, value: str):
        """Fill form field within modal using locator.
        
        Args:
            field_name: Field name
            value: Value to fill
        """
        selector = f'{self.modal_selector} input[name="{field_name}"]'
        self.page.locator(selector).fill(value)

"""Login page using PCOM (Page Component Object Model)."""
from playwright.sync_api import Page, expect
from qa.pages.base_page import BasePage
from qa.pages.components import FormComponent


class LoginPage(BasePage):
    """Login page using components."""
    PAGE_URL_PATTERN = "**/login"

    # Component selectors
    FORM_SELECTOR = 'div[data-slot="card-content"] form'
    ERROR_MESSAGE = '[data-testid="error"], .error-message, .alert-danger'
    SUCCESS_MESSAGE = '[data-testid="success"], .success-message, .alert-success'
    
    def __init__(self, page: Page):
        """Initialize login page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        # Initialize form component
        self.form = FormComponent(page, self.FORM_SELECTOR)
        self._verify_page_loaded()
    
    def _verify_page_loaded(self):
        """Verify we're on the correct page."""
        self.page.wait_for_url(self.PAGE_URL_PATTERN)
        expect(self.page.locator(":text-is('Login to your account')")).to_be_visible()

    def verify_login_form_displayed(self) -> bool:
        """Check if login form is displayed."""
        expect(self.page.locator("input[name=\"firstName\"]")).not_to_be_visible()
        expect(self.page.locator("input[name=\"lastName\"]")).not_to_be_visible()
        self.form.get_field("email")
        self.form.get_field("password")

    def login(self, email: str, password: str):
        """Perform login.
        
        Args:
            email: User email
            password: User password
        """
        self.form.fill_field("email", email)
        self.form.fill_field("password", password)
        self.form.submit()
        self.wait_for_url("**/teams")

    def register(self, first_name:str, last_name: str, email: str, password: str):
        """
        Register new user via registration form.
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User email
            password: User password
        """
        self.form.fill_field("firstName", first_name)
        self.form.fill_field("lastName", last_name)
        self.form.fill_field("email", email)
        self.form.fill_field("password", password)
        self.form.submit()
        self.wait_for_load_state("networkidle")


    def get_error_message(self) -> str:
        """Get error message text.
        
        Returns:
            Error message text
        """
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed.
        
        Returns:
            True if error is displayed
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    def is_success_displayed(self) -> bool:
        """Check if success message is displayed.
        
        Returns:
            True if success is displayed
        """
        return self.is_visible(self.SUCCESS_MESSAGE)
    
    def get_field_error(self, field_name: str) -> str:
        """Get field-specific error message.
        
        Args:
            field_name: Field name (email, password)
            
        Returns:
            Error message text
        """
        return self.form.get_field_error(field_name)

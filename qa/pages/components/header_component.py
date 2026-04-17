"""Header component for application header and navigation using locators."""
from playwright.sync_api import Page
from qa.pages.components.base_component import BaseComponent


class HeaderComponent(BaseComponent):
    """Reusable component for application header."""
    USER_MENU_BTN = "button[data-slot='dropdown-menu-trigger']"
    USER_MENU_OPTION = 'div[role="menuitem"]:has-text("{option_text}")'
    
    def __init__(self, page: Page, header_selector: str = 'div:has(~ main)'):
        """Initialize header component.
        
        Args:
            page: Playwright Page instance
            header_selector: CSS selector for header element
        """
        super().__init__(page, header_selector)
        self.header_selector = header_selector
    
    def get_title(self) -> str:
        """Get page title from header using locator.
        
        Returns:
            Title text
        """
        selectors = [
            f'{self.header_selector} [data-testid="page-title"]',
            f'{self.header_selector} h1',
            f'{self.header_selector} .title',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator.text_content()
        
        return ""

    def click_user_menu(self):
        """Click user menu/profile in header"""
        self.click(selector=self.USER_MENU_BTN)

    def select_user_menu_option(self, option_text: str):
        """Select option from user menu in header"""
        option_locator = self.page.locator(self.USER_MENU_OPTION.format(option_text=option_text))
        if option_locator.is_visible():
            option_locator.click()
            return
        
        raise AssertionError(f"Could not find user menu option: {option_text}")

    def get_user_profile_name(self) -> str:
        """Get logged-in user name from profile using locator.
        
        Returns:
            User name
        """
        selectors = [
            f'{self.header_selector} [data-testid="user-name"]',
            f'{self.header_selector} .user-profile',
            f'{self.header_selector} .profile-name',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator.text_content()
        
        return ""
    
    def click_user_profile(self):
        """Click user profile button/icon using locator.
        
        Opens profile menu or dropdown.
        """
        selectors = [
            f'{self.header_selector} [data-testid="user-profile"]',
            f'{self.header_selector} .profile-icon',
            f'{self.header_selector} button[aria-label*="Profile"]',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError("Could not find user profile button")
    
    def click_logout(self):
        """Click logout button using locator."""
        selectors = [
            f'{self.header_selector} [data-testid="logout"]',
            f'{self.header_selector} button:has-text("Logout")',
            f'{self.header_selector} button:has-text("Log Out")',
            f'{self.header_selector} a:has-text("Logout")',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError("Could not find logout button")
    
    def click_notifications(self):
        """Click notifications button/bell icon using locator."""
        selectors = [
            f'{self.header_selector} [data-testid="notifications"]',
            f'{self.header_selector} button[aria-label*="Notification"]',
            f'{self.header_selector} .notification-icon',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError("Could not find notifications button")
    
    def get_notification_count(self) -> str:
        """Get notification count badge using locator.
        
        Returns:
            Notification count as string
        """
        selectors = [
            f'{self.header_selector} [data-testid="notification-badge"]',
            f'{self.header_selector} .notification-count',
            f'{self.header_selector} .badge',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                return locator.text_content()
        
        return ""
    
    def search(self, query: str):
        """Use header search bar using locator.
        
        Args:
            query: Search query
        """
        selectors = [
            f'{self.header_selector} [data-testid="search"]',
            f'{self.header_selector} input[placeholder*="Search"]',
            f'{self.header_selector} .search-input',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.fill(query)
                return
        
        raise AssertionError("Could not find search input")
    
    def is_user_logged_in(self) -> bool:
        """Check if user is logged in (profile visible) using locator.
        
        Returns:
            True if profile visible
        """
        selectors = [
            f'{self.header_selector} [data-testid="user-profile"]',
            f'{self.header_selector} .user-profile',
        ]
        
        for selector in selectors:
            if self.page.locator(selector).is_visible():
                return True
        
        return False

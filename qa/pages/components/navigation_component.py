"""Navigation component for sidebar and menus using locators."""
from playwright.sync_api import Page
from .base_component import BaseComponent


class NavigationComponent(BaseComponent):
    """Reusable component for application navigation."""
    
    def __init__(self, page: Page, nav_selector: str = 'nav'):
        """Initialize navigation component.
        
        Args:
            page: Playwright Page instance
            nav_selector: CSS selector for navigation element
        """
        super().__init__(page, nav_selector)
        self.nav_selector = nav_selector
    
    def click_link(self, link_text: str):
        """Click navigation link by text using locator.
        
        Args:
            link_text: Link text
        """
        selectors = [
            f'{self.nav_selector} a:has-text("{link_text}")',
            f'{self.nav_selector} button:has-text("{link_text}")',
            f'{self.nav_selector} [data-testid="{link_text.lower()}-link"]',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
        
        raise AssertionError(f"Could not find navigation link: {link_text}")
    
    def is_link_active(self, link_text: str) -> bool:
        """Check if navigation link is active using locator.
        
        Args:
            link_text: Link text
            
        Returns:
            True if link is active
        """
        selectors = [
            f'{self.nav_selector} a:has-text("{link_text}").active',
            f'{self.nav_selector} a:has-text("{link_text}")[aria-current="page"]',
            f'{self.nav_selector} a.active:has-text("{link_text}")',
        ]
        
        for selector in selectors:
            if self.page.locator(selector).is_visible():
                return True
        
        return False
    
    def get_all_links(self) -> list:
        """Get all navigation link texts using locator.
        
        Returns:
            List of link texts
        """
        selector = f'{self.nav_selector} a'
        return self.page.locator(selector).all_text_contents()
    
    def is_link_visible(self, link_text: str) -> bool:
        """Check if navigation link is visible using locator.
        
        Args:
            link_text: Link text
            
        Returns:
            True if link is visible
        """
        selector = f'{self.nav_selector} a:has-text("{link_text}")'
        return self.page.locator(selector).is_visible()
    
    def click_menu_item(self, item_text: str):
        """Click menu item (supports nested items) using locator.
        
        Args:
            item_text: Menu item text
        """
        self.click_link(item_text)
    
    def expand_menu_section(self, section_text: str):
        """Expand collapsible menu section using locator.
        
        Args:
            section_text: Section header text
        """
        selectors = [
            f'{self.nav_selector} [data-testid="{section_text.lower()}-expand"]',
            f'{self.nav_selector} button:has-text("{section_text}")',
            f'{self.nav_selector} .menu-section:has-text("{section_text}")',
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.is_visible():
                locator.click()
                return
    
    def is_menu_expanded(self, section_text: str) -> bool:
        """Check if menu section is expanded using locator.
        
        Args:
            section_text: Section header text
            
        Returns:
            True if expanded
        """
        selectors = [
            f'{self.nav_selector} [data-testid="{section_text.lower()}-menu"].expanded',
            f'{self.nav_selector} .menu-section:has-text("{section_text}").open',
        ]
        
        for selector in selectors:
            if self.page.locator(selector).is_visible():
                return True
        
        return False

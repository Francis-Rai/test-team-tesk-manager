"""Base page class for Playwright page objects using locators."""
from playwright.sync_api import Page


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        """Initialize page object.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    def goto(self, url: str, wait_until: str = "load"):
        """Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_until: Wait condition (load, domcontentloaded, networkidle)
        """
        self.page.goto(url, wait_until=wait_until)
    
    def click(self, selector: str):
        """Click on element using locator.
        
        Args:
            selector: CSS selector for element
        """
        print("Clicking element with selector:", selector)
        self.page.locator(selector).click()

    def click_by_text(self, text: str):
        """Click element by text within component using locator.
        
        Args:
            text: Text of element to click
        """
        print("Clicking element with selector:", text)
        self.page.get_by_role("button", name=text).click()

    def fill(self, selector: str, text: str):
        """Fill input field with text using locator.
        
        Args:
            selector: CSS selector for input element
            text: Text to fill
        """
        self.page.locator(selector).fill(text)
    
    def get_text(self, selector: str) -> str:
        """Get text content of element using locator.
        
        Args:
            selector: CSS selector for element
            
        Returns:
            Text content
        """
        return self.page.locator(selector).text_content()
    
    def get_attribute(self, selector: str, attr: str) -> str:
        """Get attribute value of element using locator.
        
        Args:
            selector: CSS selector for element
            attr: Attribute name
            
        Returns:
            Attribute value
        """
        return self.page.locator(selector).get_attribute(attr)
    
    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Wait for element to appear using locator.
        
        Args:
            selector: CSS selector for element
            timeout: Timeout in milliseconds
        """
        self.page.locator(selector).wait_for(timeout=timeout)
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible using locator.
        
        Args:
            selector: CSS selector for element
            
        Returns:
            True if visible, False otherwise
        """
        return self.page.locator(selector).is_visible()
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled using locator.
        
        Args:
            selector: CSS selector for element
            
        Returns:
            True if enabled, False otherwise
        """
        return self.page.locator(selector).is_enabled()
    
    def get_count(self, selector: str) -> int:
        """Get count of elements using locator.
        
        Args:
            selector: CSS selector for element
            
        Returns:
            Count of elements
        """
        return self.page.locator(selector).count()
    
    def press_key(self, key: str):
        """Press keyboard key.
        
        Args:
            key: Key name (Enter, Tab, Escape, etc.)
        """
        self.page.keyboard.press(key)
    
    def wait_for_load_state(self, state: str = "networkidle"):
        """Wait for page load state.
        
        Args:
            state: Load state (load, domcontentloaded, networkidle)
        """
        self.page.wait_for_load_state(state)
    
    def wait_for_url(self, url: str, timeout: int = 5000):
        """Wait for page URL to match.
        
        Args:
            url: URL pattern or full URL
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_url(url, timeout=timeout)
    
    def take_screenshot(self, path: str):
        """Take screenshot.
        
        Args:
            path: Path to save screenshot
        """
        self.page.screenshot(path=path)

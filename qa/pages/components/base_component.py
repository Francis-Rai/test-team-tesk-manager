"""Base component class for all UI components using locators."""
from playwright.sync_api import Page


class BaseComponent:
    """Base class for all UI components in PCOM."""
    
    def __init__(self, page: Page, component_selector: str = None):
        """Initialize component.
        
        Args:
            page: Playwright Page instance
            component_selector: CSS selector for the component root element
        """
        self.page = page
        self.component_selector = component_selector
        # Create scoped locator for the component
        self.locator = page.locator(component_selector) if component_selector else page
    
    def _get_scoped_locator(self, child_selector: str):
        """Get scoped locator for child element.
        
        Args:
            child_selector: Child element selector
            
        Returns:
            Scoped locator
        """
        if self.component_selector:
            return self.page.locator(f'{self.component_selector} {child_selector}')
        return self.page.locator(child_selector)
    
    def click(self, selector: str):
        """Click element within component using locator.
        
        Args:
            selector: Element selector relative to component
        """
        self._get_scoped_locator(selector).click()
    
    def click_option(self, selector: str, option_text: str):
        """Click option from dropdown or menu within component using locator.
        
        Args:
            selector: Dropdown or menu selector relative to component
            option_text: Option text to click
        """
        dropdown_locator = self._get_scoped_locator(selector)
        dropdown_locator.click()  # Open the dropdown/menu
        
        # Click the option by text
        option_locator = self.page.locator(f'{selector} >> text="{option_text}"')
        if option_locator.is_visible():
            option_locator.click()
        else:
            raise AssertionError(f"Option '{option_text}' not found in '{selector}'")
    
    def fill(self, selector: str, text: str):
        """Fill input within component using locator.
        
        Args:
            selector: Input selector relative to component
            text: Text to fill
        """
        self._get_scoped_locator(selector).fill(text)
    
    def get_text(self, selector: str) -> str:
        """Get text from element within component using locator.
        
        Args:
            selector: Element selector relative to component
            
        Returns:
            Element text
        """
        return self._get_scoped_locator(selector).text_content()
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible within component using locator.
        
        Args:
            selector: Element selector relative to component
            
        Returns:
            True if visible
        """
        return self._get_scoped_locator(selector).is_visible()
    
    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Wait for element within component using locator.
        
        Args:
            selector: Element selector relative to component
            timeout: Timeout in milliseconds
        """
        self._get_scoped_locator(selector).wait_for(timeout=timeout)
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled within component using locator.
        
        Args:
            selector: Element selector relative to component
            
        Returns:
            True if enabled
        """
        return self._get_scoped_locator(selector).is_enabled()
    
    def get_attribute(self, selector: str, attr: str) -> str:
        """Get attribute from element within component using locator.
        
        Args:
            selector: Element selector relative to component
            attr: Attribute name
            
        Returns:
            Attribute value
        """
        return self._get_scoped_locator(selector).get_attribute(attr)
    
    def get_count(self, selector: str) -> int:
        """Get count of elements within component using locator.
        
        Args:
            selector: Element selector relative to component
            
        Returns:
            Count of elements
        """
        return self._get_scoped_locator(selector).count()

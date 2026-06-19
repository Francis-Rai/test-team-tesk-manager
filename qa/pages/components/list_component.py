"""List component for handling lists, tables, and grids using locators."""
from playwright.sync_api import Page
from .base_component import BaseComponent


class ListComponent(BaseComponent):
    """Reusable component for handling lists, tables, and grids."""
    
    def __init__(self, page: Page, list_selector: str, item_selector: str = None):
        """Initialize list component.
        
        Args:
            page: Playwright Page instance
            list_selector: CSS selector for the list container
            item_selector: CSS selector for individual list items
        """
        super().__init__(page, list_selector)
        self.list_selector = list_selector
        self.item_selector = item_selector or 'li'  # Default to li elements
    
    def _get_items_locator(self):
        """Get locator for all items in list.
        
        Returns:
            Locator for items
        """
        return self.page.locator(f'{self.list_selector} {self.item_selector}')
    
    def get_item_count(self) -> int:
        """Get number of items in list using locator.
        
        Returns:
            Count of items
        """
        return self._get_items_locator().count()
    
    def get_item_text(self, index: int) -> str:
        """Get text of item at index using locator.
        
        Args:
            index: Zero-based item index
            
        Returns:
            Item text
        """
        return self._get_items_locator().nth(index).text_content()
    
    def click_item(self, index: int):
        """Click item at index using locator.
        
        Args:
            index: Zero-based item index
        """
        locator = self._get_items_locator().nth(index)
        if locator.is_visible():
            locator.click()
        else:
            raise IndexError(f"Item {index} not found or not visible in list")
    
    def click_item_by_text(self, text: str):
        """Click item by text content using locator.
        
        Args:
            text: Text to search for
        """
        selector = f'{self.list_selector} {self.item_selector}:has-text("{text}")'
        self.page.locator(selector).click()
    
    def find_item_by_text(self, text: str) -> bool:
        """Check if item with text exists using locator.
        
        Args:
            text: Text to search for
            
        Returns:
            True if found
        """
        selector = f'{self.list_selector} {self.item_selector}:has-text("{text}")'
        return self.page.locator(selector).is_visible()
    
    def get_all_item_texts(self) -> list:
        """Get text of all items using locator.
        
        Returns:
            List of item texts
        """
        locator = self._get_items_locator()
        return locator.all_text_contents()
    
    def is_empty(self) -> bool:
        """Check if list is empty using locator.
        
        Returns:
            True if list has no items
        """
        return self.get_item_count() == 0
    
    def wait_for_items(self, timeout: int = 5000):
        """Wait for list items to appear using locator.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self._get_items_locator().first.wait_for(timeout=timeout)
    
    def filter_items(self, filter_selector: str, filter_value: str):
        """Filter list by criteria using locator.
        
        Args:
            filter_selector: Selector for filter control
            filter_value: Value to filter by
        """
        self.page.locator(filter_selector).click()
        self.page.locator(f'text="{filter_value}"').click()
        self.wait_for_items()
    
    def sort_items(self, sort_selector: str):
        """Sort list by clicking sort button using locator.
        
        Args:
            sort_selector: Selector for sort control
        """
        self.page.locator(sort_selector).click()
        self.wait_for_items()

"""Projects page using PCOM."""
from playwright.sync_api import Page
from qa.pages.base_page import BasePage
from qa.pages.components import (
    FormComponent,
    ListComponent,
    ModalComponent,
    HeaderComponent,
    NavigationComponent,
)


class ProjectsPage(BasePage):
    """Projects page with multiple components."""
    
    # Component selectors
    HEADER_SELECTOR = 'header'
    NAV_SELECTOR = 'nav'
    PROJECT_LIST_SELECTOR = '[data-testid="projects-list"], .projects-list'
    PROJECT_ITEM_SELECTOR = '[data-testid="project-item"], .project-item'
    CREATE_PROJECT_MODAL = '[data-testid="create-project-modal"], .modal'
    
    def __init__(self, page: Page):
        """Initialize projects page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        
        # Initialize components
        self.header = HeaderComponent(page, self.HEADER_SELECTOR)
        self.nav = NavigationComponent(page, self.NAV_SELECTOR)
        self.project_list = ListComponent(
            page, 
            self.PROJECT_LIST_SELECTOR,
            self.PROJECT_ITEM_SELECTOR
        )
        self.create_modal = ModalComponent(page, self.CREATE_PROJECT_MODAL)
    
    def get_project_count(self) -> int:
        """Get number of projects displayed.
        
        Returns:
            Project count
        """
        return self.project_list.get_item_count()
    
    def open_project(self, project_name: str):
        """Open project by name.
        
        Args:
            project_name: Project name
        """
        self.project_list.click_item_by_text(project_name)
        self.wait_for_load_state("networkidle")
    
    def create_project(self, name: str, description: str = ""):
        """Create new project via modal.
        
        Args:
            name: Project name
            description: Project description
        """
        # Open create modal
        self.click('button:has-text("Create Project"), [data-testid="create-project-btn"]')
        self.create_modal.wait_for_open()
        
        # Fill form
        self.create_modal.fill_form_field("name", name)
        if description:
            self.create_modal.fill_form_field("description", description)
        
        # Submit
        self.create_modal.confirm()
        self.create_modal.wait_for_close()
        self.wait_for_load_state("networkidle")
    
    def is_project_visible(self, project_name: str) -> bool:
        """Check if project is visible in list.
        
        Args:
            project_name: Project name
            
        Returns:
            True if project is visible
        """
        return self.project_list.find_item_by_text(project_name)
    
    def get_all_projects(self) -> list:
        """Get all project names.
        
        Returns:
            List of project names
        """
        return self.project_list.get_all_item_texts()
    
    def filter_projects(self, filter_name: str):
        """Filter projects by category.
        
        Args:
            filter_name: Filter name
        """
        self.project_list.filter_items(
            '[data-testid="project-filter"]',
            filter_name
        )
    
    def logout(self):
        """Logout via header.
        
        Args:
            None
        """
        self.header.click_user_profile()
        self.header.click_logout()

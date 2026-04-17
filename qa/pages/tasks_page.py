"""Tasks page using PCOM."""
from playwright.sync_api import Page
from qa.pages.base_page import BasePage
from qa.pages.components import (
    FormComponent,
    ListComponent,
    ModalComponent,
    HeaderComponent,
)


class TasksPage(BasePage):
    """Tasks page with components for task management."""
    
    # Component selectors
    HEADER_SELECTOR = 'header'
    TASK_LIST_SELECTOR = '[data-testid="tasks-list"], .tasks-list'
    TASK_ITEM_SELECTOR = '[data-testid="task-item"], .task-item'
    CREATE_TASK_MODAL = '[data-testid="create-task-modal"], .modal'
    TASK_DETAILS_MODAL = '[data-testid="task-details-modal"], .task-details'
    
    def __init__(self, page: Page):
        """Initialize tasks page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        
        # Initialize components
        self.header = HeaderComponent(page, self.HEADER_SELECTOR)
        self.task_list = ListComponent(
            page,
            self.TASK_LIST_SELECTOR,
            self.TASK_ITEM_SELECTOR
        )
        self.create_modal = ModalComponent(page, self.CREATE_TASK_MODAL)
        self.details_modal = ModalComponent(page, self.TASK_DETAILS_MODAL)
    
    def get_task_count(self) -> int:
        """Get number of tasks displayed.
        
        Returns:
            Task count
        """
        return self.task_list.get_item_count()
    
    def get_all_tasks(self) -> list:
        """Get all task titles.
        
        Returns:
            List of task titles
        """
        return self.task_list.get_all_item_texts()
    
    def open_task(self, task_name: str):
        """Open task by name.
        
        Args:
            task_name: Task name
        """
        self.task_list.click_item_by_text(task_name)
        self.details_modal.wait_for_open()
    
    def create_task(self, title: str, description: str = "", assignee: str = ""):
        """Create new task.
        
        Args:
            title: Task title
            description: Task description
            assignee: Assign to team member
        """
        # Open create modal
        self.click('button:has-text("Create Task"), [data-testid="create-task-btn"]')
        self.create_modal.wait_for_open()
        
        # Fill form
        self.create_modal.fill_form_field("title", title)
        if description:
            self.create_modal.fill_form_field("description", description)
        if assignee:
            self.create_modal.fill_form_field("assignee", assignee)
        
        # Submit
        self.create_modal.confirm()
        self.create_modal.wait_for_close()
        self.wait_for_load_state("networkidle")
    
    def change_task_status(self, task_name: str, new_status: str):
        """Change task status.
        
        Args:
            task_name: Task name
            new_status: New status (To Do, In Progress, Done)
        """
        self.open_task(task_name)
        
        # Click status dropdown and select new status
        self.click('[data-testid="task-status"]')
        self.click(f'[data-testid="status-{new_status.lower().replace(" ", "-")}"]')
        
        self.details_modal.wait_for_close()
    
    def assign_task(self, task_name: str, assignee: str):
        """Assign task to team member.
        
        Args:
            task_name: Task name
            assignee: Team member name
        """
        self.open_task(task_name)
        
        # Click assign button
        self.click('[data-testid="assign-btn"]')
        
        # Select assignee
        self.click(f'[data-testid="assignee-{assignee.lower()}"]')
        
        self.details_modal.wait_for_close()
    
    def is_task_visible(self, task_name: str) -> bool:
        """Check if task is visible.
        
        Args:
            task_name: Task name
            
        Returns:
            True if task is visible
        """
        return self.task_list.find_item_by_text(task_name)
    
    def filter_tasks_by_status(self, status: str):
        """Filter tasks by status.
        
        Args:
            status: Status to filter (To Do, In Progress, Done)
        """
        self.task_list.filter_items(
            '[data-testid="status-filter"]',
            status
        )
    
    def delete_task(self, task_name: str):
        """Delete a task.
        
        Args:
            task_name: Task name
        """
        self.open_task(task_name)
        
        # Click delete button
        self.click('[data-testid="delete-btn"], button:has-text("Delete")')
        
        # Confirm delete in confirmation modal
        self.click('button:has-text("Confirm"), button:has-text("Yes")')
        
        self.details_modal.wait_for_close()
        self.wait_for_load_state("networkidle")

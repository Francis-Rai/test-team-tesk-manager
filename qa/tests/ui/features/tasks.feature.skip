Feature: Task Management

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskCreation
  @allure.label.tag:bdd
  Scenario: User can create a task in a project
    Given the user is logged in and in a project
    When the user clicks "Create Task"
    And the user enters task title and description
    And the user sets a due date
    And the user submits the form
    Then the task should be created successfully
    And the task should appear in the project's task list
    And the task should have a default status of "To Do"
    And the creator should be automatically recorded

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskAssignment
  @allure.label.tag:bdd
  Scenario: User can assign task to team members
    Given the user is in a project with team members
    And a task exists
    When the user opens the task details
    And the user clicks "Assign To"
    And the user selects a team member
    Then the task should be assigned to the selected member
    And the assignee should see the task in their task list
    And the assignment should be timestamped

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskDetails
  @allure.label.tag:bdd
  Scenario: Task details page displays all information
    Given tasks exist with descriptions, assignees, and due dates
    When the user opens a task
    Then the task title should be displayed
    And the task description should be shown
    And the assignee name should be visible
    And the due date should be displayed
    And the task status should be shown
    And the creation date should be present

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskFiltering
  @allure.label.tag:bdd
  Scenario: Users can filter tasks by various criteria
    Given a project has tasks with different statuses and assignees
    When the user filters by status "In Progress"
    Then only tasks with "In Progress" status should be displayed
    When the user adds a filter for assignee
    Then tasks should be filtered by both status and assignee
    When the user clears filters
    Then all tasks should be displayed again

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskStatus
  @allure.label.tag:bdd
  Scenario: User can update task status
    Given a task exists with status "To Do"
    When the user opens the task
    And the user changes the status to "In Progress"
    Then the status should be updated immediately
    And the change should be reflected in the task list
    And the status change timestamp should be recorded

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskList
  @allure.label.tag:bdd
  Scenario: Different users see their assigned tasks
    Given multiple users are in a team
    And tasks are assigned to different users
    When user A views their task list
    Then user A should see only their assigned tasks
    When user B views their task list
    Then user B should see only their assigned tasks

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskDeletion
  @allure.label.tag:bdd
  Scenario: Task creator or owner can delete a task
    Given the user is logged in
    And the user has created a task
    When the user opens the task
    And the user clicks "Delete Task"
    And the user confirms the deletion
    Then the task should be removed from the system
    And the task should no longer appear in the task list

  @allure.label.suite:Tasks
  @allure.label.subSuite:TaskPriority
  @allure.label.tag:bdd
  Scenario: User can set and view task priority
    Given the user is creating a new task
    When the user sets the priority to "High"
    And the user submits the task
    Then the task should be created with "High" priority
    And the priority should be visible in the task list
    And high priority tasks can be filtered separately

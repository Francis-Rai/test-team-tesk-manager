Feature: Project Management

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectList
  @allure.label.tag:bdd
  Scenario: User can view all projects in the team
    Given the user is logged in
    And the team has multiple projects
    When the user navigates to the projects page
    Then all projects should be displayed in a list
    And each project should show its name and description
    And projects should be clickable to view details
    And project count should match the actual number

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectCreation
  @allure.label.tag:bdd
  Scenario: User can create a new project
    Given the user is logged in in a team
    When the user clicks "Create Project"
    And the user enters a project name
    And the user enters a project description
    And the user submits the form
    Then the project should be created successfully
    And the project should appear in the projects list
    And the user should be the project owner
    And the creation timestamp should be recorded

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectDetails
  @allure.label.tag:bdd
  Scenario: User can view complete project details
    Given projects exist with descriptions and creation dates
    When the user opens a project
    Then the project name should be displayed
    And the project description should be shown
    And project members should be listed
    And the project creation date should be visible
    And the project owner should be identified

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectTasks
  @allure.label.tag:bdd
  Scenario: User can view tasks aggregated by project
    Given a project has multiple tasks
    When the user opens the project
    Then all tasks should be displayed grouped by status
    And task count should match the actual number
    And users should be able to filter tasks by status

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectAccess
  @allure.label.tag:bdd
  Scenario: Only team members can access team projects
    Given the user is not part of a team
    When the user tries to access that team's projects
    Then an access denied message should be shown
    And the projects list should not load
    And the user should be redirected to their own teams

  @allure.label.suite:Projects
  @allure.label.subSuite:ProjectUpdate
  @allure.label.tag:bdd
  Scenario: Project owner can update project details
    Given the user is logged in as project owner
    When the user opens the project details
    And the user edits the project description
    And the user saves the changes
    Then the project description should be updated
    And the change should be reflected immediately
    And the modification timestamp should be updated

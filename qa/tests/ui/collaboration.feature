Feature: Team Collaboration and Updates

  @allure.label.suite:Collaboration
  @allure.label.subSuite:RealTimeUpdates
  @allure.label.tag:bdd
  Scenario: Multiple users see real-time task status updates
    Given task is assigned to user A
    And user B is viewing the same project's task list
    When user A marks their task as "Complete"
    Then user B should see the status update within a few seconds
    And the task should move to the completed section
    And both users should see the same final state

  @allure.label.suite:Collaboration
  @allure.label.subSuite:Comments
  @allure.label.tag:bdd
  Scenario: Users can comment on tasks
    Given the user is logged in
    And a task exists
    When the user opens the task
    And the user adds a comment
    And the user submits the comment
    Then the comment should appear in the task
    And the commenter name should be displayed
    And the comment timestamp should be recorded

  @allure.label.suite:Collaboration
  @allure.label.subSuite:Notifications
  @allure.label.tag:bdd
  Scenario: User receives notification when assigned to task
    Given the user is in a team
    When another user assigns them to a task
    Then a notification should appear in the notification center
    And the user should see the task in their assigned tasks
    And the notification should include the task name and assigner

  @allure.label.suite:Collaboration
  @allure.label.subSuite:TeamActivity
  @allure.label.tag:bdd
  Scenario: Team can view activity feed of all members
    Given the team has multiple members
    When multiple users perform actions (create tasks, update status, etc.)
    Then the activity feed should display all actions
    And each action should show the user who performed it
    And actions should be timestamped and sorted chronologically
    And activity should include task creation, status changes, and assignments

  @allure.label.suite:Collaboration
  @allure.label.subSuite:Mentions
  @allure.label.tag:bdd
  Scenario: User can mention team members in task descriptions
    Given the user is creating or editing a task
    When the user types @ and starts typing a member name
    Then available members should be suggested
    When the user selects a member
    Then the member should be mentioned with their name highlighted
    And the mentioned user should receive a notification

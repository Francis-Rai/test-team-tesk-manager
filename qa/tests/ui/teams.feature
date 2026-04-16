Feature: Team Management

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamSelection
  @allure.label.tag:bdd
  Scenario: User can switch between multiple teams
    Given the user is logged in
    And the user belongs to multiple teams
    When the user opens the team selector
    Then all user teams should be displayed
    When the user selects a different team
    Then the page should update with the selected team's data
    And the navigation breadcrumb should reflect the current team
    And the team name should be displayed in the header

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamCreation
  @allure.label.tag:bdd
  Scenario: User can create a new team
    Given the user is logged in
    When the user navigates to create team option
    And the user enters a team name
    And the user submits the team creation form
    Then a new team should be created
    And the team should appear in the team list
    And the user should automatically switch to the new team
    And the user should be the team owner

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamMembers
  @allure.label.tag:bdd
  Scenario: Team owner can invite members to the team
    Given the user is logged in as a team owner
    And the user is in a team
    When the user navigates to team settings
    And the user clicks "Invite Members"
    And the user enters a member email
    And the user sends the invitation
    Then an invitation should be sent to the email
    And the member should appear as "Pending" in the team members list
    And the team owner should see the invitation status

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamMembers
  @allure.label.tag:bdd
  Scenario: Regular member cannot manage team settings
    Given the user is logged in as a regular team member
    When the user navigates to team settings
    Then the "Manage Members" button should not be visible
    And the user should see read-only information
    And the user cannot access member management page

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamMembers
  @allure.label.tag:bdd
  Scenario: User can view all team members with roles
    Given the user is in a team with multiple members
    When the user navigates to the team members page
    Then all members should be displayed with their names
    And each member should show their role (Owner, Manager, Member)
    And the current user should be highlighted
    And member count should be accurate

  @allure.label.suite:Teams
  @allure.label.subSuite:TeamActivity
  @allure.label.tag:bdd
  Scenario: Team activity feed displays recent actions
    Given the user is in a team with activity
    When the user navigates to the team activity page
    Then recent activities should be displayed with timestamps
    And activities should include user names and actions performed
    And the feed should be sorted in reverse chronological order

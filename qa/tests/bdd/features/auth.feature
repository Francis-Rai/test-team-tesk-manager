Feature: Authentication

  @allure.label.suite:Authentication
  @allure.label.subSuite:Login
  @allure.label.tag:bdd
  Scenario: Successful login
    Given a registered user exists
    When the user logs in with valid credentials
    Then the login should be successful

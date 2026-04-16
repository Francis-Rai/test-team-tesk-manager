@allure.label.suite:User
@allure.label.tag:api
@allure.label.tag:integration
Feature: User

@fixture.create_user
Scenario: Super Admin user cannot access admin resources after role is downgraded to user
  Given a user is registered with role "SUPER_ADMIN"
  When the user accesses a "SUPER_ADMIN"-only endpoint
  Then the API should return a successful response
  When the user's role is updated to "USER"
  And the user accesses a "SUPER_ADMIN"-only endpoint
  Then the API should be forbidden

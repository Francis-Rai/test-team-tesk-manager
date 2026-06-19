@allure.label.suite:User
@allure.label.tag:ui
Feature: User Authentication

Scenario: User can register, log in and log out
  Given the user is on the login page
  When the user clicks on "Sign Up"
  And the user enters valid registration details and submits the form
  Then the login form should be displayed and pre-filled
  When the user clicks on "Login"
  Then the user should be redirected to the "teams" page
  When the user clicks on the user menu in the header and selects "Logout"
  Then the user should be redirected to the "login" page

# Scenario: User sees error on invalid login
#   Given the user is on the login page
#   When the user enters invalid credentials and clicks "Login"
#   Then an error message should be displayed
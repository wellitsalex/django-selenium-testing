Feature: Test navigation between pages


Scenario: Welcome page can go to login page
    Given I am on the welcome page
    When I click on the link with href "/login/"
    Then I am on the login page

Scenario: Welcome page can go to register page
    Given I am on the welcome page
    When I click on the link with href "/register/"
    Then I am on the register page

Scenario: Login page can go to welcome page
    Given I am on the login page
    When I click on the link with href "/"
    Then I am on the welcome page

Scenario: A user not logged accessing the dashboard page gets redirected to login page
    Given I am on the welcome page
    When I click on the link with href "/dashboard/"
    Then I am on the login page with next to dashboard

Scenario: A user not logged accessing the profile page gets redirected to login page
    Given I am on the welcome page
    When I click on the link with href "/profile/"
    Then I am on the login page with next to profile


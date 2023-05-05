Feature: Test that pages have the correct functionality

Scenario: A User can login
    Given I am on the login page
    When I enter "testuser" in the "id_username" field
    And I enter "testpass!" in the "id_password" field
    And I press the login button
    Then I am on the dashboard page


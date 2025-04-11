Feature: Streamer
  As a user, I want to be able to select an streamer

  @smoke @brand-p0
  Scenario: Verify select and load a streamer
    Given I load the web without login
    And I click on search icon
    And I input 'StarCraft II'
    And I select one streamer
    Then Verify the streamer page is successfully loaded

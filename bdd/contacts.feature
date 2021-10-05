Scenario Outline: Add new contact
    Given a contact list
    Given a contact with <firstname>, <lastname> and <middlename>
    When I add the contact to the list
    Then the new contact list is equal to the old list with the added contact

    Examples:
    | firstname | lastname | middlename |
    | firstname1 | lastname1 | midlename1 |
    | firstname2 | lastname2 | middlename2 |

Scenario: Delete a contact
    Given a non-empty contact list
    Given a random from the list
    When I delete the contact from the list
    Then the new contact list is equal to the old contact list without the delete contact
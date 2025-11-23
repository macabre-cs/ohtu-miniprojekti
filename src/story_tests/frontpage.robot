*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset References

*** Test Cases ***
Main Page Should Be Open
    Go To  ${HOME_URL}
    Title Should Be  References app

Main Page Should Contain Create New Reference Link
    Go To  ${HOME_URL}
    Page Should Contain Link  Create new reference

Clicking Create New Reference Link Opens Create Reference Page
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Title Should Be  Create a new reference
    Page Should Contain  Create a new reference

Main Page Should Contain Existing References
	Go To    ${HOME_URL}
	Click Link    Create new reference

	Select From List By Value    name=reference_type    book
	Input Text    name=cite_key    BOOK1
	Input Text    name=title       Book Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
	Input Text    name=publisher   Publisher
	Input Text    name=chapter     55
    
	Click Button    Create

    Page Should Contain    BOOK1

    Go To  ${HOME_URL}
    Page Should Contain  BOOK1
    Page Should Contain  Book Title
    Page Should Contain  Smith, Alice
    Page Should Contain  2010
    Page Should Contain  Publisher
    Page Should Contain  55

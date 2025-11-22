*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Edit Book Reference Updates Fields
	Go To    ${HOME_URL}
	Click Link    Create new reference

	Select From List By Value    name=reference_type    book
	Input Text    name=cite_key    BOOK1
	Input Text    name=title       Original Book Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
	Input Text    name=publisher   Original Publisher
	Input Text    name=chapter     1
    
	Click Button    Create

	Page Should Contain    Original Book Title
	Click Element    xpath=//a[contains(., "Original Book Title")]

	Click Element    xpath=//a[contains(@href, "/edit")]

	Input Text    name=title    Updated Book Title

	Click Button    id=add-author
	Input Text    xpath=(//input[@name='authors'])[2]    Doe, John

	Input Text    name=year    2021
	Input Text    name=publisher    Updated Publisher

	Click Button    Save

	Page Should Contain    Updated Book Title
    Page Should Contain    2021
    Page Should Contain    Smith, Alice
    Page Should Contain    Doe, John


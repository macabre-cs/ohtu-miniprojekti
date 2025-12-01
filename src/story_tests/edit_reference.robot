*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Edit Book Reference Updates Fields
	Go To    ${HOME_URL}
	Click Button    Create a new reference

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

	Click Button   Edit reference

    Input Text    name=cite_key    BOOK2
	Input Text    name=title    Updated Book Title

	Click Button    id=add-author
	Input Text    xpath=(//input[@name='authors'])[2]    Doe, John

	Input Text    name=year    2021
	Input Text    name=publisher    Updated Publisher
	Input Text    name=chapter    55

	Click Button    Save

    Page Should Contain    BOOK2
	Page Should Contain    Updated Book Title
    Page Should Contain    2021
    Page Should Contain    Smith, Alice
    Page Should Contain    Doe, John
	Page Should Contain    Updated Publisher
	Page Should Contain	   55

Edit Article Reference Updates Fields
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    article
	Input Text    name=cite_key    ART1
	Input Text    name=title       Original Article Title
	Input Text    name=authors    Brown, Charlie
	Input Text    name=year      2015
	Input Text    name=journal     Original Journal
	Input Text    name=volume      10
	Input Text    name=pages       100-110

	Click Button    Create

	Page Should Contain    Original Article Title
	Click Element    xpath=//a[contains(., "Original Article Title")]

	Click Button	Edit reference

    Input Text    name=cite_key    ART2
	Input Text    name=title    Updated Article Title

	Click Button    id=add-author
	Input Text    xpath=(//input[@name='authors'])[2]    Green, Lucy

	Input Text    name=year    2022
	Input Text    name=journal    Updated Journal
	Input Text    name=volume    55
	Input Text    name=pages    200-220

	Click Button    Save

	Page Should Contain    ART2
	Page Should Contain    Updated Article Title
	Page Should Contain    2022
	Page Should Contain    Brown, Charlie
	Page Should Contain    Green, Lucy
	Page Should Contain    Updated Journal
	Page Should Contain    55
	Page Should Contain    200-220

Edit Inproceedings Reference Updates Fields
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    inproceedings
	Input Text    name=cite_key    INPRO1
	Input Text    name=title       Original Inproceedings Title
	Input Text    name=authors    White, David
	Input Text    name=year      2018
	Input Text    name=booktitle   Original Booktitle

	Click Button    Create

	Page Should Contain    Original Inproceedings Title
	Click Element    xpath=//a[contains(., "Original Inproceedings Title")]
	Click Button	Edit reference

	Input Text    name=cite_key    INPRO2
	Input Text    name=title    Updated Inproceedings Title

	Click Button    id=add-author
	Input Text    xpath=(//input[@name='authors'])[2]    Black, Emma
	Input Text    name=year    2023
	Input Text    name=booktitle    Updated Booktitle

	Click Button    Save
	
	Page Should Contain    INPRO2
	Page Should Contain    Updated Inproceedings Title
	Page Should Contain    2023
	Page Should Contain    White, David
	Page Should Contain    Black, Emma
	Page Should Contain    Updated Booktitle

Edit Misc Reference Updates Fields
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    misc
	Input Text    name=cite_key    MISC1
	Input Text    name=title       Original Misc Title
	Input Text    name=authors    White, David
	Input Text    name=year      2018
	Input Text    name=url   https://example.com

	Click Button    Create

	Page Should Contain    Original Misc Title
	Click Element    xpath=//a[contains(., "Original Misc Title")]
	Click Button	Edit reference

	Input Text    name=cite_key    MISC2
	Input Text    name=title    Updated Misc Title

	Click Button    id=add-author
	Input Text    xpath=(//input[@name='authors'])[2]    Black, Emma
	Input Text    name=year    2023
	Input Text    name=url    https://updated.example.com

	Click Button    Save

	Page Should Contain    MISC2
	Page Should Contain    Updated Misc Title
	Page Should Contain    2023
	Page Should Contain    White, David
	Page Should Contain    Black, Emma
	Page Should Contain    https://updated.example.com
*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Create Book Reference Successfully
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    book
	Input Text    name=cite_key    BOOK1
	Input Text    name=title       Book Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
	Input Text    name=publisher   Publisher
	Input Text    name=chapter     55
    
	Click Button    Create

    Page Should Contain    BOOK1
	Page Should Contain    Book Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Publisher
    Page Should Contain    55

Create Article Reference Successfully
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    article
	Input Text    name=cite_key    ARTICLE1
	Input Text    name=title       Article Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
	Input Text    name=journal   Journal Name
	Input Text    name=volume     111
    Input Text    name=pages     222-333
    
	Click Button    Create

    Page Should Contain    ARTICLE1
	Page Should Contain    Article Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Journal Name
    Page Should Contain    111
    Page Should Contain    222-333

Create Inproceedings Reference Successfully
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    inproceedings
	Input Text    name=cite_key    INPROCEEDINGS1
	Input Text    name=title       Inproceedings Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
    Input Text    name=booktitle   Conference Name

	Click Button    Create

    Page Should Contain    INPROCEEDINGS1
	Page Should Contain    Inproceedings Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Conference Name

Create Misc Reference Successfully
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    misc
	Input Text    name=cite_key    MISC1
	Input Text    name=title       Misc Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
    Input Text    name=url       https://example.com

	Click Button    Create

    Page Should Contain    MISC1
	Page Should Contain    Misc Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    https://example.com
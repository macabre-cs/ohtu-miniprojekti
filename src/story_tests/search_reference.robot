*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Search Reference by Partial Word Written in Lowercase
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

    Click Button    Search references

    Input Text    name=query    smi

    Click Button    Search
    
    Page Should Contain    BOOK1
	Page Should Contain    Book Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Publisher
    Page Should Contain    55

Search Reference by Partial Word Written in Uppercase
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

    Click Button    Search references

    Input Text    name=query    ICE

    Click Button    Search
    
    Page Should Contain    BOOK1
	Page Should Contain    Book Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Publisher
    Page Should Contain    55

Search No Match
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

    Go To    ${HOME_URL}
    Click Button    Search references
    Input Text    name=query    Alise
    Click Button    Search
    Page Should Contain    Search results: 0
    
Search Returns Multiple Results
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

    Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    inproceedings
	Input Text    name=cite_key    INPROCEEDINGS1
	Input Text    name=title       Inproceedings Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
    Input Text    name=booktitle   Conference Name

	Click Button    Create

    Go To    ${HOME_URL}
    Click Button    Search references
    Input Text    name=query    Smith
    Click Button    Search

    Page Should Contain    Search results: 2
    Page Should Contain    BOOK1
	Page Should Contain    Book Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Publisher
    Page Should Contain    55

    Page Should Contain    INPROCEEDINGS1
	Page Should Contain    Inproceedings Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Conference Name


Advanced Search Returns Correct Result
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

    Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    inproceedings
	Input Text    name=cite_key    INPROCEEDINGS1
	Input Text    name=title       Inproceedings Title
	Input Text    name=authors    Smith, Alice
	Input Text    name=year      2010
    Input Text    name=booktitle   Conference Name

	Click Button    Create

    Go To    ${HOME_URL}
    Click Button    Search references
	Click Button    Switch to Advanced Search

    Input Text    name=title    Book
    Input Text    name=author    Alice
    Select From List By Value    name=reference_type    book
    Input Text    name=year_from    2009
    Input Text    name=year_to    2011
    Input Text    name=cite_key    BOOK
    Input Text    name=publisher    Publisher
    Click Button    Search

    Page Should Contain    Search results: 1
    Page Should Contain    BOOK1
	Page Should Contain    Book Title
    Page Should Contain    Smith, Alice
    Page Should Contain    2010
    Page Should Contain    Publisher
    Page Should Contain    55

    Page Should Not Contain    INPROCEEDINGS1
	Page Should Not Contain    Inproceedings Title
    Page Should Not Contain    Conference Name

*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Export Bibtex Successfully
	Go To    ${HOME_URL}
	Click Button    Create a new reference

	Select From List By Value    name=reference_type    book
	Input Text    name=cite_key    Citekey1
	Input Text    name=title    Book Title 1
	Input Text    name=authors    Martin, Robert
	Input Text    name=year    2015
	Input Text    name=publisher    Publisher 1
	Input Text    name=chapter    6
    
	Click Button    Create

    Click Element    id=checkbox-1

    Click Button    Export BibTeX

    Page Should Contain    Preview BibTeX Export
    Page Should Contain    @book
    Page Should Contain    Citekey1
    Page Should Contain    title = {Book Title 1}
    Page Should Contain    author = {Robert Martin}
    Page Should Contain    year = {2015}
    Page Should Contain    publisher = {Publisher 1}

    Page Should Contain Button    Download BibTeX File



Export Correct Selected References
    Go To    ${HOME_URL}
    
    Click Button    Create a new reference
    Select From List By Value    name=reference_type    book
    Input Text    name=cite_key    BookKey1
    Input Text    name=title    Clean Code
    Input Text    name=authors    Martin, Robert
    Input Text    name=year    2008
    Input Text    name=publisher    Prentice Hall
    Click Button    Create


    Click Button    Create a new reference
    Select From List By Value    name=reference_type    article
    Input Text    name=cite_key    ArticleKey1
    Input Text    name=title    Test Driven Development
    Input Text    name=authors    Beck, Kent
    Input Text    name=year    2003
    Input Text    name=journal    Software Engineering Journal
    Click Button    Create


    Click Button    Create a new reference
    Select From List By Value    name=reference_type    book
    Input Text    name=cite_key    BookKey2
    Input Text    name=title    Design Patterns
    Input Text    name=authors    Gamma, Erich
    Input Text    name=year    1994
    Input Text    name=publisher    Addison-Wesley
    Click Button    Create
    
    Click Element    id=checkbox-1
    Click Element    id=checkbox-2
    
    Click Button    Export BibTeX
    
    Page Should Contain    Preview BibTeX Export
    
    Page Should Contain    @book
    Page Should Contain    BookKey1
    Page Should Contain    title = {Clean Code}
    Page Should Contain    author = {Robert Martin}
    Page Should Contain    year = {2008}
    Page Should Contain    publisher = {Prentice Hall}
    
    Page Should Contain    @article
    Page Should Contain    ArticleKey1
    Page Should Contain    title = {Test Driven Development}
    Page Should Contain    author = {Kent Beck}
    Page Should Contain    year = {2003}
    Page Should Contain    journal = {Software Engineering Journal}
    
    Page Should Not Contain    BookKey2
    Page Should Not Contain    Design Patterns
    Page Should Not Contain    Erich Gamma
    Page Should Not Contain    1994
    
    Page Should Contain Button    Download BibTeX File


Export All Checkbox Selects All
    Go To    ${HOME_URL}
    
    Click Button    Create a new reference
    Select From List By Value    name=reference_type    book
    Input Text    name=cite_key    BookKey1
    Input Text    name=title    Clean Code
    Input Text    name=authors    Martin, Robert
    Input Text    name=year    2008
    Input Text    name=publisher    Prentice Hall
    Click Button    Create


    Click Button    Create a new reference
    Select From List By Value    name=reference_type    article
    Input Text    name=cite_key    ArticleKey1
    Input Text    name=title    Test Driven Development
    Input Text    name=authors    Beck, Kent
    Input Text    name=year    2003
    Input Text    name=journal    Software Engineering Journal
    Click Button    Create


    Click Button    Create a new reference
    Select From List By Value    name=reference_type    book
    Input Text    name=cite_key    BookKey2
    Input Text    name=title    Design Patterns
    Input Text    name=authors    Gamma, Erich
    Input Text    name=year    1994
    Input Text    name=publisher    Addison-Wesley
    Click Button    Create
    
    Click Element    id=select-all
    
    Click Button    Export BibTeX
    
    Page Should Contain    Preview BibTeX Export
    
    Page Should Contain    @book
    Page Should Contain    BookKey1
    Page Should Contain    title = {Clean Code}
    Page Should Contain    author = {Robert Martin}
    Page Should Contain    year = {2008}
    Page Should Contain    publisher = {Prentice Hall}
    
    Page Should Contain    @article
    Page Should Contain    ArticleKey1
    Page Should Contain    title = {Test Driven Development}
    Page Should Contain    author = {Kent Beck}
    Page Should Contain    year = {2003}
    Page Should Contain    journal = {Software Engineering Journal}
    
    Page Should Contain    BookKey2
    Page Should Contain    Design Patterns
    Page Should Contain    Erich Gamma
    Page Should Contain    1994
    
    Page Should Contain Button    Download BibTeX File

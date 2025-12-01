*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
DOI Lookup Prefills New Reference
    Go To    ${HOME_URL}/new_reference?doi=10.9999/testdoi
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Article Title
    Textfield Value Should Be    xpath=(//input[@name='authors'])[1]    Author, First
    Textfield Value Should Be    name=year     2023
    Textfield Value Should Be    name=journal    Test Journal

DOI Lookup Prefills Book Reference
    Go To    ${HOME_URL}/new_reference?doi=10.9999/bookdoi
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Book Title
    Textfield Value Should Be    xpath=(//input[@name='authors'])[1]    Writer, Alice
    Textfield Value Should Be    name=year     2018
    Textfield Value Should Be    name=publisher    Example Publisher
    # If chapter is shown in the book partial, verify it if present
    ${chap_exists}=    Run Keyword And Return Status    Page Should Contain Element    name=chapter
    Run Keyword If    ${chap_exists}    Textfield Value Should Be    name=chapter    7

DOI Lookup Prefills Inproceedings Reference
    Go To    ${HOME_URL}/new_reference?doi=10.9999/procdoi
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Conference Paper Title
    Textfield Value Should Be    xpath=(//input[@name='authors'])[1]    Researcher, Bob
    Textfield Value Should Be    name=year     2020
    Textfield Value Should Be    name=booktitle    Proceedings of the Test Conference

DOI Lookup Handles Unknown Or Malformed DOI
    # Use a DOI that has no fixture in test mode to simulate unresolved DOI input
    ${bad_doi}=    Set Variable    10.9999/doesnotexist
    Go To    ${HOME_URL}/new_reference?doi=${bad_doi}
    Wait Until Page Contains Element    name=title
    # An informative flash message should be shown
    Page Should Contain    DOI '${bad_doi}' could not be resolved
    # Title should be empty (server falls back to empty title; template shows current year)
    Textfield Value Should Be    name=title    ${EMPTY}

DOI Accepts 'doi:' Prefix
    ${prefixed}=    Set Variable    doi:10.9999/testdoi
    Go To    ${HOME_URL}/new_reference?doi=${prefixed}
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Article Title

DOI Accepts Full DOI URL
    ${fullurl}=    Set Variable    https://doi.org/10.9999/testdoi
    Go To    ${HOME_URL}/new_reference?doi=${fullurl}
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Article Title

DOI With Surrounding Whitespace Is Trimmed
    ${padded}=    Set Variable      10.9999/testdoi  
    Go To    ${HOME_URL}/new_reference?doi=${padded}
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Article Title

DOI Malformed String Shows Error
    ${bad2}=    Set Variable    not-a-doi
    Go To    ${HOME_URL}/new_reference?doi=${bad2}
    Wait Until Page Contains Element    name=title
    Page Should Contain    DOI '${bad2}' could not be resolved
    Textfield Value Should Be    name=title    ${EMPTY}

POST DOI Via Form Redirects And Prefills
    Go To    ${HOME_URL}/new_reference_doi
    Wait Until Page Contains Element    name=doi
    Input Text    name=doi    10.9999/testdoi
    Click Button    Fetch
    Wait Until Page Contains Element    name=title
    Textfield Value Should Be    name=title    Test Article Title

POST Empty DOI Shows Validation Error
    Go To    ${HOME_URL}/new_reference_doi
    Wait Until Page Contains Element    name=doi
    # Remove HTML 'required' to allow submitting an empty value in automated test
    Execute JavaScript    document.querySelector('input[name="doi"]').removeAttribute('required');
    Click Button    Fetch
    # Template now renders flashes; assert the validation message is shown
    Wait Until Page Contains    Please enter a DOI

*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Delete Reference Removes It From List
    Go To    ${HOME_URL}
    Click Link    Create new reference

    Input Text    name=cite_key      TEST
    Input Text    name=title     Sample Title
    Input Text    name=authors    John Doe
    Input Text    name=year      2023
    Input Text    name=publisher   Sample Publisher
    Click Button    Create

    Page Should Contain    Sample Title
    Click Element    xpath=//a[contains(., "Sample Title")]

    Click Element    xpath=//a[contains(@href, "/delete")]

    Click Button    xpath=//input[@name='delete']

    Page Should Not Contain    Sample Title
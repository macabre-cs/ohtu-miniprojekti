*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset References

*** Test Cases ***
Export Bibtex Successfully
	Go To    ${HOME_URL}
	Click Link    Create new reference

	Select From List By Value    name=reference_type    book
	Input Text    name=cite_key    Citekey1
	Input Text    name=title    Book Title 1
	Input Text    name=authors    Martin, Robert
	Input Text    name=year    2015
	Input Text    name=publisher    Publisher 1
	Input Text    name=chapter    6
    
	Click Button    Create

    # Get the actual reference ID from the checkbox value
    ${ref_id}=    Get Element Attribute    id=checkbox-1    value

    Create Session    app    http://localhost:5001
    ${tuple}=    Evaluate    ('reference_ids', '${ref_id}')
    @{data}=    Create List    ${tuple}
    ${response}=    POST On Session    app    /export_bibtex    data=${data}    expected_status=any
    Should Be Equal As Strings    ${response.status_code}    200
    Should Contain    ${response.text}    @book
    Should Contain    ${response.text}    Citekey1
    Should Contain    ${response.text}    title = {Book Title 1}
    Should Contain    ${response.text}    author = {Robert Martin}
    Should Contain    ${response.text}    year = {2015}
    Should Contain    ${response.text}    publisher = {Publisher 1}
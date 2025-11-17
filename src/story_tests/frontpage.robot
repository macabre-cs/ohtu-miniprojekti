*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Main Page Should Be Open
    Go To  ${HOME_URL}
    Title Should Be  References app

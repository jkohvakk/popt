*** Settings ***
Suite Setup     Suite setup
Documentation   It was really hard to figure out a good
...             way to test pop. Currently, this file
...             is used for generating a golden output.xml.
...             Strategy might change in the future.
...             Usage of output of Robot's own acceptance tests
...             has been suggested. Also, it has been suggested to
...             consider using a ResultVisitor from robot.api
...             instead of directly parsing the output.xml
Metadata        Version    0.1
Variables       very_long_text.py


*** Test Cases ***
Test 1
    [Tags]               Feature1     Feature2
    [Documentation]      This is an important documentation for test 1
    Write a long log
    Test 1 keyword 2

Test 2
    ${foo}=   Test 2 keyword 1    foo    bar   dii   daa
    Should be equal    ${foo}    bar


*** Keywords ***
Write a long log
    Log    ${VERY LONG TEXT}

Test 1 inner keyword
    Log    Test 1 inner keyword

Test 1 keyword 2
    Log    Test 1 keyword 2
    Test 1 inner keyword

Test 2 keyword 1
    [Arguments]    ${first}    ${second}    ${third}    ${fourth}
    [Documentation]    Arguments are really ignored. I do not know why :-).
    Log    Test 2 keyword 1
    [Return]     foo

Suite setup
    Log    We are doing some strange setup actions here!
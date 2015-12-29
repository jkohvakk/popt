*** Test Cases ***
Test 1
    Test 1 keyword 1
    Test 1 keyword 2
    Test 1 keyword 3

Test 2
    Test 2 keyword 1
    Should be equal    foo    bar


*** Keywords ***
Test 1 keyword 1
    Log    Test 1 keyword 1

Test 1 keyword 2
    Test 1 inner keyword

Test 1 inner keyword
    Log    Test 1 inner keyword

Test 1 keyword 3
    Log    Test 1 keyword 3

Test 2 keyword 1
    Log    Test 2 keyword 1


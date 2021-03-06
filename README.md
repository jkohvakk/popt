# popt
PoPT - Power of Plain Text is a tool for generating plain text human-readable log files from Robotframework output.xml files.

```
$ popt output.xml
========================================================================================================================
generated: 20160105 13:37:33.973
generator: Robot 3.0 (Python 2.7.6 on linux2)
========================================================================================================================
  Source Of Test Xml                                                                          FAIL  13:37:33.974  00.610
    Suite setup                                                                               PASS  13:37:34.030  00.000
      BuiltIn.Log                                                                             PASS  13:37:34.030  00.000
          arg: We are doing some strange setup actions here!
        13:37:34.030  INFO   We are doing some strange setup actions here!
------------------------------------------------------------------------------------------------------------------------
    Test 1                                                                                    PASS  13:37:34.031  00.200
      Write a long log                                                                        PASS  13:37:34.031  00.100
        BuiltIn.Log                                                                           PASS  13:37:34.031  00.000
            arg: ${VERY LONG TEXT}
          13:37:34.031  INFO   The Zen of Python, by Tim Peters
                               
                               Beautiful is better than ugly.
                               Explicit is better than implicit.
                               Simple is better than complex.
                               Complex is better than complicated.
                               Flat is better than nested.
                               Sparse is better than dense.
                               Readability counts.
                               Special cases aren't special enough to break the rules.
                               Although practicality beats purity.
                               Errors should never pass silently.
                               Unless explicitly silenced.
                               In the face of ambiguity, refuse the temptation to guess.
                               There should be one-- and preferably only one --obvious way to do it.
                               Although that way may not be obvious at first unless you're Dutch.
                               Now is better than never.
                               Although never is often better than *right* now.
                               If the implementation is hard to explain, it's a bad idea.
                               If the implementation is easy to explain, it may be a good idea.
                               Namespaces are one honking great idea -- let's do more of those!

      Test 1 keyword 2                                                                        PASS  13:37:34.032  00.100
        BuiltIn.Log                                                                           PASS  13:37:34.032  00.000
            arg: Test 1 keyword 2
          13:37:34.032  INFO   Test 1 keyword 2
        Test 1 inner keyword                                                                  PASS  13:37:34.032  00.100
          BuiltIn.Log                                                                         PASS  13:37:34.032  00.100
              arg: Test 1 inner keyword
            13:37:34.032  INFO   Test 1 inner keyword
        tag: Feature1
        tag: Feature2
------------------------------------------------------------------------------------------------------------------------
    Test 2                                                                                    FAIL  13:37:34.033  00.200
      Test 2 keyword 1                                                                        PASS  13:37:34.033  00.100
          arg: foo
          arg: bar
          arg: dii
          arg: daa
        assign {} 
          var {} ${foo}
        BuiltIn.Log                                                                           PASS  13:37:34.034  00.000
            arg: Test 2 keyword 1
          13:37:34.034  INFO   Test 2 keyword 1
        13:37:34.034  INFO   ${foo} = foo
      BuiltIn.Should Be Equal                                                                 FAIL  13:37:34.034  00.000
          arg: ${foo}
          arg: bar
        13:37:34.034  FAIL   foo != bar
    metadata {} 
      item {'name': 'Version'} 0.1
  errors {} 
========================================================================================================================

```

The following is useful in travis CI or similar to find out where your robot 
tests are failing. If you use "Log Source" you be able to view the source in the 
output.

```
"grep  --include=output.xml -Rl  FAIL . | xargs --no-run-if-empty -n 1 python2.7 popt"
```
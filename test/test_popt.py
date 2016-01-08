import unittest
import os
import difflib
import xml.etree.cElementTree as ET
import popt
import subprocess
from mock import patch


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
GOLDEN_TXT = os.path.join(THIS_DIR, 'golden.txt')
GOLDEN_XML = os.path.join(THIS_DIR, 'golden.xml')


class _WithPrintouts(object):

    def assert_printout(self, actual, expected):
        if(actual != expected):
            differences = list(difflib.Differ().compare(expected.splitlines(True), actual.splitlines(True)))
            self.fail('\n' + ''.join(differences))

    def assert_element(self, xml, text):
        t = ET.fromstring(xml)
        self.assert_printout(self.converter.print_children(t, 0), text)


class TestGoldenPopt(unittest.TestCase, _WithPrintouts):

    def test_golden_basic(self):
        result = popt.in_plain_text(GOLDEN_XML)
        expected = open(GOLDEN_TXT).read()
        self.assert_printout(expected.strip(), result.strip())


class TestPopt(unittest.TestCase, _WithPrintouts):

    def setUp(self):
        self.converter = popt.RobotXmlToTextConverter()

    def test_robot(self):
        self.assert_element('''<robot generated="20160105 13:37:33.973" generator="Robot 3.0 (Python 2.7.6 on linux2)">
</robot>''', '''\
generated: 20160105 13:37:33.973
generator: Robot 3.0 (Python 2.7.6 on linux2)
''')

    def test_msg_with_indenting(self):
        self.assert_element('''<msg timestamp="20160105 13:37:34.031" level="INFO">The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
</msg>''', '''\
13:37:34.031  INFO   The Zen of Python, by Tim Peters
                     
                     Beautiful is better than ugly.
                     Explicit is better than implicit.

''')

    def test_basic_keyword(self):
        self.assert_element('''<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>We are doing some strange setup actions here!</arg>
</arguments>
<msg timestamp="20160105 13:37:34.030" level="INFO">We are doing some strange setup actions here!</msg>
<status status="PASS" endtime="20160105 13:37:34.030" starttime="20160105 13:37:34.030"></status>
</kw>''', '''\
Log                                                                                           PASS  13:37:34.030  00.000
    arg: We are doing some strange setup actions here!
  13:37:34.030  INFO   We are doing some strange setup actions here!
''')

    def test_complex_keyword(self):
        self.assert_element('''<kw name="Test 2 keyword 1">
<doc>Arguments are really ignored. I do not know why :-).</doc>
<arguments>
<arg>foo</arg>
<arg>bar</arg>
<arg>dii</arg>
<arg>daa</arg>
</arguments>
<assign>
<var>${foo}</var>
</assign>
<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>Test 2 keyword 1</arg>
</arguments>
<msg timestamp="20160105 13:37:34.034" level="INFO">Test 2 keyword 1</msg>
<status status="PASS" endtime="20160105 13:37:34.034" starttime="20160105 13:37:34.034"></status>
</kw>
<msg timestamp="20160105 13:37:34.034" level="INFO">${foo} = foo</msg>
<status status="PASS" endtime="20160105 13:37:34.034" starttime="20160105 13:37:34.033"></status>
</kw>
''', '''\
Test 2 keyword 1                                                                              PASS  13:37:34.033  00.100
    arg: foo
    arg: bar
    arg: dii
    arg: daa
  assign {} 
    var {} ${foo}
  Log                                                                                         PASS  13:37:34.034  00.000
      arg: Test 2 keyword 1
    13:37:34.034  INFO   Test 2 keyword 1
  13:37:34.034  INFO   ${foo} = foo
''')

    def test_test(self):
        self.assert_element('''<test id="s1-t1" name="Simple test">
<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>hello</arg>
</arguments>
<msg timestamp="20160107 10:52:37.429" level="INFO">hello</msg>
<status status="PASS" endtime="20160107 10:52:37.429" starttime="20160107 10:52:37.429"></status>
</kw>
<status status="PASS" endtime="20160107 10:52:37.429" critical="yes" starttime="20160107 10:52:37.429"></status>
</test>
''', '''\
------------------------------------------------------------------------------------------------------------------------
Simple test                                                                                   PASS  10:52:37.429  00.000
  Log                                                                                         PASS  10:52:37.429  00.000
      arg: hello
    10:52:37.429  INFO   hello
''')

    def test_suite(self):
        self.assert_element('''<suite source="/home/jkohvakk/Documents/popt/simple_suite.robot" id="s1" name="Simple Suite">
<test id="s1-t1" name="Simple test">
<status status="PASS" endtime="20160107 10:52:37.429" critical="yes" starttime="20160107 10:52:37.429"></status>
</test>
<status status="PASS" endtime="20160107 10:52:37.430" starttime="20160107 10:52:37.414"></status>
</suite>
''', '''\
========================================================================================================================
Simple Suite                                                                                  PASS  10:52:37.414  00.160
------------------------------------------------------------------------------------------------------------------------
  Simple test                                                                                 PASS  10:52:37.429  00.000
''')

    def test_tag(self):
        self.assert_element('''<tags>
<tag>Feature1</tag>
<tag>Feature2</tag>
</tags>
''', '''\
  tag: Feature1
  tag: Feature2
''')

    def test_setting_width(self):
        self.converter.set_width(60)
        self.assert_element('''<test id="s1-t1" name="Simple test">
<status status="PASS" endtime="20160107 10:52:37.429" critical="yes" starttime="20160107 10:52:37.429"></status>
</test>
''', '''\
------------------------------------------------------------
Simple test                       PASS  10:52:37.429  00.000
''')

    def test_skip_timestamps(self):
        self.converter.skip_timestamps()
        self.assert_element('''<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>We are doing some strange setup actions here!</arg>
</arguments>
<msg timestamp="20160105 13:37:34.030" level="INFO">We are doing some strange setup actions here!</msg>
<status status="PASS" endtime="20160105 13:37:34.030" starttime="20160105 13:37:34.030"></status>
</kw>''', '''\
Log                                                                                           PASS  
    arg: We are doing some strange setup actions here!
  INFO   We are doing some strange setup actions here!
''')

    @patch('popt.subprocess.check_output')
    def test_default_width_is_by_screen_size_on_linux(self, check_output_mock):
        check_output_mock.return_value = '40 79'
        c = popt.RobotXmlToTextConverter()
        self.assertEqual(c._width, 79)
        check_output_mock.assert_called_once_with('stty size', stderr=subprocess.STDOUT, shell=True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
import unittest
import popt
import os
import xml.etree.cElementTree as ET

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
GOLDEN_TXT = os.path.join(THIS_DIR, 'golden.txt')
GOLDEN_XML = os.path.join(THIS_DIR, 'golden.xml')


class TestGoldenPopt(unittest.TestCase):

    def test_golden_basic(self):
        result = popt.popt(GOLDEN_XML)
        expected = open(GOLDEN_TXT).read()
        self.assertEqual(expected.strip(), result.strip())


class TestPopt(unittest.TestCase):

    def test_basic_keyword(self):
        t = ET.fromstring('''<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>We are doing some strange setup actions here!</arg>
</arguments>
<msg timestamp="20160105 13:37:34.030" level="INFO">We are doing some strange setup actions here!</msg>
<status status="PASS" endtime="20160105 13:37:34.030" starttime="20160105 13:37:34.030"></status>
</kw>''')
        self.assertEqual('''\
Log                                                                                           PASS  13:37:34.030  00.000
    arg: We are doing some strange setup actions here!
  13:37:34.030  INFO   We are doing some strange setup actions here!
''',
                         popt.print_children(t, 0))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
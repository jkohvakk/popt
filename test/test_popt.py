import unittest
import popt
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
GOLDEN_TXT = os.path.join(THIS_DIR, 'golden.txt')
GOLDEN_XML = os.path.join(THIS_DIR, 'golden.xml')


class TestPopt(unittest.TestCase):

    def test_golden_basic(self):
        result = popt.popt(GOLDEN_XML)
        expected = open(GOLDEN_TXT).read()
        self.assertEqual(expected.strip(), result.strip())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
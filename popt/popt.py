from __future__ import print_function
import sys
from xml.etree import cElementTree as ET

SKIPPED_ELEMENTS = ('doc', 'status', 'arguments')
LINE = '{}'.format('-' * 79)
DOUBLE_LINE = '{}'.format('=' * 79)


def popt(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    print(DOUBLE_LINE)
    print_children(root, 0)
    print(DOUBLE_LINE)


def print_children(element, indent):
    if element.tag == 'statistics':
        return
    print_element(element, indent)
    for child in element:
        print_children(child, indent + 2)


def print_element(element, indent):
    {'robot': print_robot,
     'kw': print_kw,
     'test': print_test,
     'suite': print_suite,
     'msg': print_msg}.get(element.tag, print_generic_element)(element, indent)


def print_robot(element, indent):
    for key, value in element.attrib.iteritems():
        print('{}{}: {}'.format(' ' * indent, key, value))


def print_msg(element, indent):
    print('{}msg: '.format(' ' * indent))
    for key, value in element.attrib.iteritems():
        print('{}{}: {}'.format(' ' * (indent + 2), key, value))
    print('{}{}'.format(' ' * (indent + 2), element.text))


def print_kw(element, indent):
    print_suite_test_kw(element, indent)


def print_test(element, indent):
    print(LINE)
    print_suite_test_kw(element, indent)


def print_suite(element, indent):
    print(DOUBLE_LINE)
    print_suite_test_kw(element, indent)


def print_suite_test_kw(element, indent):
    text = element.text.strip() if element.text is not None else ''
    status = element.find('status')
    indent_text = ' ' * indent
    name = element.get('name')
    len_of_first_part = len(indent_text + name + text)
    padding = ' ' * (52 - len_of_first_part)
    print('{}{} {}{}{} {}'.format(indent_text, name, text, padding,
                                  status.get('status'), status.get('starttime')))
    print('{}{}'.format(' ' * 58, status.get('endtime')))


def print_generic_element(element, indent):
    text = element.text.strip() if element.text is not None else ''
    if element.tag not in SKIPPED_ELEMENTS:
        print('{}{} {} {}'.format(' ' * indent, element.tag, element.attrib, text))


def print_separator_line_for_test_and_suite(element):
    print(DOUBLE_LINE)


if __name__ == '__main__':
    popt(sys.argv[1])
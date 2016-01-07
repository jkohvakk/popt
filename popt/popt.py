from __future__ import print_function
from xml.etree import cElementTree as ET
from datetime import datetime
from argparse import ArgumentParser


SKIPPED_ELEMENTS = ('doc', 'status', 'arguments', 'tags')


def print_in_plain_text(filename, converter):
    tree = ET.parse(filename)
    root = tree.getroot()
    return converter.convert(root)


class RobotXmlToTextConverter(object):

    def __init__(self):
        self._width = 120

    def set_width(self, width):
        if width:
            self._width = width

    def convert(self, root):
        result = self.print_double_line()
        result += self.print_children(root, 0)
        result += self.print_double_line()
        return result

    def print_line(self):
        return '{}\n'.format('-' * self._width)

    def print_double_line(self):
        return '{}\n'.format('=' * self._width)

    def print_children(self, element, indent):
        if element.tag == 'statistics':
            return ''
        result = self.print_element(element, indent)
        for child in element:
            result += self.print_children(child, indent + 2)
        return result

    def print_element(self, element, indent):
        return {'robot': self.print_robot,
                'kw': self.print_kw,
                'test': self.print_test,
                'suite': self.print_suite,
                'msg': self.print_msg,
                'arg': self.print_arg,
                'tag': self.print_tag}.get(element.tag, self.print_generic_element)(element, indent)

    def print_robot(self, element, indent):
        result = ''
        for key, value in element.attrib.iteritems():
            result += '{}{}: {}\n'.format(' ' * indent, key, value)
        return result

    def print_msg(self, element, indent):
        timestamp = self.format_msg_timestamp(element)
        level = element.get('level')
        text = self.indent_lines(element.text, indent + len(timestamp) + 5 + 2)
        return '{:>{indent}}{:<5}  {}\n'.format(timestamp, level, text, indent=indent + len(timestamp))

    def normal_format_msg_timestamp(self, msg):
        return msg.get('timestamp').split()[-1] + '  '

    def empty_format_msg_timestamp(self, msg):
        return ''

    def indent_lines(self, text, indent):
        indent_spaces = ' ' * indent
        return indent_spaces.join(line for line in text.splitlines(True))

    def print_kw(self, element, indent):
        return self.print_suite_test_kw(element, indent)

    def print_test(self, element, indent):
        result = self.print_line()
        result += self.print_suite_test_kw(element, indent)
        return result

    def print_suite(self, element, indent):
        result = self.print_double_line()
        result += self.print_suite_test_kw(element, indent)
        return result

    def print_arg(self, element, indent):
        return self.print_text_element(element, indent, 'arg')

    def print_tag(self, element, indent):
        return self.print_text_element(element, indent, 'tag')

    def print_text_element(self, element, indent, element_name):
        return '{:>{indent}} {}\n'.format(element_name + ':', element.text, indent=(indent + len(element_name + ':')))

    def print_suite_test_kw(self, element, indent):
        status = element.find('status')
        name = element.get('name')
        len_of_first_part = indent + len(name)
        padding = ' ' * (self._width - 26 - len_of_first_part)
        return '{:>{indent}}{}{}  {}\n'.format(name, padding,
                                               status.get('status'), self.format_timestamps(status),
                                               indent=indent + len(name))

    def normal_format_timestamps(self, status):
        starttime = status.get('starttime')
        endtime = status.get('endtime')
        start_dt = datetime.strptime(starttime + '000', '%Y%m%d %H:%M:%S.%f')
        end_dt = datetime.strptime(endtime + '000', '%Y%m%d %H:%M:%S.%f')
        duration = end_dt - start_dt
        return '{}  {:0>2}.{:0<3}'.format(starttime.split()[-1],
                                          duration.seconds, duration.microseconds / 1000)

    def empty_format_timestamps(self, status):
        return ''

    def print_generic_element(self, element, indent):
        text = element.text.strip() if element.text is not None else ''
        if element.tag in SKIPPED_ELEMENTS:
            return ''
        return '{:>{indent}} {} {}\n'.format(element.tag, element.attrib, text,
                                             indent=indent + len(element.tag))


def read_arguments():
    p = ArgumentParser(description='Convert Robot Framework output.xml to human-readable textual log')
    p.add_argument('filename', type=str, help='Path to output.xml file')
    p.add_argument('--skip-timestamps', '-T', action='store_true', help='Omit all timestamps from textual log (helps in diffing logs)')
    p.add_argument('--width', type=int, help='Display width in characters. Default is 120.')
    args = p.parse_args()

    converter = RobotXmlToTextConverter()
    converter.set_width(args.width)
    skip_timestamps(args.skip_timestamps, converter)
    print(print_in_plain_text(args.filename), converter)


def skip_timestamps(skip, converter):
    if skip:
        converter.format_timestamps = converter.empty_format_timestamps
        converter.format_msg_timestamp = converter.empty_format_msg_timestamp
    else:
        converter.format_timestamps = converter.normal_format_timestamps
        converter.format_msg_timestamp = converter.normal_format_msg_timestamp


if __name__ == '__main__':
    read_arguments()
from __future__ import print_function
import subprocess
import pkg_resources
from xml.etree import cElementTree as ET
from datetime import datetime
from argparse import ArgumentParser


def in_plain_text(filename, skip_timestamps=False, width=None):
    converter = RobotXmlToTextConverter(skip_timestamps)
    converter.set_width(width)

    tree = ET.parse(filename)
    root = tree.getroot()
    return converter.convert(root)


class RobotXmlToTextConverter(object):

    _SKIPPED_ELEMENTS = ('doc', 'status', 'arguments', 'tags')

    def __init__(self, skip_timestamps=False):
        self._width = self._get_default_width()
        self._timestamp_formatter = EmptyTimestampFormatter() if skip_timestamps else TimestampFormatter()

    def _get_default_width(self):
        try:
            _, width = subprocess.check_output('stty size', stderr=subprocess.STDOUT, shell=True).split()
            width = int(width)
        except:
            width = 120
        return width

    def skip_timestamps(self):
        self._timestamp_formatter = EmptyTimestampFormatter()

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
        timestamp = self._timestamp_formatter.msg(element)
        level = element.get('level')
        text = self.indent_lines(element.text, indent + len(timestamp) + 5 + 2)
        return '{:>{indent}}{:<5}  {}\n'.format(timestamp, level, text, indent=indent + len(timestamp))

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
                                               status.get('status'), self._timestamp_formatter.ts_and_duration(status),
                                               indent=indent + len(name))

    def print_generic_element(self, element, indent):
        text = element.text.strip() if element.text is not None else ''
        if element.tag in self._SKIPPED_ELEMENTS:
            return ''
        return '{:>{indent}} {} {}\n'.format(element.tag, element.attrib, text,
                                             indent=indent + len(element.tag))


class TimestampFormatter(object):

    def msg(self, element):
        return element.get('timestamp').split()[-1] + '  '

    def ts_and_duration(self, status):
        starttime = status.get('starttime')
        endtime = status.get('endtime')
        start_dt = datetime.strptime(starttime + '000', '%Y%m%d %H:%M:%S.%f')
        end_dt = datetime.strptime(endtime + '000', '%Y%m%d %H:%M:%S.%f')
        duration = end_dt - start_dt
        return '{}  {:0>2}.{:0<3}'.format(starttime.split()[-1],
                                          duration.seconds, duration.microseconds / 1000)


class EmptyTimestampFormatter(object):

    def msg(self, element):
        return ''

    def ts_and_duration(self, status):
        return ''


def get_version():
    return pkg_resources.get_distribution('popt').version


def read_arguments():
    p = ArgumentParser(description='Convert Robot Framework output.xml to human-readable textual log')
    p.add_argument('filename', type=str, help='Path to output.xml file')
    p.add_argument('--skip-timestamps', '-T', action='store_true', help='Omit all timestamps from textual log (helps in diffing logs)')
    p.add_argument('--width', type=int, help='Display width in characters. Default is screen width or 120.')
    p.add_argument('--version', '-v', action='version', help='Print version', version=get_version())
    args = p.parse_args()

    print(in_plain_text(args.filename, skip_timestamps=args.skip_timestamps, width=args.width))


if __name__ == '__main__':
    read_arguments()    
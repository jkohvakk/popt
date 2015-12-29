import sys
from xml.etree import ElementTree as ET


def popt(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    print_children(root, 0)


def print_children(element, indent):
    if element.tag == 'statistics':
        return
    text = element.text.strip() if element.text is not None else ''
    if element.tag not in ('doc', 'status', 'arguments'):
        if element.tag in ('suite', 'test', 'kw'):
            status = element.find('status')
            indent_text = ' ' * indent
            name = element.get('name')
            len_of_first_part = len(indent_text + name + text)
            padding = ' ' * (40 - len_of_first_part)
            print('{}{} {}{}{} {} {}'.format(indent_text, name, text, padding,
                                                status.get('status'), status.get('starttime'),
                                                status.get('endtime')))
        else:
            print('{}{} {} {}'.format(' ' * indent, element.tag, element.attrib, text))
    for child in element:
        print_children(child, indent + 2)


if __name__ == '__main__':
    popt(sys.argv[1])
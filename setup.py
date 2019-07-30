import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(name='popt',
      packages=['popt'],
      version='0.4',
      description='Tool for converting Robot Framework xml output to a human-readable log file',
      long_description='{0}\n\n{1}'.format(read("README.md"),
                                           read("CHANGES.md"),),
      long_description_content_type="text/markdown",
      author='Janne Kohvakka',
      author_email='jkohvakk@gmail.com',
      url='https://github.com/jkohvakk/popt',
      keywords=['Robot Framework', 'log'],
      classifiers=[],
      extras_require={
            'test': [
                  'pytest',
                  'mock',
            ],
      },
      entry_points={'console_scripts': ['popt=popt:read_arguments']}
      )

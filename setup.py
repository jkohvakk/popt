from setuptools import setup


setup(name='popt',
      packages=['popt'],
      version='0.3',
      description='Tool for converting Robot Framework xml output to a human-readable log file',
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

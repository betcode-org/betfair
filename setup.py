import sys
from distutils.core import setup, Extension
from setuptools.command.test import test as TestCommand
from betfairlightweight.__init__ import __version__


INSTALL_REQUIRES = [
    'requests=2.10.0',
]
TEST_REQUIRES = [
    'mock'
]

setup(
        name='betfairlightweight',
        version=__version__,
        packages=['betfairlightweight', 'betfairlightweight.endpoints',
                  'betfairlightweight.resources', 'betfairlightweight.streaming'],
        package_dir={'betfairlightweight': 'betfairlightweight'},
        install_requires=INSTALL_REQUIRES,
        requires=['requests'],
        url='https://github.com/liampauling/betfairlightweight',
        license='MIT',
        author='liampauling',
        author_email='',
        description='Lightweight python wrapper for Betfair API-NG',
        test_suite='tests'
)

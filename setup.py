import sys

from setuptools import setup
from betfairlightweight.__init__ import __version__


INSTALL_REQUIRES = [
    'requests',
]
TEST_REQUIRES = [
    'mock'
]

if sys.version_info < (3,4):
    INSTALL_REQUIRES.extend([
        'enum34',
    ])

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

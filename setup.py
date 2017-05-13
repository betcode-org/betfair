import sys
import re

from setuptools import setup


INSTALL_REQUIRES = [
    'requests',
    'ciso8601',
    'ujson',
]
TEST_REQUIRES = [
    'mock'
]

if sys.version_info < (3, 4):
    INSTALL_REQUIRES.extend([
        'enum34',
    ])

with open('betfairlightweight/__init__.py', 'r') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE
    ).group(1)

setup(
        name='betfairlightweight',
        version=version,
        packages=[
            'betfairlightweight',
            'betfairlightweight.endpoints',
            'betfairlightweight.resources',
            'betfairlightweight.streaming',
        ],
        package_dir={
            'betfairlightweight': 'betfairlightweight'
        },
        install_requires=INSTALL_REQUIRES,
        url='https://github.com/liampauling/betfairlightweight',
        license='MIT',
        author='liampauling',
        author_email='',
        description='Lightweight python wrapper for Betfair API-NG',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        test_suite='tests'
)

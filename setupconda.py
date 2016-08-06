from betfairlightweight.__init__ import __version__
from distutils.core import setup, Extension
import distutils.command.bdist_conda


setup(
        name='betfairlightweight',
        version=__version__,
        packages=['betfairlightweight', 'betfairlightweight.endpoints',
                  'betfairlightweight.resources', 'betfairlightweight.streaming'],
        package_dir={'betfairlightweight': 'betfairlightweight'},
        requires=['requests'],
        url='https://github.com/LiamPa/betfairlightweight',
        license='',
        author='liampauling',
        author_email='',
        description='Lightweight python wrapper for Betfair API-NG',
        conda_buildnum=1,
        conda_features=['mk1']
)

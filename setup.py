from distutils.core import setup, Extension
import distutils.command.bdist_conda


setup(
        name='betfairlightweight',
        version='0.0.1',
        packages=['betfairlightweight', 'betfairlightweight.errors', 'betfairlightweight.parse'],
        package_dir={'betfairlightweight': 'betfairlightweight'},
        url='https://github.com/LiamPa/betfairlightweight',
        license='',
        author='liampauling',
        author_email='',
        description='Lightweight python wrapper for Betfair API-NG',
        conda_buildnum=1,
        conda_features=['mk1']
)

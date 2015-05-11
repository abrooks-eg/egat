#####################################################################################
#
# To build the package and upload to PyPi
#    python setup.py sdist upload 
#
# To build and upload to Test PyPi
#    python setup.py sdist upload -r https://testpypi.python.org/pypi
# To install from Test PyPi
#    pip install -i https://testpypi.python.org/pypi egat
#
#####################################################################################
import setuptools
from distutils.core import setup
setup(
    name = 'egat',
    packages = ['egat', 'egat.loggers', 'egat.scripts'], # this must be the same as the name above
    include_package_data=True,
    package_data = {
        'data': ['default.css', 'egat-header.png']
    },
    entry_points = {
        'console_scripts': ['egatest = egat.scripts.egatest:run']
    },
    version = '0.9.23',
    description = 'An automated testing toolkit',
    author = 'E-gineering LLC',
    author_email = 'eg.pypi@e-gineering.com', # contact email
    url = 'http://e-gineering.com', # url with information about the package
    download_url = 'https://bitbucket.org/e-gineering/e-g_automated_testing_poc/get/tag/0.1.tar.gz', # should be a url of the tarball
    keywords = ['testing', 'automated testing', 'functional testing'], # arbitrary keywords
    classifiers = [],
)

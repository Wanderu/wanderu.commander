# coding: utf-8
from setuptools import setup, find_packages
from os.path import join as pathjoin, dirname


def read(*rnames):
    return open(pathjoin(dirname(__file__), *rnames)).read()

setup(
    # about meta
    name = 'wanderu.commander',
    version = '0.1.6',
    author = "Wanderu Dev Team",
    author_email = "dev@wanderu.com",
    url = "www.wanderu.com",
    description = read('README.rst'),
    # package info
    namespace_packages = ['wanderu'],  # setuptools specific feature
    packages = find_packages(),   # Find packages in the 'src' folder
    #package_dir = {'': 'src'},        # Make the 'src' folder the root
                                       # package folder
    install_requires = [
        'setuptools',
        'enum34>=1.0'
        ],
    setup_requires = ['nose'],  # for the ``nosetests`` setuptools command
    tests_require = ['nose', 'coverage>=4.0a1'],  # to run the tests themselves
    test_suite = 'nose.collector',
    # entry_points={
    #     'console_scripts': [
    #         'exprog = module_path:callable_name',
    #     ]
    # }
)

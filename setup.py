# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "application"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Twitter Social Popularity Service",
    author_email="rsamer@ist.tugraz.at",
    url="",
    keywords=["Swagger", "Twitter Social Popularity Service"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['application=application.__main__:main']},
    long_description="""\
    Twitter Social Popularity Service
    """
)


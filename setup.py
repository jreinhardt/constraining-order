#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the version from the relevant file
with open(path.join(here, 'version'), encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name='constrainingorder',
    version=version,
    packages=find_packages("src"),
    package_dir={"" : "src"},
    description='Pure python constraint satisfaction solvers',
    long_description=long_description,
    author="Johannes Reinhardt",
    author_email="jreinhardt@ist-dein-freund.de",
    license="LGPL 2.1+",
    keywords="csp constraint satisfaction propagation intervals",
    url="https://github.com/jreinhardt/constraining order"
)

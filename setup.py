#!/usr/bin/env python3
import os

from distutils.core import setup
from os import path


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

VERSION = read(path.join('pg_corrupt', 'VERSION')).strip()

install_requires = [
    l for l in read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

setup(
    name="pg_corrupt",
    packages=["pg_corrupt"],
    install_requires=install_requires,
    version=VERSION,
    description="Find and excise corrupt tuples from Postgres databases",
    author="Daniel Farina",
    author_email="daniel@heroku.com",
    keywords=["postgres", "postgresql", "database", "corruption"],
    package_data={'pg_corrupt': ['VERSION']},
    entry_points={'console_scripts': ['pg_corrupt=pg_corrupt.cmd:main']}
)

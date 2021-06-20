#!/usr/bin/env python3
# Ledger - A web application to track cryptocurrency investments
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import setup
from setuptools import find_packages


version = '0.0.6'
tag = f'/archive/refs/tags/{version}.zip'
url = 'https://github.com/teleprint-me/ledger'
download_url = url + tag

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    install_requires = file.read().splitlines()

dependency_links = [
    'git+ssh://git@github.com/teleprint-me/coinbasepro-python.git#egg=coinbasepro-python',
    'git+ssh://git@github.com/teleprint-me/python3-krakenex.git#egg=python3-krakenex'
]

tests_require = ['pytest']

setup(
    name='teleprint.me',
    version=version,
    description='A web application to track cryptocurrency investments',
    long_description=long_description,
    author='teleprint.me',
    author_email='77757836+teleprint-me@users.noreply.github.com',
    url=url,
    download_url=download_url,
    install_requires=install_requires,
    dependency_links=dependency_links,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    packages=find_packages(),
    python_requires='>=3.6',
    keywords=[
        'ledger', 'teleprint.me', 'web', 'app', 'invest', 'track',
        'bitcoin', 'ethereum', 'litecoin', 'client', 'interface',
        'exchange', 'crypto', 'currency', 'trade', 'trading', 'trading-api',
        'dca', 'ddca', 'dva', 'ddva', 'accounting'
    ],
    classifiers=[
        'Development Status :: Development/Unstable',
        'Intended Audience :: Client',
        'Intended Audience :: Web Application',
        'Intended Audience :: Financial Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software :: Web Application :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

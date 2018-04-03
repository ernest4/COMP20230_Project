#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: Put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(ernest4): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: Put package test requirements here
]

setup(
    name='ernestas_monkevicius_14493758_project',
    version='0.1.0',
    description="Term project for COMP20230. Finds out optimal route for a list of input airports.",
    long_description=readme + '\n\n' + history,
    author="Ernestas Monkevicius",
    author_email='ernestas.monkevicius@ucdconnect.ie',
    url='https://github.com/ernest4/ernestas_monkevicius_14493758_project',
    packages=find_packages(include=['ernestas_monkevicius_14493758_project']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='ernestas_monkevicius_14493758_project',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

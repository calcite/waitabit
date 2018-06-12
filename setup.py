#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'aiohttp>=2.2.5',
    'sockjs>=0.6.0',
]

setup_requirements = []

test_requirements = []

setup(
    name='waitabit',
    version='0.5.0',
    description="The simplest waiting line management.",
    long_description=readme + '\n\n' + history,
    author="Josef Nevrly",
    author_email='jnevrly@alps.cz',
    url='https://github.com/calcite/waitabit',
    packages=find_packages(include=['waitabit']),
    entry_points={
        'console_scripts': [
            'waitabit=waitabit.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='waitabit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

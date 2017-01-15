#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('src')
README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()


setup(
    name='ao3',
    version='0.2.0',
    description='A Python API for scraping AO3 (the Archive of Our Own)',
    long_description=long_description,
    url='https://github.com/alexwlchan/ao3',
    author='Alex Chan',
    author_email='alex@alexwlchan.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=[
        'beautifulsoup4>=4.5.3, <5',
        'requests>=2.12.4, <3',
    ],
)

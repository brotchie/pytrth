#!/usr/bin/env python

from setuptools import setup

setup(name='pytrth',
    packages=['trth'],
    version='1.0',
    description='Python interface to the Thomson Reuters Tick History API.',
    author='James Brotchie',
    author_email='brotchie@gmail.com',
    url='https://github.com/brotchie/pytrth',
    install_requires=['suds', 'pyyaml', 'egenix-mx-base'],
)

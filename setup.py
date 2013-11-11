#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from eedd import __version__ as version

setup(
    name='eedd',
    version=version,
    description='dd-inspirted interface to Arduino EEPROM burner',
    author='Luke Maurits',
    author_email='luke@maurits.id.au',
    url='https://github.com/lmaurits/eedd',
    license="BSD (3 clause)",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
    ],
    scripts=['bin/eedd',],
    py_modules=['eedd',],
    requires=['pyserial'],
    install_requires=['pyserial']
)

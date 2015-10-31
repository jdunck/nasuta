#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "src"))


version = __import__('nasuta').__version__

setup(
    name='nasuta',
    version=version,
    description="Data structures you wish were in the language.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'rb').read().decode('utf-8'),
    author='Jeremy Dunck',
    author_email='jdunck@gmail.com',
    url='https://github.com/jdunck/nasuta',
    package_dir = {'': 'src'},
    packages=['nasuta'],
    tests_require=[],
    test_suite='runtests.get_suite',
    license='BSD License',
    classifiers=['Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Natural Language :: English',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: Implementation :: PyPy',
                'Programming Language :: Python :: Implementation :: CPython',],
)


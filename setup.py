from distutils.core import setup

from setuptools import find_packages

setup(
    name='mediawiki-utilities',
    version=open('VERSION').read().strip(),
    author='Aaron Halfaker',
    author_email='aaron.halfaker@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/mediawiki-utilities',
    license=open('LICENSE').read(),
    description='A set of utilities for extracting and processing MediaWiki data.',
    long_description=open('README.rst').read(),
    install_requires=[
        "argparse >= 1.1",
        "requests >= 2.0.1",
        "oursql >= 0.9.1"],
    test_suite='nose.collector',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering"
    ],
)

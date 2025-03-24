#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# Get version from package
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'src', 'hpfc', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

# Read the README file for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hpfc-tool',
    version=about['__version__'],
    description='A high-performance directory comparison tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ethan Li',
    url='https://github.com/ethan-li/hpfc',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.11,<4',
    install_requires=[
        'jinja2>=2.11.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=20.8b1',
            'isort>=5.0.0',
            'mypy>=0.800',
            'flake8>=3.8.0',
            'build>=0.7.0',
            'twine>=3.4.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'hpfc=hpfc.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
    keywords='directory, folder, comparison, diff, file comparison',
) 
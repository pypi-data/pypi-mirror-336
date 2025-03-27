#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()

setup(
    name='pyquet',
    version='1.0.7',
    description='Generate pseudorandom data from .json schemas',
    author='Ricardo Múgica',
    author_email='rmugicag@gmail.com',
    entry_points={
        "console_scripts": [
            "PyquetGenerate=pyquet.pyquet_generator:main"
        ]
    },
    install_requires=[
        "pandastable",
        "pandas",
        "numpy <= 2",
        "pyarrow >= 1.0.0",
    ],
    packages=find_packages(),
)
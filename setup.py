#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-instrument",
    version="0.3.0",
    author="Joep Schuurkes",
    author_email="j19sch@gmail.com",
    maintainer="Joep Schuurkes",
    maintainer_email="j19sch@gmail.com",
    license="MIT",
    url="https://github.com/j19sch/pytest-instrument",
    description="pytest plugin to instrument tests",
    long_description=read("README.rst"),
    packages=["pytest_instrument"],
    python_requires=">=3.6",
    install_requires=["pytest>=5.1.0", "python-json-logger>=0.1.11"],
    tests_require=["jsonschema>=3.1.1"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["metrics = pytest_instrument.plugin"]},
)

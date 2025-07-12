#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains the build information for this project."""
import setuptools

# open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements
required = [
    "setuptools>=51.1.1",       # standard
]

setuptools.setup(
    name="borb",
    version="3.0.2",
    author="Joris Schellekens",
    author_email="joris.schellekens.1989@gmail.com",
    description="borb is a library for reading, creating and manipulating PDF files in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorisschellekens/borb",
    packages=setuptools.find_packages(include=["borb", "borb.*"]),
    include_package_data=True,
    install_requires=required,
    python_requires=">=3.6",
)

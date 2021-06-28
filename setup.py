#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains the build information for this project
"""
import sys

import setuptools

# open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# open requirements
required = [
    "fonttools>=4.22.1",  # TTF fonts
    "Pillow>=7.1.0",  # image processing
    "python-barcode>=0.13.1",  # generating barcodes
    "qrcode[pil]>=6.1",  # generating QR codes
    "requests>=2.24.0" "setuptools~=51.1.1",  # generating images from a URL  # standard
] + (["windows-curses>=2.2.0"] if sys.platform.startswith("win") else [])

dependency_links = [
    "http://github.com/ojii/pymaging/tarball/master",
    "http://github.com/ojii/pymaging-png/tarball/master",
]

setuptools.setup(
    name="ptext-joris-schellekens",  # Replace with your own username
    version="2.0.0",
    author="Joris Schellekens",
    author_email="joris.schellekens.1989@gmail.com",
    description="pText is a library for reading, creating and manipulating PDF files in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorisschellekens/ptext-release",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    dependency_links=dependency_links,
    python_requires=">=3.6",
)

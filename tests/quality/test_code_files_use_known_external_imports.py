import typing
from pathlib import Path

from tests.quality.all_code_files import get_all_code_files_in_repository
from tests.test_case import TestCase


class TestCodeFilesUseKnownExternalImports(TestCase):

    EXTERNAL_IMPORT_WHITELIST: typing.List[str] = [
        "from barcode.",
        "from cryptography.",
        "from fontTools.",
        "from lxml.",
        "from PIL ",
        "import barcode  # type: ignore[import]",
        "import qrcode  # type: ignore[import]",
        "import requests",
    ]

    INTERNAL_IMPORT_WHITELIST: typing.List[str] = [
        "from __future__ import annotations",
        "from decimal import Decimal",
        "from decimal import Decimal as oDecimal",
        "from functools import cmp_to_key",
        "from typing import TYPE_CHECKING",
        "import atexit",
        "import base64",
        "import copy",
        "import datetime",
        "import decimal",
        "import enum",
        "import functools",
        "import hashlib",
        "import io",
        "import itertools",
        "import json",
        "import logging",
        "import math",
        "import numbers",
        "import os",
        "import pathlib",
        "import platform",
        "import random",
        "import re",
        "import signal",
        "import string",
        "import subprocess",
        "import sys",
        "import sysconfig",
        "import tempfile",
        "import threading",
        "import time",
        "import typing",
        "import types",
        "import urllib.request",
        "import unittest",
        "import xml.etree.ElementTree",
        "import xml.etree.ElementTree as ET",
        "import zlib",
    ]

    KNOWN_EXCEPTIONS: typing.List[str] = [
        "pdf_to_mp3.py",
        "markdown_to_pdf.py",
        "html_to_pdf.py",
        "face_detection_event_listener.py",
        "ocr_image_render_event_listener.py",
        "a4_portrait_template.py",
        "a4_portrait_resume_template.py",
        "slide_template.py",
        "codeblock_with_syntax_highlighting.py",
        "codeblock.py",
        "unsplash.py",
    ]

    def test_code_files_use_known_external_imports(self):

        # check all the imports in each file
        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if (
                python_file.name
                in TestCodeFilesUseKnownExternalImports.KNOWN_EXCEPTIONS
            ):
                continue

            # extract code
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()

            # extract imports
            imports: typing.List[str] = [
                x.strip()
                for x in lines
                if x.strip().startswith("import ") or x.strip().startswith("from ")
            ]

            # filter every "from borb.<something>"
            # fmt: off
            external_imports: typing.List[str] = [x for x in imports if not x.startswith("from borb.")]
            external_imports = [x for x in external_imports if not x.startswith("import borb.")]
            # fmt: on

            # filter every "from .<something>"
            external_imports = [
                x for x in external_imports if not x.startswith("from .")
            ]

            # filter system_import_whitelist
            external_imports = [
                x
                for x in external_imports
                if x
                not in TestCodeFilesUseKnownExternalImports.INTERNAL_IMPORT_WHITELIST
            ]

            # filter known dependencies
            # fmt: off
            for known_external_import in TestCodeFilesUseKnownExternalImports.EXTERNAL_IMPORT_WHITELIST:
                external_imports = [x for x in external_imports if not x.startswith(known_external_import)]
            # fmt: on

            # fmt: off
            if len(external_imports) > 0:
                assert False, f"Unknown external import '{external_imports[0]}' in file {python_file}"
            # fmt: on

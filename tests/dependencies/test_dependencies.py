import typing
from pathlib import Path

from tests.test_case import TestCase


class TestDependencies(TestCase):
    def _get_all_python_files_in_borb_directory(self) -> typing.List[Path]:

        # find root directory
        root_dir: Path = Path(__file__).parent
        while root_dir.exists() and ".github" not in [
            x.name for x in root_dir.iterdir()
        ]:
            root_dir = root_dir.parent

        # find all code files
        todo_stk: typing.List[Path] = [root_dir / "borb"]
        python_files: typing.List[Path] = []
        while len(todo_stk) > 0:
            tmp: Path = todo_stk[0]
            todo_stk.pop(0)
            if tmp.is_dir():
                todo_stk += [x for x in tmp.iterdir()]
                continue
            if tmp.is_file() and tmp.name.endswith(".py"):
                python_files.append(tmp)

        # return
        return python_files

    def test_all_internal_imports_use_fully_qualified_path(self):

        # check all the imports in each file
        for python_file in self._get_all_python_files_in_borb_directory():

            # fmt: off
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()
            imports: typing.List[str] = [x for x in lines if x.startswith("import") or x.startswith("from")]
            # fmt: on

            # fmt: off
            forbidden_imports: typing.List[str] = [x for x in imports if x.startswith("from borb.pdf import")]
            if len(forbidden_imports) > 0:
                assert False, f"Forbidden import '{forbidden_imports[0][:-1]}' in file {python_file}"
            # fmt: on

    def test_there_are_no_multiline_imports(self):

        # check all the imports in each file
        for python_file in self._get_all_python_files_in_borb_directory():

            # fmt: off
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()
            imports: typing.List[str] = [x for x in lines if x.startswith("import") or x.startswith("from")]
            # fmt: on

            # fmt: off
            multi_line_imports: typing.List[str] = [x for x in imports if ("(" in x)]
            if len(multi_line_imports) > 0:
                assert False, f"Multiline import '{multi_line_imports[0][:-1]}' in file {python_file}"
            # fmt: on

    def test_external_imports_are_listed_in_requirements(self):

        # whitelist
        system_import_whitelist: typing.List[str] = [
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
            "import xml.etree.ElementTree as ET",
            "import zlib",
        ]

        # check all the imports in each file
        for python_file in self._get_all_python_files_in_borb_directory():
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()
            imports: typing.List[str] = [
                x.strip()
                for x in lines
                if x.strip().startswith("import") or x.strip().startswith("from")
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
                x for x in external_imports if x[:-1] not in system_import_whitelist
            ]

            # filter known dependencies
            # fmt: off
            external_imports = [x for x in external_imports if not x.startswith("from barcode.")]
            external_imports = [x for x in external_imports if not x.startswith("from cryptography.")]
            external_imports = [x for x in external_imports if not x.startswith("from fontTools.")]
            external_imports = [x for x in external_imports if not x.startswith("from lxml.")]
            external_imports = [x for x in external_imports if not x.startswith("from PIL ")]
            external_imports = [x for x in external_imports if not x.startswith("import barcode  # type: ignore [import]")]
            external_imports = [x for x in external_imports if not x.startswith("import qrcode  # type: ignore [import]")]
            external_imports = [x for x in external_imports if not x.startswith("import requests")]
            # fmt: on

            # known exceptions
            if python_file.name == "pdf_to_mp3.py":
                external_imports = [
                    x for x in external_imports if not x.startswith("from gtts ")
                ]
            if python_file.name == "markdown_to_pdf.py":
                external_imports = [
                    x for x in external_imports if not x.startswith("from markdown_it ")
                ]

            # fmt: off
            if len(external_imports) > 0:
                assert False, f"Unknown external import '{external_imports[0][:-1]}' in file {python_file}"
            # fmt: on

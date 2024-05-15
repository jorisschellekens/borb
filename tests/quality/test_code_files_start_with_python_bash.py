import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesStartWithPythonBash(unittest.TestCase):

    KNOWN_EXCEPTIONS: typing.List[str] = ["__init__.py"]

    def test_all_code_files_start_with_python_bash(self):
        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if python_file.name in TestCodeFilesStartWithPythonBash.KNOWN_EXCEPTIONS:
                continue

            # read lines
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()

            # check
            assert lines[0].startswith(
                "#!/usr/bin/env python"
            ), f"File {python_file} does not start with python bash (1)"
            assert lines[1].startswith(
                "# -*- coding: utf-8 -*-"
            ), f"File {python_file} does not start with python bash (2)"

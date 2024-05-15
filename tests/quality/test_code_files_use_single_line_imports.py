import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesUseSingleLineImports(unittest.TestCase):
    def test_code_files_use_single_line_imports(self):

        # check all the imports in each file
        for python_file in get_all_code_files_in_repository():

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

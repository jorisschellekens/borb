import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesUseFullyQualifiedBorbImports(unittest.TestCase):
    def test_code_files_use_fully_qualified_borb_imports(self):

        # check all the imports in each file
        for python_file in get_all_code_files_in_repository():

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

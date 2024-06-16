import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesNeverUseKeyring(unittest.TestCase):
    def test_code_files_never_use_keyring(self):

        # check all the imports in each file
        for python_file in get_all_code_files_in_repository():

            # fmt: off
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()
            imports: typing.List[str] = [x.strip() for x in lines if x.strip().startswith("import") or x.strip().startswith("from")]
            # fmt: on

            # fmt: off
            assert not any([x.startswith("import keyring") for x in imports]), f"keyring is used in {python_file}"
            # fmt: on

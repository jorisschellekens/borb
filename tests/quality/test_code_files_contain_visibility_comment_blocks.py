import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesContainVisibilityCommentBlocks(unittest.TestCase):

    KNOWN_EXCEPTIONS: typing.List[str] = ["adobe_glyph_list.py", "page_size.py"]

    def test_code_files_contain_visibility_comment_blocks(self):

        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if (
                python_file.name
                in TestCodeFilesContainVisibilityCommentBlocks.KNOWN_EXCEPTIONS
            ):
                continue

            # count the number of lines in the file
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()

            # if not a class, continue
            if not any([x.startswith("class ") for x in lines]):
                continue

            assert any(
                ["# CONSTRUCTOR" in x for x in lines]
            ), f"File {python_file.name} does not contain CONSTRUCTOR visibility comment block."
            assert any(
                ["# PRIVATE" in x for x in lines]
            ), f"File {python_file.name} does not contain PRIVATE visibility comment block."
            assert any(
                ["# PUBLIC" in x for x in lines]
            ), f"File {python_file.name} does not contain PUBLIC visibility comment block."

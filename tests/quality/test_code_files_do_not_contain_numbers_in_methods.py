import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesDoNotContainNumbersInMethods(unittest.TestCase):

    KNOWN_EXCEPTIONS: typing.List[str] = [
        "a4_portrait_template.py",
        "color.py",
        "font_type_1.py",
        "html_to_pdf.py",
        "information_dictionary_transformer.py",
        "line_art_factory.py",
        "pdf_to_mp3.py",
        "table_util.py",
        "true_type_font.py",
    ]

    def test_code_files_do_not_contain_numbers_in_methods(self):

        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if (
                python_file.name
                in TestCodeFilesDoNotContainNumbersInMethods.KNOWN_EXCEPTIONS
            ):
                continue

            # get the lines of code from each file
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()

            # keep only function/method definitions
            lines = [x.strip() for x in lines if x.startswith("    def ")]
            lines = [x[: x.index("(")] for x in lines]

            # check
            assert not any(
                [any([y in x for y in "0123456789"]) for x in lines]
            ), f"File {python_file.name} has a method containing numbers."

import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesAreSmall(unittest.TestCase):

    KNOWN_EXCEPTIONS: typing.List[str] = [
        "a4_portrait_invoice_template.py",
        "a4_portrait_resume_template.py",
        "a4_portrait_template.py",
        "adobe_glyph_list.py",
        "color.py",
        "emoji.py",
        "font_type_1.py",
        "html_to_pdf.py",
        "layout_element.py",
        "line_art_factory.py",
        "pantone.py",
        "postfix_eval.py",
        "slide_template.py",
        "smart_art.py",
        "table.py",
        "types.py",
    ]

    def test_code_files_are_small(self):

        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if python_file.name in TestCodeFilesAreSmall.KNOWN_EXCEPTIONS:
                continue

            # count the number of lines in the file
            nof_lines: int = 0
            with open(python_file, "r") as fh:
                nof_lines = len(fh.readlines())
            assert nof_lines < 500, f"File {python_file.name} is over 400 lines."

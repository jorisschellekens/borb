import typing
import unittest

from tests.quality.all_code_files import get_all_code_files_in_repository


class TestCodeFilesContainSortedMethods(unittest.TestCase):

    KNOWN_EXCEPTIONS: typing.List[str] = [
        "append_cubic_bezier.py",
        "barcode.py",
        "canvas_graphics_state.py",
        "chunk_of_text_render_event.py",
        "cid_font_type_0.py",
        "color.py",
        "document_info.py",
        "farrow_and_ball.py",
        "font_type_0.py",
        "font_type_1.py",
        "font_type_3.py",
        "glyph_line.py",
        "heterogeneous_paragraph.py",
        "low_level_tokenizer.py",
        "lzw_decode.py",
        "matrix.py",
        "multi_column_layout.py",
        "ocr_image_render_event_listener.py",
        "pantone.py",
        "paragraph.py",
        "progressbar.py",
        "push_button.py",
        "rectangle.py",
        "redacted_canvas_stream_processor.py",
        "regular_expression_text_extraction.py",
        "str_trie.py",
        "table.py",
        "true_type_font.py",
        "types.py",
        "cid_font_type_2.py",
        "disjoint_set.py",
    ]

    def test_code_files_contain_sorted_methods(self):

        for python_file in get_all_code_files_in_repository():

            # skip KNOWN_EXCEPTIONS
            if python_file.name in TestCodeFilesContainSortedMethods.KNOWN_EXCEPTIONS:
                continue

            # get the lines of code from each file
            lines: typing.List[str] = []
            with open(python_file, "r") as fh:
                lines = fh.readlines()

            # if not a class, continue
            if not any([x.startswith("class ") for x in lines]):
                continue

            # keep only function/method definitions
            lines = [x.strip() for x in lines if x.startswith("    def ")]

            # split into its parts
            constructor_defs: typing.List[str] = [
                x for x in lines if x.startswith("def __")
            ]
            private_defs: typing.List[str] = [
                x for x in lines if x.startswith("def _") and x not in constructor_defs
            ]
            public_defs: typing.List[str] = [
                x
                for x in lines
                if x in lines
                and (x not in private_defs)
                and (x not in constructor_defs)
            ]

            # sort each part
            constructor_defs.sort()
            private_defs.sort()
            public_defs.sort()

            # check order
            sorted_defs: typing.List[str] = constructor_defs
            sorted_defs += private_defs
            sorted_defs += public_defs
            assert (
                lines == sorted_defs
            ), f"Function/method defs are not sorted in {python_file}."

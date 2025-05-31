#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import re
import sys
import typing

KNOWN_EXCEPTIONS: typing.List[str] = [
    "cmyk_color.py::__init__",
    "fixed_column_width_table.py::__init__",
    "flexible_column_width_table.py::__init__",
    "inside.py::__init__",
    "map.py::scale_to_fit",
    "page_content_stream_processor.py::_apply_c",
    "page_content_stream_processor.py::_apply_d1",
    "page_content_stream_processor.py::_apply_k",
    "page_content_stream_processor.py::_apply_K",
    "page_content_stream_processor.py::_apply_re",
    "page_content_stream_processor.py::_apply_RG",
    "page_content_stream_processor.py::_apply_rg",
    "page_content_stream_processor.py::_apply_v",
    "pdf_bytes.py::next_eof_keyword",
    "pdf_bytes.py::next_integer",
    "pdf_bytes.py::next_newline",
    "pdf_bytes.py::next_space",
    "pdf_bytes.py::next_startxref_keyword",
    "pdf_bytes.py::next_start_of_dictionary",
    "pdf_bytes.py::next_start_of_pdf_keyword",
    "pdf_bytes.py::previous_eof_keyword",
    "pdf_bytes.py::previous_newline",
    "pdf_bytes.py::previous_startxref_keyword",
    "pdf_bytes.py::previous_start_of_pdf_keyword",
    "pdf_bytes.py::__find_next",
    "pdf_bytes.py::__find_previous",
    "primitives.py::__init__",
    "reference_visitor.py::__look_up_reference",
    "rgb_color.py::__init__",
    "shape.py::scale_to_fit",
    "source.py::image",
    "source.py::text",
    "table.py::__init__",
    "text_event.py::__init__",
    "true_type_font.py::__get_cmap_for_type_0_font",  # turns out this script can not deal with mypy type comments
    "xref_visitor.py::_get_value_from_dictionary_bytes",
]


def main(root: str):
    stk_todo = [pathlib.Path(root)]
    stk_done = []
    while len(stk_todo) > 0:
        f = stk_todo.pop(0)
        if f.is_dir():

            # IF we have reached the /.github directory
            # THEN do not delve into it
            if f.name == ".github":
                continue

            # IF we have reached the /.venv directory
            # THEN do not delve into it
            if f.name == ".venv":
                continue

            # IF we have reached the /tests directory
            # THEN do not delve into it
            if f.name == "tests":
                continue

            stk_todo += [subdir for subdir in f.iterdir()]
        else:
            if f.name.endswith(".py"):
                stk_done += [f]

    def __extract_method_name(s: str) -> str:
        s = s[s.find("    def ") + 8 :]
        s = s[: s.find("(")]
        return s

    def __extract_method_parameters(s: str) -> typing.List[str]:
        open_bracket_count: int = 0
        args: typing.List[str] = [""]
        for c in s:
            if c == ",":
                if open_bracket_count != 0:
                    args[-1] += c
                else:
                    args += [""]
                continue
            if c == "[":
                open_bracket_count += 1
                args[-1] += c
                continue
            if c == "]":
                open_bracket_count -= 1
                args[-1] += c
                continue
            args[-1] += c
        return args

    # loop over all .py files
    function_def_regex: re.Pattern = re.compile(
        "def (?P<name>[^()]+)\\((?P<args>[^()]+)\\)"
    )
    exit_code: int = 0
    nof_bad_files: int = 0
    for python_file in stk_done:
        text: str = ""
        with open(python_file, "r") as python_file_handle:
            text = python_file_handle.read()

        # handle \n
        while "\n" in text:
            text = text.replace("\n", "")

        # find all function definitions
        for m in re.findall(function_def_regex, text):

            # build args_with_default
            args: typing.List[str] = [
                x.strip() for x in __extract_method_parameters(m[1])
            ]
            args = [x for x in args if len(x) > 0]
            args_with_default: typing.List[str] = [x for x in args if "=" in x]

            # build args_without_default
            args_without_default: typing.List[str] = [x for x in args if "=" not in x]
            if "self" in args:
                args_without_default.remove("self")

            # build sorted_args
            sorted_args = []
            if "self" in args:
                sorted_args += ["self"]
            sorted_args += sorted(args_without_default)
            sorted_args += sorted(args_with_default)

            identifier: str = f"{python_file.name}::{m[0]}"
            if identifier in KNOWN_EXCEPTIONS:
                continue

            # print
            if args != sorted_args:
                exit_code = 1
                nof_bad_files += 1
                print(f"Methods arguments unsorted in {identifier}")
                print(f"\t- <ACTUAL> \t <EXPECTED>")
                for a0, a1 in zip(args, sorted_args):
                    print(f"\t- {a0} \t {a1}")

    # print
    if nof_bad_files != 0:
        print(f"Found {nof_bad_files} METHODS with unsorted parameters.")

    # exit
    sys.exit(exit_code)


if __name__ == "__main__":
    main(sys.argv[1])

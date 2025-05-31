#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

KNOWN_EXCEPTIONS = [
    "a4_portrait.py",
    "a4_portrait_invoice.py",
    "a4_portrait_resume.py",
    "adobe_glyph_list.py",
    "avatar.py",
    "chunk.py",
    "code_snippet.py",
    "common_character_encodings.py",
    "conformance_checks.py",
    "dict_visitor.py",
    "document.py",
    "emoji.py",
    "emoji_a_k.py",
    "emoji_l_z.py",
    "heterogeneous_paragraph.py",
    "layout_element.py",
    "line_art.py",
    "map.py",
    "pantone_color.py",
    "primitives.py",
    "shape.py",
    "slideshow.py",
    "smart_art.py",
    "source.py",
    "table.py",
]


def main(root: str):
    stk_todo = [Path(root)]
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
            if f.name == "__init__.py":
                continue
            if f.name.endswith(".py"):
                stk_done += [f]

    # loop over all .py files
    stk_large_python_files = []
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()
        if len(lines) > 400:
            stk_large_python_files += [python_file]
            continue

    # print all files that are too large
    for large_python_file in stk_large_python_files:
        if large_python_file.name in KNOWN_EXCEPTIONS:
            continue
        print(f"File {large_python_file} contains more than 400 lines")

    # filter out KNOWN_EXCEPTIONS
    stk_large_python_files = [
        x for x in stk_large_python_files if x.name not in KNOWN_EXCEPTIONS
    ]

    # sys.exit
    if len(stk_large_python_files) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import sys
import typing

KNOWN_EXCEPTIONS = [
    "lzw_decode.py",
    "primitives.py",
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

    # loop over all .py files
    exit_code: int = 0
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()

        lines = [l for l in lines if l.startswith("    def ")]
        unsorted_method_names: typing.List[str] = [
            __extract_method_name(l) for l in lines
        ]

        # constructor
        constructor_methods = [
            __extract_method_name(l) for l in lines if l.startswith("    def __init__")
        ]

        # filter private methods
        private_methods = [
            __extract_method_name(l)
            for l in lines
            if l.startswith("    def _") and not l.startswith("    def __init__")
        ]

        # filter public methods
        public_methods = [
            __extract_method_name(l) for l in lines if not l.startswith("    def _")
        ]

        # compare unsorted to sorted
        sorted_method_names = (
            sorted(constructor_methods)
            + sorted(private_methods)
            + sorted(public_methods)
        )

        if sorted_method_names != unsorted_method_names:

            # IF the file is a known exception
            # THEN skip it
            if python_file.name in KNOWN_EXCEPTIONS:
                continue

            exit_code = 1
            print(f"Methods unsorted in {python_file}")
            print(f"\t- <ACTUAL> \t <EXPECTED>")
            for m0, m1 in zip(unsorted_method_names, sorted_method_names):
                print(f"\t- {m0} \t {m1}")

    # exit
    sys.exit(exit_code)


if __name__ == "__main__":
    main(sys.argv[1])

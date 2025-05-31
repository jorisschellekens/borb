#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path


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
                stk_done += [f]

    # loop over all __init__.py files
    stk_empty_init_file = []
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()
        if len(lines) < 40:
            stk_empty_init_file += [python_file]

    # print all empty __init__.py files
    for empty_init_file in stk_empty_init_file:
        print(f"Empty __init__.py file found: {empty_init_file}")

    # sys.exit
    if len(stk_empty_init_file) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])

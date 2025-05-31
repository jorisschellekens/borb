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
            if f.name.endswith(".py"):
                stk_done += [f]

    # loop over all .py files
    stk_no_python_bash = []
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()
        if len(lines) < 2:
            stk_no_python_bash += [python_file]
            continue
        if lines[0] != "#!/usr/bin/env python\n":
            stk_no_python_bash += [python_file]
            continue
        if lines[1] != "# -*- coding: utf-8 -*-\n":
            stk_no_python_bash += [python_file]
            continue

    # print all files missing a python bash
    for python_file_without_bash in stk_no_python_bash:
        print(f"Missing python-bash in {python_file_without_bash}")

    # sys.exit
    if len(stk_no_python_bash) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])

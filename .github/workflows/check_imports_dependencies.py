#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

KNOWN_EXCEPTIONS = [
    "import collections\n",
    "import datetime\n",
    "import enum\n",
    "import functools\n",
    "import io\n",
    "import logging\n",
    "import math\n",
    "import os\n",
    "import pathlib\n",
    "import PIL.Image\n",
    "import re\n",
    "import requests\n",
    "import typing\n",
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
            if f.name.endswith(".py"):
                stk_done += [f]

    # loop over all .py files
    stk_class_uses_unknown_imports = []
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()

        # gather all imports
        imports = [x for x in lines if x.startswith("from ") and "import" in x]
        imports += [x for x in lines if x.startswith("import ")]

        # remove self-imports
        imports = [x for x in imports if not x.startswith("from borb.")]

        # remove KNOWN_EXCEPTIONS
        imports = [x for x in imports if x not in KNOWN_EXCEPTIONS]

        # debug
        if len(imports) > 0:
            print(f"Unknown imports in {python_file}")
            stk_class_uses_unknown_imports += [python_file]
            for imp in imports:
                print(f"\t{imp}")

    # sys.exit
    if len(stk_class_uses_unknown_imports) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])

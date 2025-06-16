#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import typing
from pathlib import Path

KNOWN_EXCEPTIONS: typing.List[str] = ["Chart"]


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
    class_name_to_class_file: typing.Dict[str, Path] = {}
    inheritance_graph: typing.Dict[str, typing.List[str]] = {}
    for python_file in stk_done:
        lines = []
        with open(python_file, "r") as python_file_handle:
            lines = python_file_handle.readlines()

            # should have a line 'class xxx(yyy)' such that
            # yyy inherits from LayoutElement
            lines = [x for x in lines if x.startswith("class ") and x.endswith(":\n")]

            # IF the file has no class definitions
            # THEN skip
            if len(lines) == 0:
                continue

            # keep track of inheritance
            for line in lines:
                m: re.match = re.compile(
                    "class (?P<x>[a-zA-Z0-9]+)\\((?P<y>[a-zA-Z0-9]+)\\):\n"
                ).match(line)

                # IF the class does not inherit from anything
                # THEN we are not interested in it (for the purposes of this workflow)
                if m is None:
                    continue

                # keep track of inheritance (and file)
                x: str = m.group("x")
                ys: typing.List[str] = [y.strip() for y in m.group("y").split(",")]
                inheritance_graph[x] = ys
                class_name_to_class_file[x] = python_file

    # find every descendant from LayoutElement
    stk_done = []
    stk_todo = ["LayoutElement"]
    while len(stk_todo) > 0:
        n: str = stk_todo.pop(0)
        for c in [k for k, v in inheritance_graph.items() if n in v]:
            stk_todo += [c]
        stk_done += [n]
    stk_done.sort()

    # DEBUG
    print(f"Found {len(stk_done)} classes that inherit from LayoutElement.")
    for class_name in stk_done:
        if class_name in KNOWN_EXCEPTIONS:
            print(f"   - {class_name} (EXCEPTION)")
        else:
            print(f"   - {class_name}")

    # find the constructor of each of these LayoutElement objects
    classes_missing_init_args: typing.List[typing.Tuple[str, Path]] = []
    for class_name in stk_done:
        if class_name in KNOWN_EXCEPTIONS:
            continue
        class_file: Path = class_name_to_class_file.get(class_name, None)
        if class_file is None:
            continue

        # get full text
        full_text: str = ""
        with open(class_file, "r") as fh:
            full_text = fh.read()
        while "\n" in full_text:
            full_text = full_text.replace("\n", " ")

        # find __init__ args
        if "def __init__" not in full_text:
            continue
        args_line = full_text[full_text.find("def __init__(") + len("def __init__(") :]
        args = [
            x.strip().split(":")[0].strip()
            for x in args_line[: args_line.find("):")].split(",")
        ]
        args.sort()
        if "" in args:
            args.remove("")
        if "self" in args:
            args.remove("self")

        # compare the args to those of LayoutElement.__init__
        missing_init_args: typing.List[str] = [
            x
            for x in [
                "background_color",
                "border_color",
                "border_dash_pattern",
                "border_width_bottom",
                "border_width_left",
                "border_width_right",
                "border_width_top",
                "horizontal_alignment",
                "margin_bottom",
                "margin_left",
                "margin_right",
                "margin_top",
                "padding_bottom",
                "padding_left",
                "padding_right",
                "padding_top",
                "vertical_alignment",
            ]
            if x not in args
        ]

        if len(missing_init_args) != 0:
            classes_missing_init_args += [(class_name, class_file, missing_init_args)]

    # DEBUG
    for class_name, class_file, missing_args in classes_missing_init_args:
        print(
            f"Class {class_name} (defined in {class_file}) is missing args {missing_args} inherited from LayoutElement"
        )

    # sys.exit
    if len(classes_missing_init_args) != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])

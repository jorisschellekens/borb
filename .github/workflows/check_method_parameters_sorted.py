import ast
import collections
import pathlib
import re
import typing
import sys

WarningType = collections.namedtuple(
    "WarningType",
    field_names=[
        "file",
        "function",
        "line_number",
        "text",
    ],
)


class ArgNameChecker(ast.NodeVisitor):

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self.__warnings: typing.List[WarningType] = []

    #
    # PUBLIC
    #

    def get_warnings(self) -> typing.List[WarningType]:
        return self.__warnings

    def visit_FunctionDef(self, node):
        # IF the function is private
        # THEN ignore it
        if node.name.startswith("__"):
            return
        if node.name.startswith("_"):
            return

        # split arguments in groups
        number_of_args: int = len(node.args.args)
        number_of_args_with_defaults: int = len(node.args.defaults)
        number_of_args_without_defaults: int = (
            number_of_args - number_of_args_with_defaults
        )
        args_without_default = [
            x
            for i, x in enumerate(node.args.args)
            if i < number_of_args_without_defaults
        ]
        args_with_default = [
            x
            for i, x in enumerate(node.args.args)
            if i >= number_of_args_without_defaults
        ]
        self_or_class_arg = []
        if len(args_without_default) > 0 and args_without_default[0].arg in [
            "self",
            "cls",
        ]:
            self_or_class_arg = [args_without_default[0]]
            args_without_default = args_without_default[1:]

        # sort arguments
        sorted_args = []
        sorted_args += sorted(self_or_class_arg)
        sorted_args += sorted(args_without_default, key=lambda x: x.arg)
        sorted_args += sorted(args_with_default, key=lambda x: x.arg)

        for i in range(0, len(sorted_args)):

            # IF the argument order does not match
            # THEN generate a warning
            if node.args.args[i] != sorted_args[i]:
                self.__warnings += [
                    WarningType(
                        file="",
                        function=node.name,
                        line_number=node.lineno,
                        text=f"Expected {sorted_args[i].arg}, found {node.args.args[i].arg}",
                    )
                ]
        self.generic_visit(node)


class CheckSomethingTemplate:

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        root: pathlib.Path,
        known_exceptions: typing.List[typing.Union[pathlib.Path, str]],
    ):
        self.__root: pathlib.Path = root
        self.__warnings: typing.List[WarningType] = []
        self.__number_of_files_checked: int = 0
        self.__known_exceptions: typing.List[pathlib.Path] = known_exceptions

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_number_of_files_checked(self) -> int:
        return self.__number_of_files_checked

    def get_warnings(self) -> typing.List[WarningType]:
        return self.__warnings

    def perform_check_on_directory(self) -> None:
        stk_todo = [self.__root]
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

        # filter out known_exceptions
        # fmt: off
        known_exceptions_01 = [x for x in self.__known_exceptions if isinstance(x, pathlib.Path)]
        known_exceptions_02 = [re.compile(x) for x in self.__known_exceptions if isinstance(x, str)]
        stk_done = [x for x in stk_done if x not in known_exceptions_01]
        stk_done = [x for x in stk_done if not any([y.match(x.name) is not None for y in known_exceptions_02])]
        # fmt: on

        # perform_check_on_file for each item in stk_done
        stk_done.sort(key=lambda x: x.name)
        for f in stk_done:
            self.perform_check_on_file(f)

    def perform_check_on_file(self, file: pathlib.Path) -> None:
        self.__number_of_files_checked += 1

        with open(file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file)
            arg_name_checker: ArgNameChecker = ArgNameChecker()
            arg_name_checker.visit(tree)
            self.__warnings += [
                WarningType(
                    file=file,
                    function=x.function,
                    line_number=x.line_number,
                    text=x.text,
                )
                for x in arg_name_checker.get_warnings()
            ]


if __name__ == "__main__":
    checker = CheckSomethingTemplate(
        root=pathlib.Path(sys.argv[1]),
        known_exceptions=["pdf_bytes.py", "source.py"],
    )
    checker.perform_check_on_directory()
    warnings: typing.List[WarningType] = checker.get_warnings()

    # IF everything passed
    # THEN display pass text
    if len(warnings) == 0:
        print(
            f"Finished checking {checker.get_number_of_files_checked()} file(s), everything OK"
        )

    # IF there are warnings
    # THEN display them
    if len(warnings) > 0:
        print(
            f"Finished checking {checker.get_number_of_files_checked()} file(s), found {len(warnings)} warnings:"
        )
        for w in warnings:
            if (
                w.file is not None
                and w.function is not None
                and w.line_number is not None
                and w.text is not None
            ):
                print(f"{w.file}:{w.function}:{w.line_number} {w.text}")
                continue
            if w.file is not None and w.line_number is not None and w.text is not None:
                print(f"{w.file}:{w.line_number} {w.text}")
                continue
            if w.file is not None and w.text is not None:
                print(f"{w.file} {w.text}")
                continue
            if w.file is not None:
                print(f"{w.file}")
                continue

        sys.exit(1)

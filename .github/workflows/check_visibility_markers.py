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
        lines: typing.List[str] = []
        try:
            with open(file, "r") as fh:
                lines = fh.readlines()
        except:
            return

        constructor_section_index = None
        private_section_index = None
        public_section_index = None
        for i in range(0, len(lines) - 2):
            # IF the next lines match a CONSTRUCTOR section
            # THEN keep track of it
            if (
                lines[i].strip().startswith("#")
                and lines[i + 1].strip().startswith("# CONSTRUCTOR")
                and lines[i + 2].strip().startswith("#")
                and constructor_section_index is None
            ):
                constructor_section_index = i
            # IF the next lines match a PRIVATE section
            # THEN keep track of the line number
            if (
                lines[i].strip().startswith("#")
                and lines[i + 1].strip().startswith("# PRIVATE")
                and lines[i + 2].strip().startswith("#")
                and private_section_index is None
            ):
                private_section_index = i
            # IF the next lines match a PUBLIC section
            # THEN keep track of the line number
            if (
                lines[i].strip().startswith("#")
                and lines[i + 1].strip().startswith("# PUBLIC")
                and lines[i + 2].strip().startswith("#")
                and public_section_index is None
            ):
                public_section_index = i

        if constructor_section_index is None:
            self.__warnings += [
                WarningType(
                    file=file,
                    function=None,
                    line_number=private_section_index or public_section_index or 0,
                    text=f"CONSTRUCTOR section not found",
                )
            ]
        if private_section_index is None:
            self.__warnings += [
                WarningType(
                    file=file,
                    function=None,
                    line_number=public_section_index or len(lines),
                    text=f"PRIVATE section not found",
                )
            ]
        if public_section_index is None:
            self.__warnings += [
                WarningType(
                    file=file,
                    function=None,
                    line_number=len(lines),
                    text=f"PUBLIC section not found",
                )
            ]


if __name__ == "__main__":
    checker = CheckSomethingTemplate(
        root=pathlib.Path(sys.argv[1]),
        known_exceptions=["__init__.py", "setup.py"],
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

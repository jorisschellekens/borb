import typing
from pathlib import Path


def get_all_code_files_in_repository() -> typing.List[Path]:

    # find root directory
    root_dir: Path = Path(__file__).parent
    while root_dir.exists() and ".github" not in [x.name for x in root_dir.iterdir()]:
        root_dir = root_dir.parent

    # find all code files
    todo_stk: typing.List[Path] = [root_dir / "borb"]
    python_files: typing.List[Path] = []
    while len(todo_stk) > 0:
        tmp: Path = todo_stk[0]
        todo_stk.pop(0)
        if tmp.is_dir():
            todo_stk += [x for x in tmp.iterdir()]
            continue
        if tmp.is_file() and tmp.name.endswith(".py"):
            python_files.append(tmp)

    # return
    return python_files

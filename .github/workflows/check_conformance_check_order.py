import pathlib
import sys
import typing


def main(root: str):

    # Crawl over the entire directory (useful if we ever decide to move the file)
    todo: typing.List[pathlib.Path] = [pathlib.Path(root)]
    done: typing.List[pathlib.Path] = []
    while len(todo) > 0:
        f: pathlib.Path = todo.pop()
        if f.is_dir():
            todo += [x for x in f.iterdir()]
            continue
        if f.is_file() and f.suffix == '.py':
            done += [f]

    # Find the file containing the conformance checks
    conformance_check_file: typing.Optional[pathlib.Path] = next(iter([x for x in done if x.stem == 'conformance_checks']))
    if conformance_check_file is None:
        sys.exit(1)

    # Read all the lines in this file
    lines: typing.List[str] = []
    with open(conformance_check_file, 'r') as fh:
        lines = fh.readlines()

    # Filter out the comments
    import re
    prev_n: int = 0
    prev_m: int = 0
    failed: bool = False
    for line in lines:
        match: typing.Optional[re.Match] = re.match(r'#\s\[(\d+)/(\d+)\]', line.strip())
        if match is None:
            continue
        n: int = int(match.group(1))
        m: int = int(match.group(2))
        if prev_n == 0 and prev_m == 0:
            prev_n = n
            prev_m = m
            continue
        if n < prev_n:
            print(f'Check out of order: [{n}/{m}] found AFTER [{prev_n}/{prev_m}]')
            failed = True
        if m != prev_m:
            print(f'Number of checks changed: [{n}/{m}] found AFTER [{prev_n}/{prev_m}]')
            failed = True
        prev_n = n
        prev_m = m

    # exit
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1])
import typing
from pathlib import Path


class Node:
    def __init__(self):
        self._line_number: int = 0
        self._indent_level: int = 0
        self._line: str = ""
        self._children: typing.List["Node"] = []
        self._parent: typing.Optional["Node"] = None

    def sort(self):
        self._children.sort(key=lambda x: x._line)
        self._children = (
            [x for x in self._children if x._line.strip().startswith("class")]
            + [x for x in self._children if x._line.strip().startswith("def __init__")]
            + [
                x
                for x in self._children
                if not x._line.strip().startswith("def __init__")
                and not x._line.strip().startswith("class")
            ]
        )
        for c in self._children:
            c.sort()

    def was_sorted(self) -> bool:
        for i in range(1, len(self._children)):
            c0: "Node" = self._children[i - 1]
            c1: "Node" = self._children[i]
            if c0._line_number > c1._line_number:
                return False
        for c in self._children:
            if not c.was_sorted():
                return False
        return True

    def __str__(self):
        s: str = ""
        if self._line != "":
            s += str(self._line_number) + "\t" + self._line
            if not s.endswith("\n"):
                s += "\n"
        for c in self._children:
            s += str(c)
        if not s.endswith("\n"):
            s += "\n"
        return s


def build_graph_for_file(input_file: Path) -> Node:

    # read lines
    lines: typing.List[str] = []
    with open(input_file, "r") as fh:
        lines = fh.readlines()

    # find class / def
    last_node: Node = Node()
    last_node._indent_level = -1
    for line_nr, line in enumerate(lines):

        # we only care about classes and methods
        is_class: bool = line.strip().startswith("class")
        is_method: bool = line.strip().startswith("def ")
        if not is_class and not is_method:
            continue

        # strip trailing newline
        if line.endswith("\n"):
            line = line[:-1]

        # determine level
        indent_level: int = 0
        while line[indent_level] == " ":
            indent_level += 1

        if indent_level > last_node._indent_level:
            new_node: Node = Node()
            new_node._indent_level = indent_level
            new_node._line_number = line_nr
            new_node._line = line
            new_node._parent = last_node
            last_node._children += [new_node]
            last_node = new_node
            continue

        if indent_level == last_node._indent_level:
            parent = last_node._parent
            new_node: Node = Node()
            new_node._indent_level = indent_level
            new_node._line_number = line_nr
            new_node._line = line
            new_node._parent = parent
            parent._children += [new_node]
            last_node = new_node
            continue

        if indent_level < last_node._indent_level:
            parent = last_node
            while indent_level <= parent._indent_level:
                parent = parent._parent
            new_node: Node = Node()
            new_node._indent_level = indent_level
            new_node._line_number = line_nr
            new_node._line = line
            new_node._parent = parent
            parent._children += [new_node]
            last_node = new_node
            continue

    # find root
    root = last_node
    while root._parent is not None:
        root = root._parent

    # return
    return root


if __name__ == "__main__":

    ignore_list: typing.List[str] = [
        "append_cubic_bezier.py",
        "barcode.py",
        "color.py",
        "font_type_1.py",
        "heterogeneous_paragraph.py",
        "low_level_tokenizer.py",
        "lzw_decode.py",
        "push_button.py",
        "redacted_canvas_stream_processor.py",
        "rubber_stamp_annotation.py",
        "table.py",
        "text_annotation.py",
        "transformer.py",
        "types.py",
    ]
    stk_todo: typing.List[Path] = [Path("/home/joris/Code/borb-dev/borb/")]
    nof_errors: int = 0
    nof_files: int = 0
    while len(stk_todo) > 0:
        p: Path = stk_todo[0]
        stk_todo.pop(0)
        if p.is_file() and p.name in ignore_list:
            continue
        if p.is_file() and p.name.endswith(".py"):
            nof_files += 1
            n: Node = build_graph_for_file(p)
            n.sort()
            if not n.was_sorted():
                nof_errors += 1
                print(str(n))
        if p.is_dir():
            stk_todo += [x for x in p.iterdir()]
    print("%d error(s) in %d file(s)" % (nof_errors, nof_files))

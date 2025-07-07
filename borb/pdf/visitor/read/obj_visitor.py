#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for reading and parsing individual PDF indirect objects.

`ObjVisitor` is specialized to locate and interpret indirect objects in a PDF,
specifically those defined by `obj` and `endobj` markers. This includes handling
dictionaries, as well as streams enclosed within `stream` and `endstream` markers.

Using the visitor pattern, `ObjVisitor` reads:
- Object metadata (object number and generation)
- Dictionary entries within the `<< >>` delimiters
- Embedded stream data, if present, converting it into a Python-compatible format.

This class enables accurate extraction and parsing of standalone PDF objects,
supporting detailed and low-level PDF content processing.
"""

import typing

from borb.pdf.primitives import PDFType, stream
from borb.pdf.visitor.read.read_visitor import ReadVisitor


class ObjVisitor(ReadVisitor):
    """
    Visitor class for reading and parsing individual PDF indirect objects.

    `ObjVisitor` is specialized to locate and interpret indirect objects in a PDF,
    specifically those defined by `obj` and `endobj` markers. This includes handling
    dictionaries, as well as streams enclosed within `stream` and `endstream` markers.

    Using the visitor pattern, `ObjVisitor` reads:
    - Object metadata (object number and generation)
    - Dictionary entries within the `<< >>` delimiters
    - Embedded stream data, if present, converting it into a Python-compatible format.

    This class enables accurate extraction and parsing of standalone PDF objects,
    supporting detailed and low-level PDF content processing.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def visit(
        self, node: typing.Union[int, bytes]
    ) -> typing.Optional[typing.Tuple[PDFType, int]]:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        if not isinstance(node, int):
            return None
        if self.get_bytes()[node] not in b"0123456789":
            return None

        # read object nr
        i: int = node
        j: int = node
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        object_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read generation number
        i = j
        if self.get_bytes()[i] not in b"0123456789":
            return None
        while self.get_bytes()[j] in b"0123456789":
            j += 1
        generation_nr: int = int(self.get_bytes()[i:j].decode())

        # read space
        i = j
        if self.get_bytes()[i : i + 1] != b" ":
            return None
        while self.get_bytes()[j : j + 1] == b" ":
            j += 1

        # read 'obj'
        i = j
        if self.get_bytes()[i : i + 3] != b"obj":
            return None
        i += 3

        # read newline or SPACE (\n\r )
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1
        if self.get_bytes()[i : i + 1] == b" ":
            i += 1

        # read object
        obj_or_dict_and_i = self.root_generic_visit(i)
        assert obj_or_dict_and_i is not None
        obj_or_dict, i = obj_or_dict_and_i

        # read space
        while self.get_bytes()[i : i + 1] == b" ":
            i += 1

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read 'endobj'
        has_seen_endobj: bool = False
        if self.get_bytes()[i : i + 6] == b"endobj":
            has_seen_endobj = True
            i += 6

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # IF we have read 'endobj'
        # THEN we do not need to read any further AND return
        if has_seen_endobj:
            return obj_or_dict, i

        # read 'stream'
        has_seen_stream: bool = False
        if self.get_bytes()[i : i + 6] == b"stream":
            has_seen_stream = True
            i += 6

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read the bytes of the stream
        assert isinstance(obj_or_dict, dict)
        assert "Length" in obj_or_dict
        assert isinstance(obj_or_dict["Length"], int)
        length: int = obj_or_dict["Length"]
        stream_bytes: bytes = self.get_bytes()[i : i + length]
        i += length

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read 'endstream'
        has_seen_endstream: bool = False
        if self.get_bytes()[i : i + 9] == b"endstream":
            has_seen_endstream = True
            i += 9

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # read 'endobj'
        if self.get_bytes()[i : i + 6] == b"endobj":
            i += 6

        # read newline (\n\r)
        if self.get_bytes()[i : i + 2] == b"\n\r":
            i += 2
        if self.get_bytes()[i : i + 2] == b"\r\n":
            i += 2
        if self.get_bytes()[i : i + 1] == b"\n":
            i += 1
        if self.get_bytes()[i : i + 1] == b"\r":
            i += 1

        # IF we have seen 'stream' and 'endstream' keyword
        # THEN we do not need to process any further bytes AND return
        if has_seen_stream and has_seen_endstream:
            retval = stream()
            for k, v in obj_or_dict.items():
                retval[k] = v
            retval["Bytes"] = stream_bytes
            return retval, i

        # default
        return None

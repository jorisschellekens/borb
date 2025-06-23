#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for building the cross-reference (XRef) table in a PDF.

`BuildXRefVisitor` is a specialized visitor used in the initial stages
of PDF serialization to construct the XRef table. It iterates through
objects in the PDF document structure, replacing each object with a
`Reference` where appropriate, thus marking it as an item to be cross-referenced.
This class is primarily responsible for identifying which objects need to
be added to the XRef table and creating these references.

This visitor does not handle the persistence or writing of the XRef table
itself; it only prepares the objects for later serialization. Actual
persistence of the XRef data is handled by other components in the
serialization process, following the completion of this visitor's work.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.primitives import PDFType, reference, name
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class BuildXRefVisitor(WriteNewVisitor):
    """
    Visitor class for building the cross-reference (XRef) table in a PDF.

    `BuildXRefVisitor` is a specialized visitor used in the initial stages
    of PDF serialization to construct the XRef table. It iterates through
    objects in the PDF document structure, replacing each object with a
    `Reference` where appropriate, thus marking it as an item to be cross-referenced.
    This class is primarily responsible for identifying which objects need to
    be added to the XRef table and creating these references.

    This visitor does not handle the persistence or writing of the XRef table
    itself; it only prepares the objects for later serialization. Actual
    persistence of the XRef data is handled by other components in the
    serialization process, following the completion of this visitor's work.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __build_xref(document: Document) -> typing.List[reference]:

        id_to_parent_dict: typing.Dict[int, PDFType] = {}
        xref: typing.List[reference] = []
        stk: typing.List[PDFType] = [document]
        while len(stk) > 0:

            m: PDFType = stk.pop()
            p: typing.Optional[PDFType] = id_to_parent_dict.get(id(m))

            # IF the object is already in the XREF
            # THEN skip
            if any([id(x.get_referenced_object()) == id(m) for x in xref]):
                continue

            # handle parent link for dictionaries
            if isinstance(m, dict):
                for k in sorted(m.keys()):
                    v = m[k]
                    id_to_parent_dict[id(v)] = m
                    stk += [v]

            # handle parent link for lists
            if isinstance(m, list):
                for v in m:
                    id_to_parent_dict[id(v)] = m
                    stk += [v]

            # IF the object should be a direct object
            # THEN skip
            if BuildXRefVisitor.__is_direct_object(m, p):
                continue

            # IF the object is the xref
            # THEN skip
            if (
                isinstance(p, dict)
                and ("XRef" in p)
                and (p["XRef"] is not None)
                and p["XRef"] == m
            ):
                continue

            # IF the object is not a direct object
            # THEN get the next available reference
            if isinstance(m, list) or isinstance(m, dict):
                max_obj_nr = max(
                    [xref_entry.get_object_nr() for xref_entry in xref] + [0]
                )
                xref += [
                    reference(
                        object_nr=max_obj_nr + 1,
                        generation_nr=0,
                        id=id(m),
                        referenced_object=m,
                    )
                ]

        # return
        return xref

    @staticmethod
    def __is_direct_object(n: PDFType, p: typing.Optional[PDFType]) -> bool:

        # /
        if isinstance(n, Document):
            return True

        # /Trailer
        if (
            p is not None
            and isinstance(p, Document)
            and isinstance(n, dict)
            and "Root" in n
            and "Info" in n
        ):
            return True

        # /Trailer /ID
        if (
            p is not None
            and isinstance(p, dict)
            and "ID" in p
            and p["ID"] == n
            and isinstance(n, list)
            and len(n) == 2
        ):
            return True

        # /Trailer /Root /Pages /Kids
        if (
            p is not None
            and isinstance(p, dict)
            and "Type" in p
            and p["Type"] == "Pages"
            and "Kids" in p
            and p["Kids"] == n
        ):
            return True

        # /Trailer /Root /MarkInfo
        if (
            p is not None
            and isinstance(p, dict)
            and "MarkInfo" in p
            and p["MarkInfo"] == n
        ):
            return True

        # /Trailer /Root /StructTreeRoot /K
        if (
            p is not None
            and isinstance(p, dict)
            and "Type" in p
            and p["Type"] == "StructTreeRoot"
            and "K" in p
            and p["K"] == n
        ):
            return True

        # /Trailer /Root /Pages /Kids <index> /CropBox
        if (
            p is not None
            and isinstance(p, dict)
            and "Type" in p
            and p["Type"] == "Page"
            and "CropBox" in p
            and p["CropBox"] == n
        ):
            return True

        # /Trailer /Root /Pages /Kids <index> /MediaBox
        if (
            p is not None
            and isinstance(p, dict)
            and "Type" in p
            and p["Type"] == "Page"
            and "MediaBox" in p
            and p["MediaBox"] == n
        ):
            return True

        # /Trailer /Root /Pages /Kids <index> /ProcSet
        if (
            p is not None
            and isinstance(p, dict)
            and "Type" in p
            and p["Type"] == "Page"
            and "ProcSet" in p
            and p["ProcSet"] == n
        ):
            return True

        # lists of 4 (primitive) elements or fewer
        if (
            n is not None
            and isinstance(n, list)
            and len(n) <= 4
            and all(
                [
                    isinstance(x, int)
                    or isinstance(x, float)
                    or isinstance(x, bool)
                    or isinstance(x, reference)
                    for x in n
                ]
            )
        ):
            return True

        # default
        return False

    #
    # PUBLIC
    #

    def visit(self, node: typing.Any) -> bool:
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
        # check whether this is a document
        if not isinstance(node, Document):
            return False
        if "XRef" not in node:
            return False
        if len(node["XRef"]) != 0:
            return False
        if "Trailer" not in node:
            return False

        # build the XRef table for the Document
        node["XRef"] = self.__build_xref(document=node)

        # set the /Trailer /Size entry
        node.get("Trailer", {})[name("Size")] = len(node["XRef"]) + 1

        # call other visitor(s)
        self.go_to_root_and_visit(node)

        # return
        return True

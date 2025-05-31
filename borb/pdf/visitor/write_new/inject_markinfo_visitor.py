#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor that injects a MarkInfo dictionary into a PDF to improve accessibility and ensure tagged PDF compliance.

This visitor modifies the document's catalog by adding or updating the /MarkInfo
entry, which indicates the presence of tagged content. The /MarkInfo dictionary
is essential for PDF/UA (Universal Accessibility) compliance and helps assistive
technologies interpret the document structure correctly.

The visitor follows the visitor pattern to traverse and modify the document,
ensuring that the /MarkInfo dictionary is injected if it is missing. If an entry
already exists, it is left unchanged unless an update is required.
"""
import typing

from borb.pdf.conformance import Conformance
from borb.pdf.primitives import name
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class InjectMarkInfoVisitor(WriteNewVisitor):
    """
    A visitor that injects a MarkInfo dictionary into a PDF to improve accessibility and ensure tagged PDF compliance.

    This visitor modifies the document's catalog by adding or updating the /MarkInfo
    entry, which indicates the presence of tagged content. The /MarkInfo dictionary
    is essential for PDF/UA (Universal Accessibility) compliance and helps assistive
    technologies interpret the document structure correctly.

    The visitor follows the visitor pattern to traverse and modify the document,
    ensuring that the /MarkInfo dictionary is injected if it is missing. If an entry
    already exists, it is left unchanged unless an update is required.
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

    def visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
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
        from borb.pdf.document import Document

        if not isinstance(node, Document):
            return False
        conformance: typing.Optional[Conformance] = node.get_conformance_at_create()
        if conformance is None:
            return False
        if not conformance.requires_tagged_pdf():
            return False
        if "Trailer" not in node:
            return False
        if "Root" not in node["Trailer"]:
            return False

        # get Catalog
        catalog: typing.Dict[typing.Union[name, str], typing.Any] = node["Trailer"][
            "Root"
        ]

        # IF MarkInfo is already present
        # THEN skip
        if "MarkInfo" in catalog:
            if (
                isinstance(catalog.get("MarkInfo"), dict)
                and catalog.get("MarkInfo").get("Marked", False) == True  # type: ignore[union-attr]
            ):
                return False

        # add MarkInfo
        if catalog.get("MarkInfo", {}).get("Marked", False) == False:
            catalog[name("MarkInfo")] = {name("Marked"): True}

        # call root
        super().go_to_root_and_visit(node=node)

        # return
        return True

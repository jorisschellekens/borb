#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor to construct and inject a StructTreeRoot into a PDF document, ensuring proper tagging for accessibility.

This visitor scans the document's content streams, identifying nested MCIDs
(Marked Content Identifiers) to reconstruct the document's structure tree.
The StructTreeRoot is a critical component for tagged PDFs, enabling proper
navigation and accessibility for assistive technologies (e.g., screen readers).

The class follows the visitor pattern to traverse the document, creating a
logical structure hierarchy based on the marked content. If a StructTreeRoot
is missing, it is injected into the document's catalog.
"""
import re
import typing

from borb.pdf.conformance import Conformance
from borb.pdf.page import Page
from borb.pdf.primitives import name, stream
from borb.pdf.visitor.read.compression.decode_stream import decode_stream
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class InjectStructTreeRootVisitor(WriteNewVisitor):
    """
    A visitor to construct and inject a StructTreeRoot into a PDF document, ensuring proper tagging for accessibility.

    This visitor scans the document's content streams, identifying nested MCIDs
    (Marked Content Identifiers) to reconstruct the document's structure tree.
    The StructTreeRoot is a critical component for tagged PDFs, enabling proper
    navigation and accessibility for assistive technologies (e.g., screen readers).

    The class follows the visitor pattern to traverse the document, creating a
    logical structure hierarchy based on the marked content. If a StructTreeRoot
    is missing, it is injected into the document's catalog.
    """

    # fmt: off
    BMD_PATTERN: re.Pattern = re.compile(r"/([A-Za-z0-9]+)\s*<<[^>]*?/MCID\s+(\d+)[^>]*?>>\s*BDC")
    EMC_PATTERN: re.Pattern = re.compile(r"\bEMC\b")
    # fmt: on

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

        # IF the document already has a StructTreeRoot
        # THEN skip
        if "StructTreeRoot" in catalog:
            return False

        # create an (empty) StructTreeRoot
        catalog[name("StructTreeRoot")] = {
            name("Type"): name("StructTreeRoot"),
            name("K"): [],
        }

        # loop over all pages
        import copy

        for page_nr in range(0, node.get_number_of_pages()):

            # get Page
            page: Page = node.get_page(page_nr)

            # get content stream
            content_stream_bytes: bytes = b""
            if isinstance(page["Contents"], list):
                content_stream_bytes = b"".join(
                    [
                        decode_stream(cs).get("DecodedBytes", b"")
                        for cs in page["Contents"]
                    ]
                )
            if isinstance(page["Contents"], stream):
                content_stream_bytes = decode_stream(page["Contents"]).get(
                    "DecodedBytes", b""
                )

            # gather all matches (BMD, EMC) and sort them
            bmd_matches: typing.List[re.Match] = [
                x
                for x in InjectStructTreeRootVisitor.BMD_PATTERN.finditer(
                    content_stream_bytes.decode("latin1")
                )
            ]
            emc_matches: typing.List[re.Match] = [
                x
                for x in InjectStructTreeRootVisitor.EMC_PATTERN.finditer(
                    content_stream_bytes.decode("latin1")
                )
            ]
            all_matches: typing.List[typing.Tuple[bool, re.Match]] = [
                (True, x) for x in bmd_matches
            ] + [(False, x) for x in emc_matches]
            all_matches.sort(key=lambda x: x[1].start())

            # loop over all matches
            stk = [catalog["StructTreeRoot"]]
            for is_open, m in all_matches:

                # IF the element is a closing element
                # THEN pop from the stack
                if not is_open:
                    stk.pop(0)
                    continue

                # IF the element is an opening element
                # THEN create the element
                if is_open:
                    parent = stk[0]
                    if "K" not in parent:
                        parent[name("K")] = []

                    # IF /K is in the parent AND an integer
                    # THEN we need to create an intermediate element
                    if "K" in parent and isinstance(parent["K"], int):
                        intermediate_struct_elem = copy.deepcopy(
                            {k: v for k, v in parent.items() if k != "P"}
                        )
                        intermediate_struct_elem[name("P")] = parent
                        parent["K"] = [intermediate_struct_elem]
                        parent = intermediate_struct_elem

                    # add new element
                    struct_elem = {
                        name("S"): name(m.group(1)),
                        name("Type"): name("StructElem"),
                        name("K"): int(m.group(2)),
                        name("P"): parent,
                    }
                    parent["K"] += [struct_elem]

                    # push this thing on top
                    stk = [struct_elem] + stk

        # call other visitor(s)
        super().go_to_root_and_visit(node=node)

        # return
        return True

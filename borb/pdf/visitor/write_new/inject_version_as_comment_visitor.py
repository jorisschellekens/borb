#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A specialized PDF visitor that injects versioning and licensing metadata as comments  into a PDF document.

This visitor operates within the `borb` PDF generation and manipulation framework and
extends the `WriteNewVisitor` to insert a version comment block at the beginning of
the PDF serialization. The injected block includes the current `borb` version and
license information (either AGPL or the licensed company name), prefixed with `#`
to conform to comment syntax where applicable.

The visitor is designed to run only once per session to prevent redundant metadata
injection. It uses an internal state flag to enforce single-use behavior. Typically
employed at the root level of a visitor hierarchy, this visitor ensures version
tracking and attribution in generated PDF files, which is useful for diagnostics,
auditing, and support.
"""
import typing

from borb.pdf import License
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class InjectVersionAsCommentVisitor(WriteNewVisitor):
    """
    A specialized PDF visitor that injects versioning and licensing metadata as comments  into a PDF document.

    This visitor operates within the `borb` PDF generation and manipulation framework and
    extends the `WriteNewVisitor` to insert a version comment block at the beginning of
    the PDF serialization. The injected block includes the current `borb` version and
    license information (either AGPL or the licensed company name), prefixed with `#`
    to conform to comment syntax where applicable.

    The visitor is designed to run only once per session to prevent redundant metadata
    injection. It uses an internal state flag to enforce single-use behavior. Typically
    employed at the root level of a visitor hierarchy, this visitor ensures version
    tracking and attribution in generated PDF files, which is useful for diagnostics,
    auditing, and support.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize a new instance of `InjectVersionAsCommentVisitor`.

        This constructor prepares the visitor to inject a version and license comment
        block into a PDF during serialization. It optionally accepts a root `NodeVisitor`,
        allowing this visitor to participate in a composite visitor hierarchy and delegate
        traversal when required.

        An internal flag (`__has_been_used`) ensures the comment is inserted only once,
        maintaining idempotent behavior across multiple visits.

        :param root: An optional `NodeVisitor` instance representing the root of the visitor
                     hierarchy, often used to manage shared context or data among multiple
                     visitors. Defaults to `None`.
        """
        super().__init__(root=root)
        self.__has_been_used: bool = False

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
        # IF we are not processing a ReferencedObject type
        # THEN return
        from borb.pdf.visitor.write_new.document_visitor import ReferencedObjectType

        if not isinstance(node, ReferencedObjectType):
            return False

        # IF the version info has already been embedded in the PDF
        # THEN do not do so again
        if self.__has_been_used:
            return False

        # IF we are in the first 1Kb
        # THEN do nothing
        N: int = len(self.bytes())
        if N < 1024:
            return False

        # append bytes
        from borb.pdf import Version

        if License.get_company():
            self._append_newline_to_output_stream()
            self._append_bytes_or_str(
                f"% borb\n"
                f"% version {Version.get_current_version()}\n"
                f"% Licensed to {License.get_company()}"
                "\n"
                "\n"
            )
        else:
            self._append_newline_to_output_stream()
            self._append_bytes_or_str(
                f"% borb\n"
                f"% version {Version.get_current_version()}\n"
                f"% AGPL"
                "\n"
                "\n"
            )

        self.__has_been_used = True

        # call root
        super().go_to_root_and_visit(node=node)

        # return
        return True

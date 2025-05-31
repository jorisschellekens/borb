#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor that injects an sRGB OutputIntent into a PDF document to ensure PDF/A compliance.

This visitor class modifies the PDF document by adding an OutputIntent dictionary
to the document's catalog. The OutputIntent ensures that any DeviceRGB colors are
properly defined with an embedded sRGB ICC profile, which is a requirement for PDF/A-1
compliance. PDF/A-1 standards prohibit the use of DeviceRGB without an associated
OutputIntent, and this visitor ensures that the document conforms to that specification.

The class uses the visitor pattern to traverse and modify the PDF document, adding
the required OutputIntent information if it's not already present. It performs the
injection only once per session to avoid redundant operations.
"""
import typing

from borb.pdf.conformance import Conformance
from borb.pdf.primitives import name, stream
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class InjectsRGBOutputIntentVisitor(WriteNewVisitor):
    """
    A visitor that injects an sRGB OutputIntent into a PDF document to ensure PDF/A compliance.

    This visitor class modifies the PDF document by adding an OutputIntent dictionary
    to the document's catalog. The OutputIntent ensures that any DeviceRGB colors are
    properly defined with an embedded sRGB ICC profile, which is a requirement for PDF/A-1
    compliance. PDF/A-1 standards prohibit the use of DeviceRGB without an associated
    OutputIntent, and this visitor ensures that the document conforms to that specification.

    The class uses the visitor pattern to traverse and modify the PDF document, adding
    the required OutputIntent information if it's not already present. It performs the
    injection only once per session to avoid redundant operations.
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
        if not conformance.requires_icc_color_profile():
            return False
        if "Trailer" not in node:
            return False
        if "Root" not in node["Trailer"]:
            return False
        if "Info" not in node["Trailer"]:
            return False

        # get Catalog
        catalog: typing.Dict[typing.Union[name, str], typing.Any] = node["Trailer"][
            "Root"
        ]

        # IF there is an /OutputIntents /OutputConditionIdentifier sRGB
        # THEN skip
        if any(
            [
                x.get("OutputConditionIdentifier", None) == "sRGB"
                for x in catalog.get("OutputIntents", [])
            ]
        ):
            return False

        # add OutputIntents
        if "OutputIntents" not in catalog:
            catalog[name("OutputIntents")] = []

        # add /OutputIntents /OutputConditionIdentifier /DestOutputProfile
        catalog["OutputIntents"] += [
            {
                name("Type"): name("OutputIntent"),
                name("S"): name("GTS_PDFA1"),
                name("OutputConditionIdentifier"): "sRGB",
                name("DestOutputProfile"): stream(
                    {
                        name("N"): 3,
                        name(
                            "DecodedBytes"
                        ): b"\x00\x00\x020ADBE\x02\x10\x00\x00mntrRGB XYZ \x07\xd0\x00\x08\x00\x0b\x00\x13\x003\x00;acspAPPL\x00\x00\x00\x00none\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf6\xd6\x00\x01\x00\x00\x00\x00\xd3-ADBE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\ncprt\x00\x00\x00\xfc\x00\x00\x002desc\x00\x00\x010\x00\x00\x00kwtpt\x00\x00\x01\x9c\x00\x00\x00\x14bkpt\x00\x00\x01\xb0\x00\x00\x00\x14rTRC\x00\x00\x01\xc4\x00\x00\x00\x0egTRC\x00\x00\x01\xd4\x00\x00\x00\x0ebTRC\x00\x00\x01\xe4\x00\x00\x00\x0erXYZ\x00\x00\x01\xf4\x00\x00\x00\x14gXYZ\x00\x00\x02\x08\x00\x00\x00\x14bXYZ\x00\x00\x02\x1c\x00\x00\x00\x14text\x00\x00\x00\x00Copyright 2000 Adobe Systems Incorporated\x00\x00\x00desc\x00\x00\x00\x00\x00\x00\x00\x11Adobe RGB (1998)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00XYZ \x00\x00\x00\x00\x00\x00\xf3Q\x00\x01\x00\x00\x00\x01\x16\xccXYZ \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00curv\x00\x00\x00\x00\x00\x00\x00\x01\x023\x00\x00curv\x00\x00\x00\x00\x00\x00\x00\x01\x023\x00\x00curv\x00\x00\x00\x00\x00\x00\x00\x01\x023\x00\x00XYZ \x00\x00\x00\x00\x00\x00\x9c\x18\x00\x00O\xa5\x00\x00\x04\xfcXYZ \x00\x00\x00\x00\x00\x004\x8d\x00\x00\xa0,\x00\x00\x0f\x95XYZ \x00\x00\x00\x00\x00\x00&1\x00\x00\x10/\x00\x00\xbe\x9c",
                    }
                ),
            }
        ]

        # call other visitor(s)
        super().go_to_root_and_visit(node=node)

        # return
        return True
